#!/usr/bin/env python3
"""Deterministic PPTX native-object, geometry, and semantic-coverage audit.

The audit compares PresentationML top-level objects with a pre-build
native-object-intent-plan.json. It reports observed computation only; it does
not claim content fit, visual quality, edit-session success, or learner outcome.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree as ET


EMU_PER_PT = 12700.0
NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}
TABLE_URI = "http://schemas.openxmlformats.org/drawingml/2006/table"
CHART_URI = "http://schemas.openxmlformats.org/drawingml/2006/chart"
DEFAULT_THRESHOLDS = {
    "profile_id": "visual-authoring-default-v1",
    "safe_margin_pt": 0.0,
    "alignment_tolerance_pt": 1.5,
    "spacing_tolerance_ratio": 0.15,
    "spacing_tolerance_pt_when_zero": 1.5,
    "overlap_epsilon_ratio": 0.01,
    "unplanned_text_overlap_epsilon_ratio": 0.01,
    "connector_endpoint_tolerance_pt": 3.0,
    "minimum_native_unit_coverage": 0.0,
    "minimum_required_relation_coverage": 1.0,
}

REQUIRED_INTENT_ROOT_FIELDS = {
    "contract_version",
    "target_medium",
    "style_materialization",
    "threshold_profile",
    "slides",
    "waivers",
}
REQUIRED_INTENT_UNIT_FIELDS = {
    "unit_id",
    "slide_number",
    "semantic_role",
    "criticality",
    "native_requirement",
    "expected_native_type",
    "planned_object_names",
    "edit_boundary",
    "group_name",
    "z_order",
    "reading_order",
    "required_relations",
    "presentation_behavior",
    "raster_exception_reason",
}
VALID_CRITICALITY = {"critical", "high_change", "supporting"}
VALID_NATIVE_REQUIREMENT = {"required", "preferred", "raster_allowed", "not_applicable"}
VALID_NATIVE_TYPE = {"text", "shape", "table", "chart", "connector", "group", "picture", "any_native"}
VALID_RELATIONS = {
    "inside_safe_area",
    "separate",
    "contain",
    "overlay",
    "align_left",
    "align_right",
    "align_top",
    "align_bottom",
    "align_center_x",
    "align_center_y",
    "horizontal_gap",
    "vertical_gap",
    "connect",
}


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def bottom(self) -> float:
        return self.y + self.h

    @property
    def center_x(self) -> float:
        return self.x + self.w / 2.0

    @property
    def center_y(self) -> float:
        return self.y + self.h / 2.0

    @property
    def area(self) -> float:
        return max(0.0, self.w) * max(0.0, self.h)

    def as_dict(self) -> dict[str, float]:
        return {"x_pt": self.x, "y_pt": self.y, "w_pt": self.w, "h_pt": self.h}


@dataclass(frozen=True)
class Transform:
    """Axis-aligned DrawingML coordinate transform in point units."""

    sx: float = 1.0
    sy: float = 1.0
    tx: float = 0.0
    ty: float = 0.0

    def apply(self, box: Box) -> Box:
        return Box(
            self.sx * box.x + self.tx,
            self.sy * box.y + self.ty,
            self.sx * box.w,
            self.sy * box.h,
        )

    def compose(self, child: "Transform") -> "Transform":
        """Return self(child(point)); used for nested editable groups."""
        return Transform(
            sx=self.sx * child.sx,
            sy=self.sy * child.sy,
            tx=self.sx * child.tx + self.tx,
            ty=self.sy * child.ty + self.ty,
        )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_json(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def emu_to_pt(value: str | int | None) -> float:
    try:
        return float(value or 0) / EMU_PER_PT
    except (TypeError, ValueError):
        return 0.0


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def union_box(boxes: Iterable[Box]) -> Box | None:
    items = list(boxes)
    if not items:
        return None
    x1 = min(item.x for item in items)
    y1 = min(item.y for item in items)
    x2 = max(item.right for item in items)
    y2 = max(item.bottom for item in items)
    return Box(x1, y1, x2 - x1, y2 - y1)


def intersection_area(a: Box, b: Box) -> float:
    width = max(0.0, min(a.right, b.right) - max(a.x, b.x))
    height = max(0.0, min(a.bottom, b.bottom) - max(a.y, b.y))
    return width * height


def overlap_ratio(a: Box, b: Box) -> float:
    denominator = min(a.area, b.area)
    return 0.0 if denominator <= 0 else intersection_area(a, b) / denominator


def horizontal_gap(a: Box, b: Box) -> float:
    if a.right <= b.x:
        return b.x - a.right
    if b.right <= a.x:
        return a.x - b.right
    return 0.0


def vertical_gap(a: Box, b: Box) -> float:
    if a.bottom <= b.y:
        return b.y - a.bottom
    if b.bottom <= a.y:
        return a.y - b.bottom
    return 0.0


def q1(value: float) -> float:
    return round(float(value), 3)


def pptx_slide_paths(archive: zipfile.ZipFile) -> list[str]:
    fallback = sorted(
        (name for name in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)),
        key=lambda name: int(re.search(r"(\d+)\.xml$", name).group(1)),
    )
    try:
        presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
        rels = ET.fromstring(archive.read("ppt/_rels/presentation.xml.rels"))
    except KeyError:
        return fallback
    rel_map = {
        node.get("Id"): node.get("Target")
        for node in rels.findall("pr:Relationship", NS)
        if node.get("Id") and node.get("Target")
    }
    ordered: list[str] = []
    for slide_id in presentation.findall("p:sldIdLst/p:sldId", NS):
        target = rel_map.get(slide_id.get(f"{{{NS['r']}}}id"))
        if not target:
            continue
        normalized = os.path.normpath(os.path.join("ppt", target)).replace("\\", "/")
        if normalized in archive.namelist():
            ordered.append(normalized)
    return ordered or fallback


def slide_size(archive: zipfile.ZipFile) -> tuple[float, float]:
    presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
    size = presentation.find("p:sldSz", NS)
    if size is None:
        raise ValueError("ppt/presentation.xml has no p:sldSz")
    return emu_to_pt(size.get("cx")), emu_to_pt(size.get("cy"))


def find_transform(node: ET.Element, kind: str) -> ET.Element | None:
    paths = {
        "sp": "p:spPr/a:xfrm",
        "pic": "p:spPr/a:xfrm",
        "graphicFrame": "p:xfrm",
        "cxnSp": "p:spPr/a:xfrm",
        "grpSp": "p:grpSpPr/a:xfrm",
    }
    return node.find(paths[kind], NS)


def parse_box(node: ET.Element, kind: str) -> Box | None:
    transform = find_transform(node, kind)
    if transform is None:
        return None
    off = transform.find("a:off", NS)
    ext = transform.find("a:ext", NS)
    if off is None or ext is None:
        return None
    return Box(
        emu_to_pt(off.get("x")),
        emu_to_pt(off.get("y")),
        emu_to_pt(ext.get("cx")),
        emu_to_pt(ext.get("cy")),
    )


def group_child_transform(node: ET.Element) -> Transform:
    """Map child coordinates in a:p:grpSp into the parent coordinate space."""
    transform = find_transform(node, "grpSp")
    if transform is None:
        return Transform()
    off = transform.find("a:off", NS)
    ext = transform.find("a:ext", NS)
    child_off = transform.find("a:chOff", NS)
    child_ext = transform.find("a:chExt", NS)
    if off is None or ext is None or child_off is None or child_ext is None:
        return Transform()
    off_x, off_y = emu_to_pt(off.get("x")), emu_to_pt(off.get("y"))
    ext_w, ext_h = emu_to_pt(ext.get("cx")), emu_to_pt(ext.get("cy"))
    child_x, child_y = emu_to_pt(child_off.get("x")), emu_to_pt(child_off.get("y"))
    child_w, child_h = emu_to_pt(child_ext.get("cx")), emu_to_pt(child_ext.get("cy"))
    sx = ext_w / child_w if child_w else 1.0
    sy = ext_h / child_h if child_h else 1.0
    return Transform(sx=sx, sy=sy, tx=off_x - child_x * sx, ty=off_y - child_y * sy)


def object_type(node: ET.Element, kind: str) -> str:
    if kind == "pic":
        return "picture"
    if kind == "cxnSp":
        return "connector"
    if kind == "grpSp":
        return "group"
    if kind == "graphicFrame":
        data = node.find("a:graphic/a:graphicData", NS)
        uri = data.get("uri") if data is not None else ""
        if uri == TABLE_URI:
            return "table"
        if uri == CHART_URI or "chart" in uri:
            return "chart"
        return "graphic_frame"
    text = "".join((item.text or "") for item in node.findall(".//a:t", NS)).strip()
    return "text" if text else "shape"


def non_visual_properties(node: ET.Element, kind: str) -> ET.Element | None:
    paths = {
        "sp": "p:nvSpPr/p:cNvPr",
        "pic": "p:nvPicPr/p:cNvPr",
        "graphicFrame": "p:nvGraphicFramePr/p:cNvPr",
        "cxnSp": "p:nvCxnSpPr/p:cNvPr",
        "grpSp": "p:nvGrpSpPr/p:cNvPr",
    }
    return node.find(paths[kind], NS)


def connector_target_ids(node: ET.Element) -> list[int]:
    values: list[int] = []
    for path in ("p:nvCxnSpPr/p:cNvCxnSpPr/a:stCxn", "p:nvCxnSpPr/p:cNvCxnSpPr/a:endCxn"):
        endpoint = node.find(path, NS)
        if endpoint is not None and endpoint.get("id"):
            try:
                values.append(int(endpoint.get("id")))
            except ValueError:
                pass
    return values


def parse_slide(archive: zipfile.ZipFile, path: str, slide_number: int, width: float, height: float) -> dict[str, Any]:
    root = ET.fromstring(archive.read(path))
    tree = root.find("p:cSld/p:spTree", NS)
    objects: list[dict[str, Any]] = []
    flat_order = 0

    def walk(container: ET.Element, parent_transform: Transform, group_path: list[str]) -> None:
        nonlocal flat_order
        for node in list(container):
            kind = local_name(node.tag)
            if kind not in {"sp", "pic", "graphicFrame", "cxnSp", "grpSp"}:
                continue
            flat_order += 1
            props = non_visual_properties(node, kind)
            box = parse_box(node, kind)
            if box is not None:
                box = parent_transform.apply(box)
            object_id = None
            if props is not None and props.get("id"):
                try:
                    object_id = int(props.get("id"))
                except ValueError:
                    pass
            item = {
                "object_id": object_id,
                "name": props.get("name") if props is not None else None,
                "type": object_type(node, kind),
                "xml_kind": kind,
                "order": flat_order,
                "bbox": {key: q1(value) for key, value in box.as_dict().items()} if box else None,
                "connector_target_ids": connector_target_ids(node) if kind == "cxnSp" else [],
                "group_path": group_path,
            }
            objects.append(item)
            if kind == "grpSp":
                name = item.get("name") or f"group-{object_id or flat_order}"
                child_transform = parent_transform.compose(group_child_transform(node))
                walk(node, child_transform, [*group_path, name])

    if tree is not None:
        walk(tree, Transform(), [])
    density = len(objects) / ((width * height) / 1_000_000.0) if width > 0 and height > 0 else None
    type_counts: dict[str, int] = {}
    for item in objects:
        item_type = item["type"]
        type_counts[item_type] = type_counts.get(item_type, 0) + 1
    return {
        "slide_number": slide_number,
        "part": path,
        "object_count": len(objects),
        "object_type_counts": type_counts,
        "object_density_per_million_pt2": q1(density) if density is not None else None,
        "objects": objects,
    }


def box_from_object(item: dict[str, Any]) -> Box | None:
    bbox = item.get("bbox")
    if not bbox:
        return None
    return Box(bbox["x_pt"], bbox["y_pt"], bbox["w_pt"], bbox["h_pt"])


def overlap_exception_pair(left: str, right: str) -> tuple[str, str]:
    """Return a stable name pair for an intentional text-on-text overlay."""
    return tuple(sorted((left, right)))


def object_label(item: dict[str, Any]) -> str:
    """Use the semantic object name when present, never an empty exception key."""
    name = item.get("name")
    return str(name) if name else f"object_id:{item.get('object_id', 'unknown')}"


def intentional_text_overlap_pairs(intent: dict[str, Any]) -> dict[int, set[tuple[str, str]]]:
    pairs: dict[int, set[tuple[str, str]]] = {}
    for exception in intent.get("overlap_exceptions", []):
        slide_number = int(exception["slide_number"])
        left, right = [str(name) for name in exception["object_names"]]
        pairs.setdefault(slide_number, set()).add(overlap_exception_pair(left, right))
    return pairs


def type_matches(expected: str, actual: str) -> bool:
    if expected in {"", "any", "any_object"}:
        return True
    if expected == "any_native":
        return actual in {"text", "shape", "table", "chart", "connector", "group", "graphic_frame"}
    return expected == actual


def ratio_or_na(numerator: int, denominator: int) -> float | str:
    return round(numerator / denominator, 6) if denominator else "not_applicable"


def add_finding(findings: list[dict[str, Any]], slide: int, unit: str, relation: str, message: str, **details: Any) -> None:
    findings.append(
        {
            "finding_id": f"s{slide}-{unit}-{relation}-{len(findings) + 1}",
            "slide_number": slide,
            "unit_id": unit,
            "relation": relation,
            "message": message,
            "details": details,
        }
    )


def validate_intent(intent: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(intent, dict):
        return ["intent plan root must be a JSON object"], warnings
    for field in sorted(REQUIRED_INTENT_ROOT_FIELDS - set(intent)):
        errors.append(f"root missing required field: {field}")
    if intent.get("target_medium") != "powerpoint":
        errors.append("target_medium must be powerpoint")
    threshold_profile = intent.get("threshold_profile")
    if not isinstance(threshold_profile, dict) or not threshold_profile.get("profile_id"):
        errors.append("threshold_profile.profile_id is required")
    slides = intent.get("slides")
    if not isinstance(slides, list):
        errors.append("slides must be an array")
        return errors, warnings
    seen_slides: set[int] = set()
    for slide_index, slide in enumerate(slides):
        if not isinstance(slide, dict):
            errors.append(f"slides[{slide_index}] must be an object")
            continue
        number = slide.get("slide_number")
        if not isinstance(number, int) or number < 1:
            errors.append(f"slides[{slide_index}].slide_number must be a positive integer")
            continue
        if number in seen_slides:
            errors.append(f"duplicate slide_number: {number}")
        seen_slides.add(number)
        units = slide.get("units")
        if not isinstance(units, list):
            errors.append(f"slide {number}: units must be an array")
            continue
        unit_ids = {unit.get("unit_id") for unit in units if isinstance(unit, dict) and unit.get("unit_id")}
        if len(unit_ids) != len([unit for unit in units if isinstance(unit, dict)]):
            errors.append(f"slide {number}: unit_id values must be present and unique")
        for unit_index, unit in enumerate(units):
            prefix = f"slide {number} unit[{unit_index}]"
            if not isinstance(unit, dict):
                errors.append(f"{prefix}: unit must be an object")
                continue
            unit_id = str(unit.get("unit_id") or unit_index)
            prefix = f"slide {number} unit {unit_id}"
            for field in sorted(REQUIRED_INTENT_UNIT_FIELDS - set(unit)):
                errors.append(f"{prefix}: missing required field {field}")
            if unit.get("slide_number") != number:
                errors.append(f"{prefix}: slide_number must equal containing slide_number")
            if unit.get("criticality") not in VALID_CRITICALITY:
                errors.append(f"{prefix}: invalid criticality")
            if unit.get("native_requirement") not in VALID_NATIVE_REQUIREMENT:
                errors.append(f"{prefix}: invalid native_requirement")
            if unit.get("expected_native_type") not in VALID_NATIVE_TYPE:
                errors.append(f"{prefix}: invalid expected_native_type")
            names = unit.get("planned_object_names")
            if not isinstance(names, list):
                errors.append(f"{prefix}: planned_object_names must be an array")
            elif unit.get("native_requirement") in {"required", "preferred"} and not names and not unit.get("planned_object_ids"):
                errors.append(f"{prefix}: eligible native unit needs a planned object name or id")
            if unit.get("native_requirement") == "raster_allowed" and not unit.get("raster_exception_reason"):
                errors.append(f"{prefix}: raster_allowed requires raster_exception_reason")
            relations = unit.get("required_relations")
            if not isinstance(relations, list):
                errors.append(f"{prefix}: required_relations must be an array")
                continue
            for relation_index, relation in enumerate(relations):
                relation_prefix = f"{prefix} relation[{relation_index}]"
                if not isinstance(relation, dict):
                    errors.append(f"{relation_prefix}: relation must be an object")
                    continue
                relation_type = relation.get("type")
                if relation_type not in VALID_RELATIONS:
                    errors.append(f"{relation_prefix}: unsupported relation type {relation_type}")
                if relation_type != "inside_safe_area" and not relation.get("with"):
                    errors.append(f"{relation_prefix}: with is required")
                elif relation.get("with") and relation.get("with") not in unit_ids:
                    errors.append(f"{relation_prefix}: with references missing unit {relation.get('with')}")
            for name in names or []:
                if re.fullmatch(r"(?i)(rectangle|text|shape|picture|group)\s*\d+", str(name).strip()):
                    warnings.append(f"{prefix}: generic object name is not semantic: {name}")
    overlap_exceptions = intent.get("overlap_exceptions", [])
    if not isinstance(overlap_exceptions, list):
        errors.append("overlap_exceptions must be an array when present")
    else:
        seen_exception_pairs: set[tuple[int, tuple[str, str]]] = set()
        for exception_index, exception in enumerate(overlap_exceptions):
            prefix = f"overlap_exceptions[{exception_index}]"
            if not isinstance(exception, dict):
                errors.append(f"{prefix} must be an object")
                continue
            slide_number = exception.get("slide_number")
            if not isinstance(slide_number, int) or slide_number not in seen_slides:
                errors.append(f"{prefix}.slide_number must refer to an intent slide")
            names = exception.get("object_names")
            if not isinstance(names, list) or len(names) != 2 or len({str(name).strip() for name in names}) != 2 or any(not str(name).strip() for name in names):
                errors.append(f"{prefix}.object_names must contain exactly two distinct, non-empty object names")
                continue
            if not isinstance(exception.get("reason"), str) or not exception["reason"].strip():
                errors.append(f"{prefix}.reason is required")
            key = (slide_number, overlap_exception_pair(str(names[0]), str(names[1])))
            if key in seen_exception_pairs:
                errors.append(f"{prefix} duplicates an earlier intentional text-overlap exception")
            seen_exception_pairs.add(key)
    if not isinstance(intent.get("waivers"), list):
        errors.append("waivers must be an array")
    return errors, warnings


def audit_with_intent(inventory: dict[str, Any], intent: dict[str, Any]) -> dict[str, Any]:
    thresholds = {**DEFAULT_THRESHOLDS, **(intent.get("threshold_profile") or {})}
    slide_width = inventory["slide_size_pt"]["width"]
    slide_height = inventory["slide_size_pt"]["height"]
    inventory_slides = {item["slide_number"]: item for item in inventory["slides"]}
    findings: list[dict[str, Any]] = []
    total_units = covered_units = 0
    critical_units = covered_critical_units = 0
    total_relations = passed_relations = 0
    critical_missing = critical_type_mismatch = critical_relation_missing = 0
    out_of_bounds = unintended_overlap = unplanned_text_overlap = detached_connectors = 0
    alignment_errors: list[float] = []
    spacing_deviations: list[float] = []
    raster_units = 0
    intentional_text_overlaps = intentional_text_overlap_pairs(intent)

    for slide_plan in intent.get("slides", []):
        number = int(slide_plan.get("slide_number", 0))
        slide = inventory_slides.get(number)
        units = slide_plan.get("units") or []
        if not slide:
            add_finding(findings, number, "slide", "missing_slide", "Intent plan refers to a missing slide")
            continue
        by_name = {item.get("name"): item for item in slide["objects"] if item.get("name")}
        by_id = {item.get("object_id"): item for item in slide["objects"] if item.get("object_id") is not None}
        unit_state: dict[str, dict[str, Any]] = {}
        for unit in units:
            names = unit.get("planned_object_names") or []
            ids = unit.get("planned_object_ids") or []
            objects = [by_name[name] for name in names if name in by_name]
            objects.extend(by_id[item_id] for item_id in ids if item_id in by_id and by_id[item_id] not in objects)
            unit_state[unit.get("unit_id", "unnamed")] = {
                "unit": unit,
                "objects": objects,
                "box": union_box(box for box in (box_from_object(item) for item in objects) if box),
                "relation_results": [],
            }

        for unit_id, state in unit_state.items():
            unit = state["unit"]
            objects = state["objects"]
            critical = unit.get("criticality") == "critical"
            requirement = unit.get("native_requirement", "required")
            eligible = requirement in {"required", "preferred"}
            if requirement == "raster_allowed":
                raster_units += 1
            if eligible:
                total_units += 1
                if critical:
                    critical_units += 1
            exists = bool(objects)
            expected = unit.get("expected_native_type", "any_native")
            matches = exists and all(type_matches(expected, item["type"]) for item in objects)
            if eligible and not exists:
                add_finding(findings, number, unit_id, "missing_object", "No planned PowerPoint object was found", planned_names=unit.get("planned_object_names", []))
                if critical:
                    critical_missing += 1
            elif eligible and not matches:
                add_finding(findings, number, unit_id, "object_type_mismatch", "Actual object type does not match intent", expected=expected, actual=[item["type"] for item in objects])
                if critical:
                    critical_type_mismatch += 1

            for relation in unit.get("required_relations") or []:
                total_relations += 1
                relation_type = relation.get("type", "unknown")
                passed = False
                details: dict[str, Any] = {}
                box = state["box"]
                target_state = unit_state.get(relation.get("with")) if relation.get("with") else None
                target_box = target_state.get("box") if target_state else None
                tolerance = float(relation.get("tolerance_pt", thresholds["alignment_tolerance_pt"]))

                if relation_type == "inside_safe_area" and box:
                    margin = float(relation.get("safe_margin_pt", thresholds["safe_margin_pt"]))
                    passed = box.x >= margin and box.y >= margin and box.right <= slide_width - margin and box.bottom <= slide_height - margin
                    details = {"safe_margin_pt": margin, "bbox": box.as_dict()}
                    if not passed:
                        out_of_bounds += 1
                elif relation_type in {"separate", "contain", "overlay"} and box and target_box:
                    ratio = overlap_ratio(box, target_box)
                    epsilon = float(relation.get("epsilon_ratio", thresholds["overlap_epsilon_ratio"]))
                    if relation_type == "separate":
                        passed = ratio <= epsilon
                        if not passed:
                            unintended_overlap += 1
                    elif relation_type == "contain":
                        passed = box.x <= target_box.x and box.y <= target_box.y and box.right >= target_box.right and box.bottom >= target_box.bottom
                    else:
                        passed = ratio > epsilon
                    details = {"overlap_ratio": q1(ratio), "epsilon_ratio": epsilon}
                elif relation_type.startswith("align_") and box and target_box:
                    edge = relation_type.removeprefix("align_")
                    values = {
                        "left": (box.x, target_box.x),
                        "right": (box.right, target_box.right),
                        "top": (box.y, target_box.y),
                        "bottom": (box.bottom, target_box.bottom),
                        "center_x": (box.center_x, target_box.center_x),
                        "center_y": (box.center_y, target_box.center_y),
                    }
                    if edge in values:
                        error = abs(values[edge][0] - values[edge][1])
                        alignment_errors.append(error)
                        passed = error <= tolerance
                        details = {"alignment_error_pt": q1(error), "tolerance_pt": tolerance}
                elif relation_type in {"horizontal_gap", "vertical_gap"} and box and target_box:
                    actual = horizontal_gap(box, target_box) if relation_type == "horizontal_gap" else vertical_gap(box, target_box)
                    target = float(relation.get("target_pt", 0.0))
                    if target:
                        deviation = abs(actual - target) / abs(target)
                        allowed = float(relation.get("tolerance_ratio", thresholds["spacing_tolerance_ratio"]))
                        passed = deviation <= allowed
                        details = {"actual_gap_pt": q1(actual), "target_gap_pt": target, "deviation_ratio": q1(deviation), "tolerance_ratio": allowed}
                    else:
                        deviation = abs(actual - target)
                        allowed = float(relation.get("tolerance_pt", thresholds["spacing_tolerance_pt_when_zero"]))
                        passed = deviation <= allowed
                        details = {"actual_gap_pt": q1(actual), "target_gap_pt": target, "absolute_deviation_pt": q1(deviation), "tolerance_pt": allowed}
                    spacing_deviations.append(deviation)
                elif relation_type == "connect":
                    connector_name = relation.get("connector")
                    connector = by_name.get(connector_name) if connector_name else (objects[0] if objects and objects[0]["type"] == "connector" else None)
                    target_ids = {item["object_id"] for item in (target_state or {}).get("objects", []) if item.get("object_id") is not None}
                    source_ids = {item["object_id"] for item in objects if item.get("object_id") is not None and item.get("type") != "connector"}
                    endpoint_ids = set(connector.get("connector_target_ids", [])) if connector else set()
                    passed = bool(connector and target_ids and endpoint_ids.intersection(target_ids))
                    if source_ids:
                        passed = passed and bool(endpoint_ids.intersection(source_ids))
                    details = {"connector": connector_name, "endpoint_ids": sorted(endpoint_ids), "target_ids": sorted(target_ids)}
                    if not passed:
                        detached_connectors += 1

                state["relation_results"].append(passed)
                if passed:
                    passed_relations += 1
                else:
                    if critical:
                        critical_relation_missing += 1
                    add_finding(findings, number, unit_id, relation_type, "Declared geometry/native relation did not pass or lacked supported evidence", **details)

            relations_pass = all(state["relation_results"]) if state["relation_results"] else True
            covered = eligible and exists and matches and relations_pass
            if covered:
                covered_units += 1
                if critical:
                    covered_critical_units += 1

        text_overlap_epsilon = float(thresholds["unplanned_text_overlap_epsilon_ratio"])
        slide_unplanned_text_overlap = 0
        text_objects = [
            item
            for item in slide["objects"]
            if item.get("type") == "text" and (box_from_object(item) is not None and box_from_object(item).area > 0)
        ]
        allowed_pairs = intentional_text_overlaps.get(number, set())
        for left_index, left in enumerate(text_objects):
            left_box = box_from_object(left)
            if left_box is None:
                continue
            for right in text_objects[left_index + 1:]:
                right_box = box_from_object(right)
                if right_box is None:
                    continue
                ratio = overlap_ratio(left_box, right_box)
                if ratio <= text_overlap_epsilon:
                    continue
                names = overlap_exception_pair(object_label(left), object_label(right))
                if names in allowed_pairs:
                    continue
                slide_unplanned_text_overlap += 1
                unplanned_text_overlap += 1
                add_finding(
                    findings,
                    number,
                    "unplanned_text_overlap",
                    "unplanned_text_overlap",
                    "Distinct native text objects overlap without an explicit, reasoned exception",
                    object_names=list(names),
                    object_ids=[left.get("object_id"), right.get("object_id")],
                    overlap_ratio=q1(ratio),
                    intersection_area_pt2=q1(intersection_area(left_box, right_box)),
                    epsilon_ratio=text_overlap_epsilon,
                )

        critical_read_order_mismatch = 0
        declared = [
            (int(state["unit"].get("reading_order")), unit_id, min((item["order"] for item in state["objects"]), default=math.inf))
            for unit_id, state in unit_state.items()
            if state["unit"].get("criticality") == "critical" and state["unit"].get("reading_order") is not None and state["objects"]
        ]
        expected_order = [item[1] for item in sorted(declared, key=lambda item: item[0])]
        actual_order = [item[1] for item in sorted(declared, key=lambda item: item[2])]
        for index, unit_id in enumerate(expected_order):
            if index >= len(actual_order) or actual_order[index] != unit_id:
                critical_read_order_mismatch += 1
                add_finding(findings, number, unit_id, "read_order_mismatch", "Critical declared reading order differs from top-level XML object order", expected=expected_order, actual=actual_order)
        slide["critical_read_order_mismatch_count"] = critical_read_order_mismatch
        slide["unplanned_text_overlap_count"] = slide_unplanned_text_overlap

    critical_read_order_total = sum(item.get("critical_read_order_mismatch_count", 0) for item in inventory["slides"])
    metrics = {
        "out_of_bounds_non_bleed_count": out_of_bounds,
        "unintended_overlap_count": unintended_overlap,
        "unplanned_text_overlap_count": unplanned_text_overlap,
        "max_alignment_error_pt": q1(max(alignment_errors)) if alignment_errors else "not_applicable",
        "max_spacing_deviation_ratio_or_pt": q1(max(spacing_deviations)) if spacing_deviations else "not_applicable",
        "detached_required_connector_count": detached_connectors,
        "object_density_per_slide": [
            {"slide_number": item["slide_number"], "objects_per_million_pt2": item["object_density_per_million_pt2"]}
            for item in inventory["slides"]
        ],
        "critical_native_missing_count": critical_missing,
        "critical_object_type_mismatch_count": critical_type_mismatch,
        "critical_required_relation_missing_count": critical_relation_missing,
        "critical_read_order_mismatch_count": critical_read_order_total,
        "geometry_constraint_coverage": ratio_or_na(passed_relations, total_relations),
        "native_unit_coverage": ratio_or_na(covered_units, total_units),
        "critical_native_coverage": ratio_or_na(covered_critical_units, critical_units),
        "required_relation_coverage": ratio_or_na(passed_relations, total_relations),
        "raster_exception_rate": ratio_or_na(raster_units, total_units + raster_units),
        "text_fit_risk_count": "not_run_unsupported_by_package_geometry",
        "confirmed_text_clipping_count": "requires_render_or_powerpoint_proof",
    }
    coverage_blockers = 0
    coverage_thresholds = (
        ("native_unit_coverage", "minimum_native_unit_coverage"),
        ("required_relation_coverage", "minimum_required_relation_coverage"),
    )
    for metric_name, threshold_name in coverage_thresholds:
        actual = metrics[metric_name]
        minimum = float(thresholds[threshold_name])
        if isinstance(actual, (int, float)) and actual < minimum:
            coverage_blockers += 1
            add_finding(
                findings,
                0,
                "coverage_gate",
                metric_name,
                "Observed coverage is below the declared minimum",
                actual=actual,
                minimum=minimum,
                threshold_name=threshold_name,
            )
    blockers = (
        out_of_bounds
        + unintended_overlap
        + unplanned_text_overlap
        + detached_connectors
        + critical_missing
        + critical_type_mismatch
        + critical_relation_missing
        + critical_read_order_total
        + coverage_blockers
    )
    return {
        "status": "pass_local" if blockers == 0 else "revise",
        "evidence_state": "observed_computation",
        "threshold_profile": thresholds,
        "metrics": metrics,
        "findings": findings,
        "claim_boundary": "This audit proves declared object, type, order, bounds, relation, and coverage observations only; it does not prove content fit, visual quality, edit-session success, or learner outcome.",
    }


def build_inventory(pptx_path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(pptx_path) as archive:
        width, height = slide_size(archive)
        paths = pptx_slide_paths(archive)
        slides = [parse_slide(archive, path, index, width, height) for index, path in enumerate(paths, start=1)]
    return {
        "pptx_path": str(pptx_path.resolve()),
        "pptx_sha256": sha256_file(pptx_path),
        "slide_size_pt": {"width": q1(width), "height": q1(height)},
        "slide_count": len(slides),
        "slides": slides,
    }


def run_audit(pptx_path: Path, intent_path: Path | None) -> dict[str, Any]:
    inventory = build_inventory(pptx_path)
    result: dict[str, Any] = {
        "contract_version": "1.0",
        "audit_tool": "visual-authoring/scripts/audit_pptx_native_objects.py",
        **inventory,
    }
    if intent_path is None:
        result.update(
            {
                "status": "blocked",
                "decision_code": "blocked_missing_intent_plan",
                "evidence_state": "observed_computation",
                "metrics": {"native_semantic_coverage": "not_run_missing_intent_plan"},
                "claim_boundary": "Inventory only. Without an intent plan, object count and geometry cannot establish semantic native quality.",
            }
        )
        return result
    intent = json.loads(intent_path.read_text(encoding="utf-8"))
    result["intent_plan_path"] = str(intent_path.resolve())
    result["intent_plan_sha256"] = sha256_file(intent_path)
    result["intent_content_sha256"] = sha256_json(intent)
    schema_errors, schema_warnings = validate_intent(intent)
    result["intent_schema_errors"] = schema_errors
    result["intent_schema_warnings"] = schema_warnings
    if schema_errors:
        result.update(
            {
                "status": "blocked",
                "decision_code": "blocked_invalid_intent_plan",
                "evidence_state": "observed_computation",
                "metrics": {"native_semantic_coverage": "not_run_invalid_intent_plan"},
                "claim_boundary": "Intent schema validation only. Geometry and semantic coverage were not run against an invalid plan.",
            }
        )
        return result
    result.update(audit_with_intent(inventory, intent))
    return result


def self_test() -> dict[str, Any]:
    a = Box(0, 0, 100, 100)
    b = Box(110, 0, 50, 100)
    c = Box(90, 0, 50, 50)
    inventory = {
        "slide_size_pt": {"width": 720.0, "height": 405.0},
        "slides": [
            {
                "slide_number": 1,
                "object_density_per_million_pt2": 6.9,
                "objects": [
                    {"object_id": 2, "name": "VA_TITLE", "type": "text", "order": 0, "bbox": {"x_pt": 40.0, "y_pt": 30.0, "w_pt": 300.0, "h_pt": 40.0}, "connector_target_ids": []},
                    {"object_id": 3, "name": "VA_BODY", "type": "text", "order": 1, "bbox": {"x_pt": 40.0, "y_pt": 100.0, "w_pt": 300.0, "h_pt": 180.0}, "connector_target_ids": []},
                ],
            }
        ],
    }
    intent = {
        "contract_version": "1.0",
        "target_medium": "powerpoint",
        "style_materialization": "pptx_theme",
        "threshold_profile": {"profile_id": "self-test-v1"},
        "slides": [
            {
                "slide_number": 1,
                "units": [
                    {
                        "unit_id": "title",
                        "slide_number": 1,
                        "semantic_role": "assertion",
                        "criticality": "critical",
                        "native_requirement": "required",
                        "expected_native_type": "text",
                        "planned_object_names": ["VA_TITLE"],
                        "edit_boundary": "text_and_position",
                        "group_name": None,
                        "z_order": 1,
                        "reading_order": 1,
                        "presentation_behavior": "always_visible",
                        "raster_exception_reason": None,
                        "required_relations": [
                            {"type": "inside_safe_area", "safe_margin_pt": 24},
                            {"type": "align_left", "with": "body", "tolerance_pt": 1},
                        ],
                    },
                    {
                        "unit_id": "body",
                        "slide_number": 1,
                        "semantic_role": "evidence",
                        "criticality": "critical",
                        "native_requirement": "required",
                        "expected_native_type": "text",
                        "planned_object_names": ["VA_BODY"],
                        "edit_boundary": "text_and_position",
                        "group_name": None,
                        "z_order": 2,
                        "reading_order": 2,
                        "presentation_behavior": "always_visible",
                        "raster_exception_reason": None,
                        "required_relations": [
                            {"type": "vertical_gap", "with": "title", "target_pt": 30, "tolerance_ratio": 0.01},
                        ],
                    },
                ],
            }
        ],
        "waivers": [],
    }
    schema_errors, schema_warnings = validate_intent(intent)
    intent_result = audit_with_intent(inventory, intent)
    overlap_inventory = copy.deepcopy(inventory)
    overlap_inventory["slides"][0]["objects"].append(
        {"object_id": 4, "name": "VA_CALLOUT", "type": "text", "order": 2, "bbox": {"x_pt": 80.0, "y_pt": 120.0, "w_pt": 220.0, "h_pt": 80.0}, "connector_target_ids": []}
    )
    unplanned_overlap_result = audit_with_intent(overlap_inventory, intent)
    waived_overlap_intent = copy.deepcopy(intent)
    waived_overlap_intent["overlap_exceptions"] = [
        {
            "slide_number": 1,
            "object_names": ["VA_BODY", "VA_CALLOUT"],
            "reason": "의도한 텍스트 겹침을 실험 fixture에서 명시한다.",
        }
    ]
    waived_overlap_errors, _ = validate_intent(waived_overlap_intent)
    waived_overlap_result = audit_with_intent(overlap_inventory, waived_overlap_intent)
    checks = {
        "horizontal_gap": horizontal_gap(a, b) == 10,
        "vertical_gap": vertical_gap(a, b) == 0,
        "separate_overlap": overlap_ratio(a, b) == 0,
        "positive_overlap": overlap_ratio(a, c) > 0,
        "union": union_box([a, b]) == Box(0, 0, 160, 100),
        "group_transform": Transform(2, 3, 10, 20).apply(Box(5, 4, 10, 2)) == Box(20, 32, 20, 6),
        "nested_group_transform": Transform(2, 2, 10, 10).compose(Transform(0.5, 0.5, 4, 6)) == Transform(1, 1, 18, 22),
        "native_type": type_matches("any_native", "shape") and not type_matches("any_native", "picture"),
        "zero_denominator": ratio_or_na(0, 0) == "not_applicable",
        "intent_schema": not schema_errors and not schema_warnings,
        "intent_audit_status": intent_result["status"] == "pass_local",
        "intent_native_coverage": intent_result["metrics"]["critical_native_coverage"] == 1.0,
        "intent_relation_coverage": intent_result["metrics"]["required_relation_coverage"] == 1.0,
        "intent_claim_boundary": "does not prove content fit" in intent_result["claim_boundary"],
        "unplanned_text_overlap_rejected": unplanned_overlap_result["status"] == "revise" and unplanned_overlap_result["metrics"]["unplanned_text_overlap_count"] == 1,
        "reasoned_text_overlap_exception": not waived_overlap_errors and waived_overlap_result["status"] == "pass_local" and waived_overlap_result["metrics"]["unplanned_text_overlap_count"] == 0,
    }
    failed = [name for name, passed in checks.items() if not passed]
    return {"status": "pass" if not failed else "fail", "checks": checks, "failed": failed}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pptx", type=Path, help="PPTX file to inspect")
    parser.add_argument("--intent", type=Path, help="native-object-intent-plan.json")
    parser.add_argument("--output", type=Path, help="Optional JSON output path; stdout is always available")
    parser.add_argument("--self-test", action="store_true", help="Run deterministic geometry helper tests")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.self_test:
        result = self_test()
    else:
        if not args.pptx:
            raise SystemExit("--pptx is required unless --self-test is used")
        result = run_audit(args.pptx, args.intent)
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if result.get("status") in {"pass", "pass_local"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
