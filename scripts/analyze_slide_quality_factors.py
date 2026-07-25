#!/usr/bin/env python3
"""Read-only PPTX cognitive-quality factor observation.

The script deliberately separates three things that are often collapsed into a
"slide quality score":

* package observations (text, objects, geometry, font declarations),
* a declared cognitive packet (reader task, relationship, grammar, scan path),
* optional human/LLM review codes.

It can compare a target deck with local reference decks, but references only
provide a distribution for structural proxies.  They are not a universal
quality leaderboard and do not prove visual appeal, comprehension, learning
transfer, or PowerPoint native-open behavior.

Inputs are read-only.  The only write target is --output-dir.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import statistics
import sys
import zipfile
from collections import Counter, defaultdict
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
SCHEMA_VERSION = "1.0"


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
    def area(self) -> float:
        return max(0.0, self.w) * max(0.0, self.h)


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


def q(value: float | None, digits: int = 3) -> float | None:
    return None if value is None else round(float(value), digits)


def json_default(value: object) -> object:
    """Serialize retained geometry records without losing audit traceability."""
    if isinstance(value, Box):
        return {"x": value.x, "y": value.y, "w": value.w, "h": value.h}
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def safe_ratio(numerator: float, denominator: float) -> float | None:
    return None if denominator <= 0 else numerator / denominator


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def presentation_slide_paths(archive: zipfile.ZipFile) -> list[str]:
    fallback = sorted(
        (name for name in archive.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml")),
        key=lambda name: int(name.rsplit("slide", 1)[-1].split(".", 1)[0]),
    )
    try:
        presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
        relationships = ET.fromstring(archive.read("ppt/_rels/presentation.xml.rels"))
    except (KeyError, ET.ParseError):
        return fallback
    rel_map = {
        rel.get("Id"): rel.get("Target")
        for rel in relationships.findall("pr:Relationship", NS)
        if rel.get("Id") and rel.get("Target")
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


def presentation_size(archive: zipfile.ZipFile) -> tuple[float, float]:
    root = ET.fromstring(archive.read("ppt/presentation.xml"))
    size = root.find("p:sldSz", NS)
    if size is None:
        raise ValueError("ppt/presentation.xml does not declare p:sldSz")
    return emu_to_pt(size.get("cx")), emu_to_pt(size.get("cy"))


def find_transform(node: ET.Element, kind: str) -> ET.Element | None:
    paths = {
        "sp": "p:spPr/a:xfrm",
        "pic": "p:spPr/a:xfrm",
        "cxnSp": "p:spPr/a:xfrm",
        "graphicFrame": "p:xfrm",
        "grpSp": "p:grpSpPr/a:xfrm",
    }
    return node.find(paths[kind], NS)


def parse_box(node: ET.Element, kind: str) -> Box | None:
    transform = find_transform(node, kind)
    if transform is None:
        return None
    offset = transform.find("a:off", NS)
    extent = transform.find("a:ext", NS)
    if offset is None or extent is None:
        return None
    return Box(
        emu_to_pt(offset.get("x")),
        emu_to_pt(offset.get("y")),
        emu_to_pt(extent.get("cx")),
        emu_to_pt(extent.get("cy")),
    )


def object_name(node: ET.Element, kind: str) -> str | None:
    paths = {
        "sp": "p:nvSpPr/p:cNvPr",
        "pic": "p:nvPicPr/p:cNvPr",
        "cxnSp": "p:nvCxnSpPr/p:cNvPr",
        "graphicFrame": "p:nvGraphicFramePr/p:cNvPr",
        "grpSp": "p:nvGrpSpPr/p:cNvPr",
    }
    props = node.find(paths[kind], NS)
    return props.get("name") if props is not None else None


def object_type(node: ET.Element, kind: str) -> str:
    if kind == "pic":
        return "picture"
    if kind == "cxnSp":
        return "connector"
    if kind == "grpSp":
        return "group"
    if kind == "graphicFrame":
        data = node.find("a:graphic/a:graphicData", NS)
        uri = data.get("uri", "") if data is not None else ""
        if uri == TABLE_URI:
            return "table"
        if uri == CHART_URI or "chart" in uri:
            return "chart"
        return "graphic_frame"
    return "shape"


def node_text(node: ET.Element) -> str:
    return "".join(piece.text or "" for piece in node.findall(".//a:t", NS)).strip()


def node_font_sizes(node: ET.Element) -> list[float]:
    sizes: list[float] = []
    for props in node.findall(".//a:rPr", NS) + node.findall(".//a:endParaRPr", NS):
        size = props.get("sz")
        if not size:
            continue
        try:
            sizes.append(float(size) / 100.0)
        except ValueError:
            continue
    return sizes


def node_paragraph_count(node: ET.Element) -> int:
    return len(node.findall(".//a:p", NS))


def node_bullet_count(node: ET.Element) -> int:
    count = 0
    for paragraph in node.findall(".//a:p", NS):
        props = paragraph.find("a:pPr", NS)
        if props is not None and any(local_name(child.tag).startswith("bu") for child in list(props)):
            count += 1
    return count


def union_area(boxes: Iterable[Box]) -> float:
    usable = [box for box in boxes if box.w > 0 and box.h > 0]
    if not usable:
        return 0.0
    x_values = sorted({box.x for box in usable} | {box.right for box in usable})
    total = 0.0
    for left, right in zip(x_values, x_values[1:]):
        if right <= left:
            continue
        intervals = sorted(
            (box.y, box.bottom)
            for box in usable
            if box.x < right and box.right > left
        )
        covered = 0.0
        current_start: float | None = None
        current_end: float | None = None
        for start, end in intervals:
            if current_start is None:
                current_start, current_end = start, end
            elif start > (current_end or start):
                covered += (current_end or start) - current_start
                current_start, current_end = start, end
            else:
                current_end = max(current_end or end, end)
        if current_start is not None and current_end is not None:
            covered += current_end - current_start
        total += (right - left) * covered
    return total


def alignment_cue_ratio(boxes: list[Box], tolerance_pt: float = 2.0) -> float | None:
    if len(boxes) < 2:
        return None
    edges: list[float] = []
    for box in boxes:
        edges.extend((box.x, box.right, box.y, box.bottom))
    if not edges:
        return None
    edges.sort()
    clustered = 0
    index = 0
    while index < len(edges):
        end = index + 1
        while end < len(edges) and edges[end] - edges[index] <= tolerance_pt:
            end += 1
        if end - index >= 2:
            clustered += end - index
        index = end
    return clustered / len(edges)


def parse_slide(root: ET.Element, slide_number: int, canvas: Box) -> dict[str, Any]:
    objects: list[dict[str, Any]] = []
    shape_tree = root.find("p:cSld/p:spTree", NS)
    if shape_tree is None:
        return {"slide_number": slide_number, "objects": [], "metrics": {}}
    for child in list(shape_tree):
        kind = local_name(child.tag)
        if kind not in {"sp", "pic", "cxnSp", "graphicFrame", "grpSp"}:
            continue
        box = parse_box(child, kind)
        if box is None:
            continue
        text = node_text(child)
        item = {
            "type": object_type(child, kind),
            "name": object_name(child, kind),
            "box": box,
            "text": text,
            "font_sizes": node_font_sizes(child),
            "paragraph_count": node_paragraph_count(child),
            "bullet_count": node_bullet_count(child),
        }
        item["is_background"] = not text and box.area >= canvas.area * 0.92
        objects.append(item)

    non_background = [item for item in objects if not item["is_background"]]
    text_objects = [item for item in non_background if item["text"]]
    nontext_objects = [item for item in non_background if not item["text"]]
    text_char_count = sum(len(item["text"].replace("\n", "")) for item in text_objects)
    text_area = sum(item["box"].area for item in text_objects)
    font_sizes = [size for item in text_objects for size in item["font_sizes"]]
    boxes = [item["box"] for item in non_background]
    focal_candidates = [item["box"].area for item in non_background if item["text"] or item["type"] in {"picture", "chart"}]
    title_candidates = [
        item
        for item in text_objects
        if item["box"].y <= canvas.h * 0.23 and len(item["text"]) <= 180
    ]
    title_font = max((max(item["font_sizes"]) for item in title_candidates if item["font_sizes"]), default=None)
    median_font = statistics.median(font_sizes) if font_sizes else None
    title_text = ""
    if title_candidates:
        title_text = max(
            title_candidates,
            key=lambda item: ((max(item["font_sizes"]) if item["font_sizes"] else 0), len(item["text"])),
        )["text"]
    metrics = {
        "object_count": len(non_background),
        "text_object_count": len(text_objects),
        "nontext_object_count": len(nontext_objects),
        "picture_count": sum(item["type"] == "picture" for item in non_background),
        "connector_count": sum(item["type"] == "connector" for item in non_background),
        "table_count": sum(item["type"] == "table" for item in non_background),
        "chart_count": sum(item["type"] == "chart" for item in non_background),
        "text_char_count": text_char_count,
        "paragraph_count": sum(item["paragraph_count"] for item in text_objects),
        "bullet_count": sum(item["bullet_count"] for item in text_objects),
        "text_area_ratio": safe_ratio(text_area, canvas.area),
        "text_density_chars_per_1000pt2": safe_ratio(text_char_count * 1000.0, text_area),
        "occupied_area_ratio": safe_ratio(union_area(boxes), canvas.area),
        "object_density_per_million_pt2": safe_ratio(len(non_background) * 1_000_000.0, canvas.area),
        "focal_box_ratio": safe_ratio(max(focal_candidates, default=0.0), canvas.area),
        "alignment_cue_ratio": alignment_cue_ratio(boxes),
        "min_font_pt": min(font_sizes) if font_sizes else None,
        "median_font_pt": median_font,
        "max_font_pt": max(font_sizes) if font_sizes else None,
        "font_tier_count": len({round(size, 1) for size in font_sizes}),
        "title_font_pt": title_font,
        "title_to_median_font_ratio": safe_ratio(title_font, median_font) if title_font else None,
        "title_text": title_text,
    }
    return {"slide_number": slide_number, "objects": non_background, "metrics": metrics}


def read_deck(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    with zipfile.ZipFile(path) as archive:
        width, height = presentation_size(archive)
        canvas = Box(0.0, 0.0, width, height)
        slides = []
        for slide_number, slide_path in enumerate(presentation_slide_paths(archive), start=1):
            slides.append(parse_slide(ET.fromstring(archive.read(slide_path)), slide_number, canvas))
    for record in slides:
        record["deck_label"] = label
    return {
        "label": label,
        "path": str(path),
        "sha256": sha256_file(path),
        "slide_count": len(slides),
        "canvas_pt": {"width": q(width), "height": q(height), "ratio": q(width / height if height else 0)},
        "slides": slides,
    }


def read_manifest(path: Path | None) -> tuple[dict[str, dict[str, Any]], dict[str, Any] | None]:
    if path is None:
        return {}, None
    raw = json.loads(path.read_text(encoding="utf-8"))
    items = raw.get("slides", raw if isinstance(raw, list) else [])
    mapping: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        raw_id = str(item.get("unit_id") or item.get("slide_id") or item.get("slide_number") or "")
        number = "".join(char for char in raw_id if char.isdigit())
        if number:
            mapping[str(int(number))] = item
    return mapping, {"path": str(path), "sha256": sha256_file(path), "schema_version": raw.get("schema_version")}


def read_review_codes(path: Path | None) -> tuple[dict[str, dict[str, Any]], dict[str, Any] | None]:
    if path is None:
        return {}, None
    raw = json.loads(path.read_text(encoding="utf-8"))
    items = raw.get("slides", raw if isinstance(raw, list) else [])
    mapping = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        raw_id = str(item.get("slide_id") or item.get("slide_number") or "")
        number = "".join(char for char in raw_id if char.isdigit())
        if number:
            mapping[str(int(number))] = item
    return mapping, {"path": str(path), "sha256": sha256_file(path)}


def quantile(values: list[float], value: float) -> float | None:
    if not values:
        return None
    sorted_values = sorted(values)
    if len(sorted_values) == 1:
        return 0.5
    below = sum(item < value for item in sorted_values)
    same = sum(item == value for item in sorted_values)
    return (below + max(0, same - 1) / 2.0) / (len(sorted_values) - 1)


def normalize(value: float | None, values: list[float], higher_is_better: bool = True) -> float | None:
    if value is None:
        return None
    rank = quantile(values, value)
    if rank is None:
        return None
    return rank if higher_is_better else 1.0 - rank


def slide_cognitive_proxy(record: dict[str, Any], manifest: dict[str, Any] | None, review: dict[str, Any] | None, target_values: dict[str, list[float]]) -> dict[str, Any]:
    metrics = record["metrics"]
    visual_declaration = 0
    if manifest:
        visual_declaration += int(bool(manifest.get("relationship_type")))
        visual_declaration += int(bool(manifest.get("selected_grammar")))
        visual_declaration += int(bool(manifest.get("reading_path")))
        visual_declaration += int(len(manifest.get("visible_cues") or []) >= 2)
    focus_inputs = [
        normalize(metrics.get("title_to_median_font_ratio"), target_values["title_to_median_font_ratio"]),
        normalize(metrics.get("focal_box_ratio"), target_values["focal_box_ratio"]),
        normalize(metrics.get("alignment_cue_ratio"), target_values["alignment_cue_ratio"]),
    ]
    load_inputs = [
        normalize(metrics.get("text_density_chars_per_1000pt2"), target_values["text_density_chars_per_1000pt2"], False),
        normalize(metrics.get("paragraph_count"), target_values["paragraph_count"], False),
        normalize(metrics.get("object_density_per_million_pt2"), target_values["object_density_per_million_pt2"], False),
        normalize(metrics.get("min_font_pt"), target_values["min_font_pt"]),
    ]
    def mean_available(values: list[float | None]) -> float | None:
        actual = [item for item in values if item is not None]
        return None if not actual else sum(actual) / len(actual)
    return {
        "focus_hierarchy_proxy_percentile": q(mean_available(focus_inputs), 3),
        "load_headroom_proxy_percentile": q(mean_available(load_inputs), 3),
        "relationship_encoding_declaration_count": visual_declaration if manifest else None,
        "reader_task": manifest.get("reader_task") if manifest else None,
        "relationship_type": manifest.get("relationship_type") if manifest else None,
        "selected_grammar": manifest.get("selected_grammar") if manifest else None,
        "reading_path_declared": bool(manifest.get("reading_path")) if manifest else None,
        "visible_cue_count": len(manifest.get("visible_cues") or []) if manifest else None,
        "review_codes": review or None,
    }


def pearson(values_a: list[float], values_b: list[float]) -> float | None:
    if len(values_a) < 3 or len(values_a) != len(values_b):
        return None
    mean_a, mean_b = statistics.mean(values_a), statistics.mean(values_b)
    centered_a = [item - mean_a for item in values_a]
    centered_b = [item - mean_b for item in values_b]
    denom = math.sqrt(sum(item * item for item in centered_a) * sum(item * item for item in centered_b))
    return None if denom == 0 else sum(a * b for a, b in zip(centered_a, centered_b)) / denom


def jacobi_eigen(matrix: list[list[float]], max_iterations: int = 100) -> tuple[list[float], list[list[float]]]:
    """Eigen decomposition for a small symmetric correlation matrix."""
    n = len(matrix)
    a = [row[:] for row in matrix]
    vectors = [[1.0 if row == col else 0.0 for col in range(n)] for row in range(n)]
    for _ in range(max_iterations * max(1, n * n)):
        p, r, maximum = 0, 1 if n > 1 else 0, 0.0
        for row in range(n):
            for col in range(row + 1, n):
                if abs(a[row][col]) > maximum:
                    p, r, maximum = row, col, abs(a[row][col])
        if maximum < 1e-10:
            break
        theta = 0.5 * math.atan2(2.0 * a[p][r], a[r][r] - a[p][p])
        cosine, sine = math.cos(theta), math.sin(theta)
        app, arr = a[p][p], a[r][r]
        a[p][p] = cosine * cosine * app - 2 * sine * cosine * a[p][r] + sine * sine * arr
        a[r][r] = sine * sine * app + 2 * sine * cosine * a[p][r] + cosine * cosine * arr
        a[p][r] = a[r][p] = 0.0
        for index in range(n):
            if index in {p, r}:
                continue
            aip, air = a[index][p], a[index][r]
            a[index][p] = a[p][index] = cosine * aip - sine * air
            a[index][r] = a[r][index] = sine * aip + cosine * air
        for index in range(n):
            vip, vir = vectors[index][p], vectors[index][r]
            vectors[index][p] = cosine * vip - sine * vir
            vectors[index][r] = sine * vip + cosine * vir
    values = [a[index][index] for index in range(n)]
    return values, vectors


def descriptive_pca(rows: list[dict[str, Any]]) -> dict[str, Any]:
    candidate_features = [
        "text_density_chars_per_1000pt2",
        "paragraph_count",
        "object_density_per_million_pt2",
        "occupied_area_ratio",
        "picture_count",
        "connector_count",
        "font_tier_count",
        "focal_box_ratio",
        "alignment_cue_ratio",
        "title_to_median_font_ratio",
    ]
    usable = []
    for feature in candidate_features:
        values = [row["metrics"].get(feature) for row in rows]
        numeric = [float(value) for value in values if isinstance(value, (int, float))]
        if len(numeric) >= max(8, int(len(rows) * 0.8)) and len(set(round(value, 8) for value in numeric)) > 1:
            usable.append(feature)
    if len(rows) < 8 or len(usable) < 2:
        return {"status": "not_run_insufficient_numeric_observations", "feature_count": len(usable), "slide_count": len(rows)}
    complete_rows = [row for row in rows if all(isinstance(row["metrics"].get(feature), (int, float)) for feature in usable)]
    if len(complete_rows) < max(8, len(usable) + 2):
        return {"status": "not_run_insufficient_complete_cases", "feature_count": len(usable), "complete_case_count": len(complete_rows)}
    series = [[float(row["metrics"][feature]) for row in complete_rows] for feature in usable]
    correlation = [[pearson(left, right) or 0.0 for right in series] for left in series]
    eigenvalues, eigenvectors = jacobi_eigen(correlation)
    ordering = sorted(range(len(eigenvalues)), key=lambda index: eigenvalues[index], reverse=True)
    total = sum(max(0.0, value) for value in eigenvalues) or 1.0
    axes = []
    for rank, index in enumerate(ordering[: min(3, len(ordering))], start=1):
        value = max(0.0, eigenvalues[index])
        loadings = {
            feature: q(eigenvectors[feature_index][index] * math.sqrt(value), 3)
            for feature_index, feature in enumerate(usable)
        }
        axes.append({
            "axis": rank,
            "eigenvalue": q(value),
            "explained_variance_ratio": q(value / total),
            "loadings": loadings,
            "interpretation_boundary": "Descriptive co-variation of package proxies only; this is not a validated cognitive or aesthetic quality factor.",
        })
    return {
        "status": "observed_descriptive_pca",
        "slide_count": len(rows),
        "complete_case_count": len(complete_rows),
        "features": usable,
        "correlation_matrix": {feature: {other: q(correlation[row_index][col_index]) for col_index, other in enumerate(usable)} for row_index, feature in enumerate(usable)},
        "axes": axes,
    }


def class_counts(records: list[dict[str, Any]], key: str) -> dict[str, int]:
    values = [str(record["cognitive"].get(key)) for record in records if record["cognitive"].get(key)]
    return dict(sorted(Counter(values).items()))


def target_vs_reference_structure(target: list[dict[str, Any]], references: list[dict[str, Any]]) -> dict[str, Any]:
    """Describe the target's structural position without ranking slide quality."""
    candidates = [
        "text_density_chars_per_1000pt2",
        "paragraph_count",
        "object_density_per_million_pt2",
        "occupied_area_ratio",
        "picture_count",
        "focal_box_ratio",
        "alignment_cue_ratio",
        "title_to_median_font_ratio",
    ]
    items: dict[str, Any] = {}
    for metric in candidates:
        target_values = [float(slide["metrics"][metric]) for slide in target if isinstance(slide["metrics"].get(metric), (int, float))]
        reference_values = [float(slide["metrics"][metric]) for slide in references if isinstance(slide["metrics"].get(metric), (int, float))]
        if not target_values or not reference_values:
            continue
        target_median = statistics.median(target_values)
        items[metric] = {
            "target_median": q(target_median),
            "reference_median": q(statistics.median(reference_values)),
            "target_median_reference_percentile": q(quantile(reference_values, target_median)),
            "target_slide_count": len(target_values),
            "reference_slide_count": len(reference_values),
        }
    return {
        "boundary": "A percentile locates the target median in this local, heterogeneous reference sample. It is not an indicator that higher or lower is better.",
        "metrics": items,
    }


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    fields = [
        "deck_label", "slide_number", "slide_id", "title_text", "object_count", "text_object_count", "picture_count",
        "connector_count", "table_count", "text_char_count", "paragraph_count", "bullet_count", "text_area_ratio",
        "text_density_chars_per_1000pt2", "occupied_area_ratio", "object_density_per_million_pt2", "focal_box_ratio",
        "alignment_cue_ratio", "min_font_pt", "median_font_pt", "max_font_pt", "font_tier_count", "title_font_pt",
        "title_to_median_font_ratio", "focus_hierarchy_proxy_percentile", "load_headroom_proxy_percentile",
        "relationship_encoding_declaration_count", "reader_task", "relationship_type", "selected_grammar", "reading_path_declared",
        "visible_cue_count", "manual_focus", "manual_load", "manual_relationship", "manual_transition", "manual_rhythm",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            metrics, cognitive = record["metrics"], record["cognitive"]
            review = cognitive.get("review_codes") or {}
            writer.writerow({
                "deck_label": record["deck_label"], "slide_number": record["slide_number"], "slide_id": record["slide_id"],
                **{field: metrics.get(field) for field in fields if field in metrics},
                **{field: cognitive.get(field) for field in fields if field in cognitive},
                "manual_focus": review.get("focus_hierarchy"), "manual_load": review.get("load_segmentation"),
                "manual_relationship": review.get("relational_encoding"), "manual_transition": review.get("guided_transition"),
                "manual_rhythm": review.get("deck_rhythm"),
            })


def score_label(value: float | None, high: str, middle: str, low: str) -> str:
    if value is None:
        return "not_observed"
    if value >= 0.67:
        return high
    if value <= 0.33:
        return low
    return middle


def markdown_report(analysis: dict[str, Any]) -> str:
    target = analysis["target"]
    records = target["slides"]
    pca = analysis["descriptive_pca"]
    lines = [
        "# Slide Quality Factor Observation",
        "",
        "## Judgment Boundary",
        "",
        "This is a cognitive-quality **diagnostic**, not a single quality score or a proof of aesthetic quality, comprehension, learning transfer, accessibility, or Microsoft PowerPoint native-open success. Package observations, declared cognitive structure, and optional human/LLM review codes remain separate.",
        "",
        "## Dataset",
        "",
        f"- Target: `{target['label']}` — {target['slide_count']} slides, SHA-256 `{target['sha256']}`.",
        f"- Local structural reference decks: {len(analysis['references'])} deck(s), {sum(deck['slide_count'] for deck in analysis['references'])} slides.",
        "- Reference decks establish descriptive proxy distributions only; their topic, audience, and visual strategy are not normalized.",
        "",
        "## Cognitive Factor Model",
        "",
        "| Factor | Fixed observations | Flexible cognitive judgment | Do not infer |",
        "| --- | --- | --- | --- |",
        "| Focus & hierarchy | declared font tiers, focal-box share, alignment cues | what should register first and whether it is visually dominant | aesthetic quality or comprehension |",
        "| Load & segmentation | text density, paragraph/object count, minimum declared font | whether the reader must integrate too many units at once | actual readability or learning burden |",
        "| Relational encoding | pictures/connectors/tables plus declared relation, grammar, cues | whether the visual grammar makes the required inference available | that an image or connector is explanatory |",
        "| Guided transition | declared reader task and reading path | whether explanation changes into a decision, practice, or transfer action | learner transfer |",
        "| Deck rhythm | silhouette family frequency and manual rhythm code | whether repetition is a stabilizing pattern or fatigue | engagement or pacing success |",
        "",
        "## Target Deck Observations",
        "",
        "| Slide | Focus proxy | Load headroom proxy | Relation declaration | Manual review signal |",
        "| --- | --- | --- | --- |",
    ]
    reference_summary = analysis["target_vs_reference_structural"]
    reference_lines = [
        "## Target Median in the Local Structural Sample",
        "",
        "The percentile below is a location in the heterogeneous local sample, not a better/worse direction.",
        "",
        "| Package proxy | Target median | Reference median | Target-median location in reference slides |",
        "| --- | ---: | ---: | ---: |",
    ]
    for metric, summary in reference_summary["metrics"].items():
        reference_lines.append(
            f"| {metric} | {summary['target_median']:.3f} | {summary['reference_median']:.3f} | {summary['target_median_reference_percentile']:.1%} |"
        )
    reference_lines.append("")
    lines[lines.index("## Cognitive Factor Model"):lines.index("## Cognitive Factor Model")] = reference_lines
    for record in records:
        cognitive = record["cognitive"]
        review = cognitive.get("review_codes") or {}
        lines.append(
            f"| {record['slide_id']} | {score_label(cognitive.get('focus_hierarchy_proxy_percentile'), 'higher within deck', 'middle within deck', 'lower within deck')} | "
            f"{score_label(cognitive.get('load_headroom_proxy_percentile'), 'more headroom within deck', 'middle within deck', 'less headroom within deck')} | "
            f"{cognitive.get('relationship_encoding_declaration_count') if cognitive.get('relationship_encoding_declaration_count') is not None else 'not declared'}/4 | "
            f"{review.get('overall_signal', 'not coded')} |"
        )
    lines.extend([
        "",
        "## Descriptive PCA",
        "",
        f"- Status: `{pca.get('status')}`.",
        "- The PCA is an exploratory co-variation view of package proxies. It does not validate the conceptual factors above.",
    ])
    if pca.get("status") == "observed_descriptive_pca":
        for axis in pca["axes"]:
            strongest = sorted(axis["loadings"].items(), key=lambda item: abs(item[1] or 0), reverse=True)[:3]
            labels = ", ".join(f"{name} ({value:+.3f})" for name, value in strongest)
            lines.append(f"- Axis {axis['axis']}: {axis['explained_variance_ratio']:.1%} variance; strongest loadings: {labels}.")
    lines.extend([
        "",
        "## Evidence States",
        "",
        "- structural_package: observed computation for the exact PPTX hashes listed above.",
        "- reading/cognitive: declared packet plus optional reviewer coding; it is a hypothesis about cognitive support, not an outcome measure.",
        "- viewing_render: not produced by this script; any referenced slide proxy must be reviewed separately.",
        "- native_runtime: not produced by this script.",
        "",
        "## Next Action",
        "",
        "Use lower-headroom or conditional-review slides as candidates for slide-scoped render review. Repair source structure or visual grammar, then rerun this observer; do not tune the deck merely to raise these proxy values.",
        "",
    ])
    return "\n".join(lines)


def build_svg(records: list[dict[str, Any]], output: Path) -> None:
    width, row_height, left = 1180, 28, 240
    height = 120 + row_height * len(records)
    columns = [("focus", "focus_hierarchy_proxy_percentile", "#2457d6"), ("headroom", "load_headroom_proxy_percentile", "#0f8f6b")]
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="#ffffff"/>', '<style>text { font-family: Arial, sans-serif; fill: #10233f; } .small { font-size: 13px; } .title { font-size: 20px; font-weight: 700; }</style>', '<text x="28" y="34" class="title">슬라이드 인지 프록시 — 덱 내부 상대 위치</text>', '<text x="28" y="60" class="small">점수는 절대 품질이 아니라 같은 덱 안의 구조적 관찰값 백분위입니다.</text>']
    for index, record in enumerate(records):
        y = 92 + index * row_height
        cognitive = record["cognitive"]
        lines.append(f'<text x="28" y="{y + 15}" class="small">{record["slide_id"]}</text>')
        for column_index, (label, key, color) in enumerate(columns):
            x = left + column_index * 430
            value = cognitive.get(key)
            lines.append(f'<text x="{x}" y="{y - 2}" class="small">{label}</text>')
            lines.append(f'<rect x="{x}" y="{y + 3}" width="330" height="14" rx="7" fill="#e8edf5"/>')
            if value is not None:
                lines.append(f'<rect x="{x}" y="{y + 3}" width="{max(3, value * 330):.1f}" height="14" rx="7" fill="{color}"/>')
                lines.append(f'<text x="{x + 340}" y="{y + 15}" class="small">{value:.2f}</text>')
    lines.append("</svg>")
    output.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only PPTX cognitive-quality factor observer.")
    parser.add_argument("--target", type=Path, required=True, help="Target PPTX; read only.")
    parser.add_argument("--target-label", default="target", help="Stable label used in reports.")
    parser.add_argument("--reference", type=Path, action="append", default=[], help="Optional local PPTX structural reference; repeatable and read only.")
    parser.add_argument("--cognitive-manifest", type=Path, help="Optional target visual-silhouette/cognitive packet JSON.")
    parser.add_argument("--review-codes", type=Path, help="Optional reviewer-code JSON; this is a declared judgment layer.")
    parser.add_argument("--output-dir", type=Path, required=True, help="New output directory. Existing nonempty directories are refused.")
    parser.add_argument("--force", action="store_true", help="Allow writing into an existing output directory.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.output_dir.exists() and any(args.output_dir.iterdir()) and not args.force:
        raise SystemExit(f"Output directory is not empty: {args.output_dir} (use --force to replace report files)")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    target = read_deck(args.target, args.target_label)
    references = [read_deck(path, path.stem) for path in args.reference]
    manifest_map, manifest_provenance = read_manifest(args.cognitive_manifest)
    review_map, review_provenance = read_review_codes(args.review_codes)

    target_metrics = defaultdict(list)
    for slide in target["slides"]:
        for metric, value in slide["metrics"].items():
            if isinstance(value, (int, float)):
                target_metrics[metric].append(float(value))
    records: list[dict[str, Any]] = []
    for deck in [target, *references]:
        for slide in deck["slides"]:
            number_key = str(slide["slide_number"])
            manifest = manifest_map.get(number_key) if deck is target else None
            review = review_map.get(number_key) if deck is target else None
            slide["slide_id"] = (manifest or review or {}).get("slide_id") or f"S{slide['slide_number']:02d}"
            slide["cognitive"] = slide_cognitive_proxy(slide, manifest, review, target_metrics) if deck is target else {}
            records.append(slide)
    target["slides"] = [record for record in records if record["deck_label"] == target["label"]]
    pca = descriptive_pca(records)
    reference_slides = [slide for deck in references for slide in deck["slides"]]
    analysis = {
        "schema_version": SCHEMA_VERSION,
        "evaluation_type": "cognitive_slide_quality_factor_observation",
        "status": "candidate_observed_package_plus_declared_cognitive_packet",
        "input_boundary": "All PPTX and JSON inputs were read only. The output directory is the only write surface.",
        "quality_claim_boundary": "No single quality score is produced. Structural comparisons are descriptive; cognitive codes are explicitly judgmental; neither proves rendered appearance, human comprehension, learning transfer, accessibility, or PowerPoint native-open behavior.",
        "target": target,
        "references": references,
        "cognitive_manifest": manifest_provenance,
        "review_codes": review_provenance,
        "descriptive_pca": pca,
        "target_vs_reference_structural": target_vs_reference_structure(target["slides"], reference_slides),
        "target_cognitive_distribution": {
            "reader_task": class_counts(target["slides"], "reader_task"),
            "relationship_type": class_counts(target["slides"], "relationship_type"),
            "selected_grammar": class_counts(target["slides"], "selected_grammar"),
        },
        "factor_model": {
            "focus_hierarchy": "focal signal must make the intended first inference available; package proxies are font tiers, focal box share, and alignment cues.",
            "load_segmentation": "the reader should not have to integrate too many textual or spatial units at once; proxies are text density, paragraph/object count, and declared font floor.",
            "relational_encoding": "the visual grammar should expose the required relationship; package counts are checked with declared relationship, grammar, cues, and scan path.",
            "guided_transition": "an explanatory slide should lead to the intended trace, choice, practice, or transfer action; reader task and scan path are declarations, not outcomes.",
            "deck_rhythm": "repetition may stabilize a teaching routine or cause fatigue; silhouette frequency and manual role coding require contextual judgment.",
        },
    }
    (args.output_dir / "analysis.json").write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2, default=json_default) + "\n",
        encoding="utf-8",
    )
    write_csv(args.output_dir / "slide-observations.csv", records)
    (args.output_dir / "factor-report.md").write_text(markdown_report(analysis), encoding="utf-8")
    build_svg(target["slides"], args.output_dir / "target-proxy-profile.svg")
    print(json.dumps({
        "status": analysis["status"],
        "target_slide_count": target["slide_count"],
        "reference_deck_count": len(references),
        "reference_slide_count": sum(deck["slide_count"] for deck in references),
        "output_dir": str(args.output_dir),
        "target_sha256": target["sha256"],
        "pca_status": pca["status"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, zipfile.BadZipFile, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
