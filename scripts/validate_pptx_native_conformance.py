#!/usr/bin/env python3
"""Validate a declarative PowerPoint-native conformance contract.

This tool deliberately *does not repair or rewrite a PPTX*.  It reads an exact
candidate package, compares it with the declared authoring contract, and emits
a source-level remediation plan.  A recovery-incident PPTX remains diagnostic
input only; the plan directs authors to amend their source and rebuild a fresh
source family.

The checks are structural PresentationML observations.  They do not prove that
Microsoft PowerPoint opened the file, that every object is pleasant to edit, or
that a reader understood the deck.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "p14": "http://schemas.microsoft.com/office/powerpoint/2010/main",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

CORE_CAPABILITIES = {
    "slide_master_layout_theme",
    "theme_font_scheme",
    "title_placeholder",
    "outline_navigation",
    "automatic_slide_number",
    "speaker_notes",
    "native_text_in_shapes",
    "editable_shapes",
    "connectors",
    "editable_tables",
    "editable_charts",
    "object_naming_reading_order",
    "accessibility",
    "hyperlinks_navigation",
    "animations_transitions",
    "media",
}
ALLOWED_CAPABILITY_STATUSES = {"used", "intentionally_not_used", "not_applicable"}
REQUIRED_INTENTIONAL_SETTINGS = {
    "slide_size",
    "theme_font",
    "slide_number",
    "text_frame_default",
    "outline_navigation",
}
GENERIC_OBJECT_NAME = re.compile(
    r"^(?:rectangle|rounded rectangle|text box|textbox|shape|picture|image|"
    r"line|connector|group|object)\s*\d*$",
    re.IGNORECASE,
)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def normalized_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip().casefold()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def xml_text(node: ET.Element | None) -> str:
    if node is None:
        return ""
    return "".join(node.itertext()).strip()


def pptx_slide_paths(archive: zipfile.ZipFile) -> list[str]:
    """Return slides in presentation order, with a numeric fallback."""

    fallback = sorted(
        (name for name in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)),
        key=lambda name: int(re.search(r"(\d+)\.xml$", name).group(1)),
    )
    try:
        presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
        relationships = ET.fromstring(archive.read("ppt/_rels/presentation.xml.rels"))
    except (KeyError, ET.ParseError):
        return fallback

    rel_map = {
        item.get("Id"): item.get("Target")
        for item in relationships.findall("pr:Relationship", NS)
        if item.get("Id") and item.get("Target")
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


def non_visual_name(node: ET.Element) -> str:
    candidate = node.find(".//p:cNvPr", NS)
    if candidate is None:
        return ""
    return (candidate.get("name") or "").strip()


def non_visual_description(node: ET.Element) -> str:
    candidate = node.find(".//p:cNvPr", NS)
    if candidate is None:
        return ""
    return (candidate.get("descr") or candidate.get("title") or "").strip()


def shape_is_title(node: ET.Element) -> bool:
    for placeholder in node.findall(".//p:ph", NS):
        if placeholder.get("type") in {"title", "ctrTitle"}:
            return True
    return False


def visible_paragraphs(text_body: ET.Element) -> list[dict[str, str | None]]:
    paragraphs: list[dict[str, str | None]] = []
    for paragraph in text_body.findall("a:p", NS):
        text = xml_text(paragraph)
        if not text:
            continue
        properties = paragraph.find("a:pPr", NS)
        paragraphs.append(
            {
                "text": text,
                "horizontal_alignment": properties.get("algn") if properties is not None else None,
            }
        )
    return paragraphs


def parse_slide(root: ET.Element, slide_number: int) -> dict[str, Any]:
    result: dict[str, Any] = {
        "titles": [],
        "all_text": [],
        "text_frames": [],
        "object_names": [],
        "pictures": [],
        "shape_count": 0,
        "connector_count": 0,
        "table_count": 0,
        "chart_count": 0,
        "group_count": 0,
        "hyperlink_count": 0,
        "timing_count": 0,
        "transition_count": 0,
        "media_count": 0,
    }
    for node in root.iter():
        if local_name(node.tag) == "tbl":
            result["table_count"] += 1
        elif local_name(node.tag) == "chart":
            result["chart_count"] += 1
        elif local_name(node.tag) in {"hlinkClick", "hlinkHover"}:
            result["hyperlink_count"] += 1
        elif local_name(node.tag) == "timing":
            result["timing_count"] += 1
        elif local_name(node.tag) == "transition":
            result["transition_count"] += 1
        elif local_name(node.tag) in {"audioFile", "videoFile", "media"}:
            result["media_count"] += 1

    for kind in ("sp", "pic", "cxnSp", "graphicFrame", "grpSp"):
        for index, node in enumerate(root.findall(f".//p:{kind}", NS), start=1):
            name = non_visual_name(node) or f"<unnamed:{slide_number}:{kind}:{index}>"
            result["object_names"].append(name)
            if kind == "sp":
                result["shape_count"] += 1
                text_body = node.find("p:txBody", NS)
                if text_body is None:
                    continue
                paragraphs = visible_paragraphs(text_body)
                if not paragraphs:
                    continue
                body_properties = text_body.find("a:bodyPr", NS)
                text_frame = {
                    "slide_number": slide_number,
                    "object_name": name,
                    "vertical_anchor": body_properties.get("anchor") if body_properties is not None else None,
                    "paragraphs": paragraphs,
                    "is_title": shape_is_title(node),
                }
                result["text_frames"].append(text_frame)
                text = " ".join(str(item["text"]) for item in paragraphs)
                result["all_text"].append(text)
                if text_frame["is_title"]:
                    result["titles"].append(text)
            elif kind == "pic":
                result["pictures"].append(
                    {
                        "slide_number": slide_number,
                        "object_name": name,
                        "description": non_visual_description(node),
                    }
                )
            elif kind == "cxnSp":
                result["connector_count"] += 1
            elif kind == "grpSp":
                result["group_count"] += 1
    return result


def parse_pptx(path: Path) -> dict[str, Any]:
    package_errors: list[str] = []
    observations: dict[str, Any] = {
        "pptx_sha256": sha256_file(path),
        "package_errors": package_errors,
        "slide_paths": [],
        "slides": [],
        "master_count": 0,
        "layout_count": 0,
        "theme_count": 0,
        "font_faces": {},
        "automatic_slide_number": False,
        "section_list_present": False,
        "notes_count": 0,
    }
    required_parts = {"[Content_Types].xml", "_rels/.rels", "ppt/presentation.xml", "ppt/_rels/presentation.xml.rels"}
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        missing = sorted(required_parts - names)
        if missing:
            package_errors.append(f"missing package parts: {', '.join(missing)}")
        observations["master_count"] = len([name for name in names if re.fullmatch(r"ppt/slideMasters/slideMaster\d+\.xml", name)])
        observations["layout_count"] = len([name for name in names if re.fullmatch(r"ppt/slideLayouts/slideLayout\d+\.xml", name)])
        observations["theme_count"] = len([name for name in names if re.fullmatch(r"ppt/theme/theme\d+\.xml", name)])
        observations["notes_count"] = len([name for name in names if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", name)])
        slide_paths = pptx_slide_paths(archive)
        observations["slide_paths"] = slide_paths

        try:
            presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
            observations["section_list_present"] = any(
                local_name(node.tag) == "sectionLst" for node in presentation.iter()
            )
        except (KeyError, ET.ParseError) as exc:
            package_errors.append(f"presentation parse failed: {exc}")

        for part in names:
            if not (
                re.fullmatch(r"ppt/slideMasters/slideMaster\d+\.xml", part)
                or re.fullmatch(r"ppt/slideLayouts/slideLayout\d+\.xml", part)
            ):
                continue
            try:
                root = ET.fromstring(archive.read(part))
            except ET.ParseError as exc:
                package_errors.append(f"{part} parse failed: {exc}")
                continue
            for node in root.iter():
                if local_name(node.tag) == "ph" and node.get("type") == "sldNum":
                    observations["automatic_slide_number"] = True
                if local_name(node.tag) == "hf" and (node.get("sldNum") or "").casefold() in {"1", "true"}:
                    observations["automatic_slide_number"] = True

        for part in sorted(name for name in names if re.fullmatch(r"ppt/theme/theme\d+\.xml", name)):
            try:
                theme = ET.fromstring(archive.read(part))
            except ET.ParseError as exc:
                package_errors.append(f"{part} parse failed: {exc}")
                continue
            scheme = theme.find(".//a:fontScheme", NS)
            if scheme is None:
                continue
            for group_name in ("majorFont", "minorFont"):
                group = scheme.find(f"a:{group_name}", NS)
                if group is None:
                    continue
                observations["font_faces"][group_name] = {
                    "latin": (group.find("a:latin", NS).get("typeface") if group.find("a:latin", NS) is not None else ""),
                    "east_asian": (group.find("a:ea", NS).get("typeface") if group.find("a:ea", NS) is not None else ""),
                }

        for slide_number, part in enumerate(slide_paths, start=1):
            try:
                slide = ET.fromstring(archive.read(part))
            except ET.ParseError as exc:
                package_errors.append(f"{part} parse failed: {exc}")
                continue
            parsed = parse_slide(slide, slide_number)
            for field in ("shape_count", "connector_count", "table_count", "chart_count", "group_count", "hyperlink_count", "timing_count", "transition_count", "media_count"):
                observations[field] = observations.get(field, 0) + parsed[field]
            for node in slide.iter():
                if local_name(node.tag) == "fld" and "slidenum" in (node.get("type") or "").casefold():
                    observations["automatic_slide_number"] = True
            observations["slides"].append(parsed)
    return observations


def finding(code: str, message: str, *, severity: str = "error", evidence: Any = None) -> dict[str, Any]:
    result: dict[str, Any] = {"code": code, "severity": severity, "message": message}
    if evidence is not None:
        result["evidence"] = evidence
    return result


def validate_contract(contract: Any) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if not isinstance(contract, dict):
        return [finding("CONTRACT_NOT_OBJECT", "contract root must be a JSON object")]
    for field in (
        "contract_version",
        "target_medium",
        "source_family_id",
        "source_lineage",
        "capability_catalog",
        "theme_font",
        "navigation",
        "slide_number",
        "text_frame_default",
        "intentional_settings",
        "raster_exceptions",
    ):
        if field not in contract:
            findings.append(finding("CONTRACT_REQUIRED_FIELD_MISSING", f"missing contract field: {field}"))
    if contract.get("target_medium") != "powerpoint":
        findings.append(finding("CONTRACT_TARGET_MEDIUM", "target_medium must be 'powerpoint'"))
    if not str(contract.get("source_family_id", "")).strip():
        findings.append(finding("CONTRACT_SOURCE_FAMILY", "source_family_id must be non-empty"))

    lineage = contract.get("source_lineage")
    if not isinstance(lineage, dict):
        findings.append(finding("CONTRACT_LINEAGE", "source_lineage must be an object"))
    else:
        if lineage.get("recovery_lineage_policy") != "reject_as_source":
            findings.append(
                finding(
                    "RECOVERY_LINEAGE_NOT_REJECTED",
                    "source_lineage.recovery_lineage_policy must be reject_as_source",
                )
            )
        if lineage.get("recovery_incident") is True:
            findings.append(
                finding(
                    "RECOVERY_INCIDENT_SOURCE_BLOCKED",
                    "a recovery-incident package cannot be the source of a new candidate",
                )
            )

    catalog = contract.get("capability_catalog")
    if not isinstance(catalog, list):
        findings.append(finding("CONTRACT_CAPABILITY_CATALOG", "capability_catalog must be a list"))
    else:
        ids = [item.get("id") for item in catalog if isinstance(item, dict)]
        if len(ids) != len(set(ids)):
            findings.append(finding("CONTRACT_CAPABILITY_DUPLICATE", "capability_catalog IDs must be unique"))
        missing = sorted(CORE_CAPABILITIES - set(ids))
        if missing:
            findings.append(
                finding(
                    "CONTRACT_CAPABILITY_COVERAGE",
                    "all core PowerPoint capabilities need an intentional status",
                    evidence={"missing": missing},
                )
            )
        for item in catalog:
            if not isinstance(item, dict):
                findings.append(finding("CONTRACT_CAPABILITY_ITEM", "each catalog entry must be an object"))
                continue
            status = item.get("status")
            if status not in ALLOWED_CAPABILITY_STATUSES:
                findings.append(
                    finding("CONTRACT_CAPABILITY_STATUS", f"{item.get('id')}: invalid status {status!r}")
                )
            if not str(item.get("decision_reason", "")).strip():
                findings.append(
                    finding(
                        "CONTRACT_CAPABILITY_REASON",
                        f"{item.get('id')}: every use and non-use decision needs decision_reason",
                    )
                )

    font = contract.get("theme_font")
    if not isinstance(font, dict):
        findings.append(finding("CONTRACT_THEME_FONT", "theme_font must be an object"))
    else:
        default = str(font.get("default_family", ""))
        if "pretendard" not in default.casefold():
            findings.append(
                finding("CONTRACT_DEFAULT_FONT", "theme_font.default_family must be a Pretendard family")
            )
        for field in ("latin_family", "east_asian_family"):
            if "pretendard" not in str(font.get(field, "")).casefold():
                findings.append(
                    finding("CONTRACT_THEME_FONT_FACE", f"theme_font.{field} must be a Pretendard family")
                )

    navigation = contract.get("navigation")
    if not isinstance(navigation, dict):
        findings.append(finding("CONTRACT_NAVIGATION", "navigation must be an object"))
    else:
        titles = navigation.get("title_sequence")
        if not isinstance(titles, list) or not titles:
            findings.append(finding("CONTRACT_TITLE_SEQUENCE", "navigation.title_sequence must be a non-empty list"))
        if not str(navigation.get("direction_statement", "")).strip():
            findings.append(
                finding(
                    "CONTRACT_DIRECTION_STATEMENT",
                    "navigation.direction_statement must say what the ordered title story is doing",
                )
            )
        if not isinstance(navigation.get("sections"), list) or not navigation.get("sections"):
            findings.append(finding("CONTRACT_SECTIONS", "navigation.sections must be a non-empty list"))
        if not isinstance(navigation.get("toc_entries"), list) or not navigation.get("toc_entries"):
            findings.append(finding("CONTRACT_TOC", "navigation.toc_entries must be a non-empty list"))

    slide_number = contract.get("slide_number")
    if not isinstance(slide_number, dict) or slide_number.get("mode") != "automatic_powerpoint":
        findings.append(
            finding(
                "CONTRACT_SLIDE_NUMBER",
                "slide_number.mode must be automatic_powerpoint; typed static numbers are not accepted",
            )
        )

    text_defaults = contract.get("text_frame_default")
    if not isinstance(text_defaults, dict):
        findings.append(finding("CONTRACT_TEXT_FRAME_DEFAULT", "text_frame_default must be an object"))
    else:
        if text_defaults.get("horizontal_alignment") != "center":
            findings.append(finding("CONTRACT_TEXT_HORIZONTAL_DEFAULT", "default horizontal alignment must be center"))
        if text_defaults.get("vertical_anchor") != "middle":
            findings.append(finding("CONTRACT_TEXT_VERTICAL_DEFAULT", "default vertical anchor must be middle"))
        if not isinstance(text_defaults.get("exceptions", []), list):
            findings.append(finding("CONTRACT_TEXT_EXCEPTIONS", "text_frame_default.exceptions must be a list"))

    settings = contract.get("intentional_settings")
    if not isinstance(settings, list):
        findings.append(finding("CONTRACT_INTENTIONAL_SETTINGS", "intentional_settings must be a list"))
    else:
        settings_by_id = {
            item.get("setting_id"): item
            for item in settings
            if isinstance(item, dict) and item.get("setting_id")
        }
        missing = sorted(REQUIRED_INTENTIONAL_SETTINGS - set(settings_by_id))
        if missing:
            findings.append(
                finding(
                    "CONTRACT_INTENTIONAL_SETTING_COVERAGE",
                    "each baseline setting needs an explicit value and reason",
                    evidence={"missing": missing},
                )
            )
        for setting_id, item in settings_by_id.items():
            if item.get("value") in (None, "", [], {}):
                findings.append(finding("CONTRACT_SETTING_VALUE", f"{setting_id}: value is required"))
            if not str(item.get("reason", "")).strip():
                findings.append(finding("CONTRACT_SETTING_REASON", f"{setting_id}: reason is required"))

    raster_exceptions = contract.get("raster_exceptions")
    if not isinstance(raster_exceptions, list):
        findings.append(finding("CONTRACT_RASTER_EXCEPTIONS", "raster_exceptions must be a list"))
    else:
        for item in raster_exceptions:
            if not isinstance(item, dict):
                findings.append(finding("CONTRACT_RASTER_EXCEPTION_ITEM", "each raster exception must be an object"))
                continue
            for field in ("object_name", "semantic_role", "reason", "equivalent_text"):
                if not str(item.get(field, "")).strip():
                    findings.append(
                        finding("CONTRACT_RASTER_EXCEPTION_FIELD", f"raster exception needs {field}")
                    )
    return findings


def catalog_by_id(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = contract.get("capability_catalog", [])
    return {item.get("id"): item for item in entries if isinstance(item, dict) and item.get("id")}


def contains_declared_family(actual: str, expected: str) -> bool:
    return normalized_text(expected) in normalized_text(actual)


def validate_observations(contract: dict[str, Any], observed: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for error in observed["package_errors"]:
        findings.append(finding("PACKAGE_STRUCTURE", error))
    catalog = catalog_by_id(contract)

    def is_used(capability_id: str) -> bool:
        return catalog.get(capability_id, {}).get("status") == "used"

    if is_used("slide_master_layout_theme") and not (
        observed["master_count"] and observed["layout_count"] and observed["theme_count"]
    ):
        findings.append(
            finding(
                "PPTX_MASTER_LAYOUT_THEME_MISSING",
                "used slide_master_layout_theme requires at least one master, layout, and theme",
                evidence={key: observed[key] for key in ("master_count", "layout_count", "theme_count")},
            )
        )

    if is_used("theme_font_scheme"):
        theme_font = contract["theme_font"]
        for group_name in ("majorFont", "minorFont"):
            actual = observed["font_faces"].get(group_name, {})
            for face, expected_key in (("latin", "latin_family"), ("east_asian", "east_asian_family")):
                if not contains_declared_family(actual.get(face, ""), str(theme_font.get(expected_key, ""))):
                    findings.append(
                        finding(
                            "PPTX_THEME_FONT_MISMATCH",
                            f"{group_name}.{face} must use {theme_font.get(expected_key)!r}",
                            evidence={"actual": actual.get(face, ""), "expected": theme_font.get(expected_key)},
                        )
                    )

    slides = observed["slides"]
    title_by_slide = {
        index: " ".join(slide["titles"]).strip()
        for index, slide in enumerate(slides, start=1)
    }
    if is_used("title_placeholder"):
        missing_titles = [number for number, text in title_by_slide.items() if not text]
        if missing_titles:
            findings.append(
                finding(
                    "PPTX_TITLE_PLACEHOLDER_MISSING",
                    "each slide needs a native title placeholder with visible text",
                    evidence={"slides": missing_titles},
                )
            )

    if is_used("automatic_slide_number") and not observed["automatic_slide_number"]:
        findings.append(
            finding(
                "PPTX_AUTOMATIC_SLIDE_NUMBER_MISSING",
                "use a native slide-number placeholder or field; do not type slide numbers as ordinary text",
            )
        )
    if is_used("speaker_notes") and observed["notes_count"] == 0:
        findings.append(finding("PPTX_SPEAKER_NOTES_MISSING", "speaker_notes is used but no notes slide part exists"))
    if is_used("native_text_in_shapes") and not any(slide["text_frames"] for slide in slides):
        findings.append(finding("PPTX_NATIVE_SHAPE_TEXT_MISSING", "native_text_in_shapes is used but no shape text was found"))
    if is_used("editable_shapes") and observed.get("shape_count", 0) == 0:
        findings.append(finding("PPTX_EDITABLE_SHAPES_MISSING", "editable_shapes is used but no native shape was found"))
    if is_used("connectors") and observed.get("connector_count", 0) == 0:
        findings.append(finding("PPTX_CONNECTORS_MISSING", "connectors is used but no connector was found"))
    if is_used("editable_tables") and observed.get("table_count", 0) == 0:
        findings.append(finding("PPTX_EDITABLE_TABLES_MISSING", "editable_tables is used but no native table was found"))
    if is_used("editable_charts") and observed.get("chart_count", 0) == 0:
        findings.append(finding("PPTX_EDITABLE_CHARTS_MISSING", "editable_charts is used but no native chart was found"))
    if is_used("hyperlinks_navigation") and observed.get("hyperlink_count", 0) == 0:
        findings.append(finding("PPTX_HYPERLINKS_MISSING", "hyperlinks_navigation is used but no native hyperlink was found"))
    if is_used("animations_transitions") and not (
        observed.get("timing_count", 0) or observed.get("transition_count", 0)
    ):
        findings.append(finding("PPTX_ANIMATION_TRANSITION_MISSING", "animations_transitions is used but none was found"))
    if is_used("media") and observed.get("media_count", 0) == 0:
        findings.append(finding("PPTX_MEDIA_MISSING", "media is used but no native media relationship was found"))

    if is_used("object_naming_reading_order"):
        generic_names = [
            name
            for slide in slides
            for name in slide["object_names"]
            if name.startswith("<unnamed:") or GENERIC_OBJECT_NAME.match(name)
        ]
        if generic_names:
            findings.append(
                finding(
                    "PPTX_SEMANTIC_OBJECT_NAME_MISSING",
                    "native objects need semantic Selection Pane names rather than generated names",
                    evidence={"objects": generic_names},
                )
            )

    if is_used("accessibility"):
        required_names = contract.get("accessibility", {}).get("required_object_names", [])
        if not isinstance(required_names, list) or not required_names:
            findings.append(
                finding(
                    "CONTRACT_ACCESSIBILITY_TARGETS",
                    "accessibility used requires accessibility.required_object_names",
                )
            )
        else:
            descriptions = {
                item["object_name"]: item["description"]
                for slide in slides
                for item in slide["pictures"]
            }
            missing = [name for name in required_names if not str(descriptions.get(name, "")).strip()]
            if missing:
                findings.append(
                    finding(
                        "PPTX_ACCESSIBILITY_DESCRIPTION_MISSING",
                        "required accessible objects need non-empty descriptions",
                        evidence={"objects": missing},
                    )
                )

    navigation = contract["navigation"]
    if is_used("outline_navigation"):
        if not observed["section_list_present"]:
            findings.append(
                finding(
                    "PPTX_NATIVE_SECTION_LIST_MISSING",
                    "outline_navigation requires a native PowerPoint section list in presentation.xml",
                )
            )
        sequence = navigation.get("title_sequence", [])
        actual_count = len(slides)
        if len(sequence) != actual_count:
            findings.append(
                finding(
                    "PPTX_TITLE_SEQUENCE_LENGTH",
                    "navigation.title_sequence must have one ordered title per actual slide",
                    evidence={"declared": len(sequence), "actual": actual_count},
                )
            )
        for expected_number, item in enumerate(sequence, start=1):
            if not isinstance(item, dict):
                findings.append(finding("PPTX_TITLE_SEQUENCE_ITEM", "title_sequence items must be objects"))
                continue
            number = item.get("slide_number")
            title = str(item.get("title", "")).strip()
            if number != expected_number or not title:
                findings.append(
                    finding(
                        "PPTX_TITLE_SEQUENCE_ORDER",
                        "title_sequence must be sequential, one-based, and non-empty",
                        evidence={"expected_slide_number": expected_number, "actual": number, "title": title},
                    )
                )
                continue
            if normalized_text(title) not in normalized_text(title_by_slide.get(number, "")):
                findings.append(
                    finding(
                        "PPTX_TITLE_SEQUENCE_MISMATCH",
                        "declared title story must match the native title placeholder text",
                        evidence={"slide_number": number, "declared": title, "observed": title_by_slide.get(number, "")},
                    )
                )
        section_starts = [item.get("start_slide") for item in navigation.get("sections", []) if isinstance(item, dict)]
        if section_starts != sorted(section_starts) or any(not isinstance(item, int) or item < 1 for item in section_starts):
            findings.append(
                finding(
                    "PPTX_SECTION_ORDER",
                    "navigation.sections must be ordered by valid start_slide values",
                    evidence={"start_slides": section_starts},
                )
            )
        for entry in navigation.get("toc_entries", []):
            if not isinstance(entry, dict):
                findings.append(finding("PPTX_TOC_ITEM", "toc_entries items must be objects"))
                continue
            toc_slide = entry.get("toc_slide_number")
            required_text = str(entry.get("section_title", "")).strip()
            all_text = " ".join(slides[toc_slide - 1]["all_text"]) if isinstance(toc_slide, int) and 0 < toc_slide <= len(slides) else ""
            if not required_text or normalized_text(required_text) not in normalized_text(all_text):
                findings.append(
                    finding(
                        "PPTX_TOC_ENTRY_MISSING",
                        "each declared table-of-contents entry must appear as native text on its TOC slide",
                        evidence={"toc_slide_number": toc_slide, "section_title": required_text},
                    )
                )

    exceptions = {
        item.get("object_name")
        for item in contract.get("text_frame_default", {}).get("exceptions", [])
        if isinstance(item, dict) and item.get("object_name")
    }
    known_shape_names = {frame["object_name"] for slide in slides for frame in slide["text_frames"]}
    unknown_exceptions = sorted(exceptions - known_shape_names)
    if unknown_exceptions:
        findings.append(
            finding(
                "PPTX_TEXT_EXCEPTION_UNKNOWN_OBJECT",
                "text alignment exception names must resolve to a native text shape",
                evidence={"objects": unknown_exceptions},
            )
        )
    for slide in slides:
        for frame in slide["text_frames"]:
            if frame["object_name"] in exceptions:
                continue
            if frame["vertical_anchor"] != "ctr":
                findings.append(
                    finding(
                        "PPTX_TEXT_VERTICAL_ALIGNMENT",
                        "shape text must default to middle vertical anchor (a:bodyPr@anchor=ctr)",
                        evidence={"slide": frame["slide_number"], "object": frame["object_name"], "actual": frame["vertical_anchor"]},
                    )
                )
            non_centered = [
                item["text"]
                for item in frame["paragraphs"]
                if item["horizontal_alignment"] != "ctr"
            ]
            if non_centered:
                findings.append(
                    finding(
                        "PPTX_TEXT_HORIZONTAL_ALIGNMENT",
                        "shape text must default to center alignment (a:pPr@algn=ctr)",
                        evidence={"slide": frame["slide_number"], "object": frame["object_name"], "paragraphs": non_centered},
                    )
                )

    declared_raster = {
        item.get("object_name"): item
        for item in contract.get("raster_exceptions", [])
        if isinstance(item, dict) and item.get("object_name")
    }
    actual_pictures = {item["object_name"]: item for slide in slides for item in slide["pictures"]}
    undeclared = sorted(set(actual_pictures) - set(declared_raster))
    if undeclared:
        findings.append(
            finding(
                "PPTX_UNDECLARED_RASTER_PICTURE",
                "every raster picture needs an explicit image exception with a semantic reason and equivalent text",
                evidence={"objects": undeclared},
            )
        )
    missing_raster_objects = sorted(set(declared_raster) - set(actual_pictures))
    if missing_raster_objects:
        findings.append(
            finding(
                "PPTX_RASTER_EXCEPTION_OBJECT_MISSING",
                "declared raster exception object was not found in the package",
                evidence={"objects": missing_raster_objects},
            )
        )
    return findings


REMEDIATION_ACTIONS = {
    "PPTX_MASTER_LAYOUT_THEME_MISSING": "Build master, layout, and theme parts from the source template before emitting slides.",
    "PPTX_THEME_FONT_MISMATCH": "Set major/minor Latin and East Asian theme fonts to the declared Pretendard family in the source builder.",
    "PPTX_TITLE_PLACEHOLDER_MISSING": "Emit a native title placeholder and visible title for every slide from the outline title sequence.",
    "PPTX_AUTOMATIC_SLIDE_NUMBER_MISSING": "Add a native slide-number placeholder or field at the master/layout level; remove manually typed page numbers.",
    "PPTX_NATIVE_SECTION_LIST_MISSING": "Generate the PowerPoint section list from navigation.sections rather than only drawing section labels.",
    "PPTX_TITLE_SEQUENCE_MISMATCH": "Update the outline and native title placeholders together so their ordered title story matches.",
    "PPTX_TITLE_SEQUENCE_LENGTH": "Regenerate navigation.title_sequence after slide insertion, deletion, or reorder.",
    "PPTX_TOC_ENTRY_MISSING": "Regenerate the native TOC text from the declared section sequence.",
    "PPTX_TEXT_VERTICAL_ALIGNMENT": "Set a:bodyPr@anchor to ctr for the affected source text shape, or declare a named exception with a reason.",
    "PPTX_TEXT_HORIZONTAL_ALIGNMENT": "Set a:pPr@algn to ctr for the affected source text shape, or declare a named exception with a reason.",
    "PPTX_UNDECLARED_RASTER_PICTURE": "Register the picture as a raster exception with semantic role, necessity, and equivalent native/accessible text; otherwise rebuild it as native objects.",
    "PPTX_RASTER_EXCEPTION_OBJECT_MISSING": "Remove stale raster exception entries or regenerate the declared image from source.",
    "PPTX_SEMANTIC_OBJECT_NAME_MISSING": "Assign stable semantic names in the source builder for the Selection Pane and reading order.",
    "RECOVERY_INCIDENT_SOURCE_BLOCKED": "Freeze the incident package. Start a new authored source family; do not ZIP-repair, convert, or resave it into release lineage.",
}


def make_repair_plan(status: str, contract: dict[str, Any], observed: dict[str, Any], findings: Iterable[dict[str, Any]]) -> dict[str, Any]:
    actions: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in findings:
        code = item["code"]
        if code in seen:
            continue
        seen.add(code)
        action = REMEDIATION_ACTIONS.get(
            code,
            "Amend the declarative source contract or source builder, then generate a fresh candidate and rerun this validator.",
        )
        actions.append(
            {
                "finding_code": code,
                "source_action": action,
                "forbidden_action": "Do not modify, normalize, convert, or resave the inspected PPTX as a repair strategy.",
            }
        )
    if status == "pass_local":
        actions.append(
            {
                "finding_code": "MANUAL_NATIVE_RUNTIME_REQUIRED",
                "source_action": "Open the exact validated hash in Microsoft PowerPoint and record the independent no-recovery result before release.",
                "forbidden_action": "Do not treat this XML/package result as native-runtime or human-outcome proof.",
            }
        )
    return {
        "schema_version": "1.0",
        "status": status,
        "source_mutation_only": True,
        "requires_fresh_source_family_when_rebuilding": status != "pass_local",
        "source_family_id": contract.get("source_family_id"),
        "candidate_pptx_sha256": observed.get("pptx_sha256"),
        "prohibited_repair_inputs": [
            "recovery-incident PPTX",
            "normalized PPTX",
            "converted PPTX",
            "PowerPoint UI-resaved incident PPTX",
        ],
        "actions": actions,
    }


def validate(pptx_path: Path, contract_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        report = {
            "schema_version": "1.0",
            "status": "blocked_missing_contract",
            "findings": [finding("CONTRACT_READ_ERROR", str(exc))],
            "claim_boundary": "No PPTX was altered. This state does not prove native runtime or human outcomes.",
        }
        return report, {"schema_version": "1.0", "status": "blocked_missing_contract", "actions": []}
    contract_findings = validate_contract(contract)
    try:
        observed = parse_pptx(pptx_path)
    except (OSError, zipfile.BadZipFile, ET.ParseError) as exc:
        observed = {"pptx_sha256": None, "package_errors": [str(exc)], "slides": []}
        package_findings = [finding("PPTX_READ_ERROR", str(exc))]
    else:
        package_findings = validate_observations(contract, observed) if not contract_findings else []

    all_findings = contract_findings + package_findings
    codes = {item["code"] for item in all_findings}
    if "RECOVERY_INCIDENT_SOURCE_BLOCKED" in codes:
        status = "blocked_recovery_incident"
    elif contract_findings:
        status = "blocked_missing_contract"
    elif all_findings:
        status = "repair_required"
    else:
        status = "pass_local"
    report = {
        "schema_version": "1.0",
        "status": status,
        "contract_path": str(contract_path.resolve()),
        "pptx_path": str(pptx_path.resolve()),
        "source_family_id": contract.get("source_family_id"),
        "observations": observed,
        "findings": all_findings,
        "manual_powerpoint_open": "not_run",
        "claim_boundary": (
            "This report proves declared native-conformance observations only. It does not prove a Microsoft PowerPoint open, "
            "edit-session success, visual quality, reader understanding, or behavior change."
        ),
    }
    return report, make_repair_plan(status, contract, observed, all_findings)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def contract_fixture() -> dict[str, Any]:
    return {
        "contract_version": "1.0",
        "target_medium": "powerpoint",
        "source_family_id": "native-conformance-fixture-v1",
        "source_lineage": {"recovery_lineage_policy": "reject_as_source", "recovery_incident": False},
        "capability_catalog": [
            {"id": "slide_master_layout_theme", "status": "used", "decision_reason": "repeatable deck structure"},
            {"id": "theme_font_scheme", "status": "used", "decision_reason": "default type must be controlled centrally"},
            {"id": "title_placeholder", "status": "used", "decision_reason": "outline and navigation need native titles"},
            {"id": "outline_navigation", "status": "used", "decision_reason": "read the title story and section path"},
            {"id": "automatic_slide_number", "status": "used", "decision_reason": "page location must follow PowerPoint convention"},
            {"id": "speaker_notes", "status": "intentionally_not_used", "decision_reason": "fixture has no facilitation script"},
            {"id": "native_text_in_shapes", "status": "used", "decision_reason": "text remains editable"},
            {"id": "editable_shapes", "status": "used", "decision_reason": "the fixture uses native title and TOC shapes"},
            {"id": "connectors", "status": "intentionally_not_used", "decision_reason": "no relation arrow is present"},
            {"id": "editable_tables", "status": "intentionally_not_used", "decision_reason": "no tabular data is present"},
            {"id": "editable_charts", "status": "intentionally_not_used", "decision_reason": "no quantitative data is present"},
            {"id": "object_naming_reading_order", "status": "used", "decision_reason": "objects need stable editing names"},
            {"id": "accessibility", "status": "intentionally_not_used", "decision_reason": "fixture has no image or non-text instructional object"},
            {"id": "hyperlinks_navigation", "status": "intentionally_not_used", "decision_reason": "fixture navigation is sequential"},
            {"id": "animations_transitions", "status": "intentionally_not_used", "decision_reason": "fixture has no staged reveal"},
            {"id": "media", "status": "intentionally_not_used", "decision_reason": "fixture has no audio or video"},
        ],
        "theme_font": {
            "default_family": "Pretendard Variable",
            "latin_family": "Pretendard Variable",
            "east_asian_family": "Pretendard Variable",
        },
        "navigation": {
            "direction_statement": "The title sequence moves from the purpose to the route through the deck.",
            "sections": [{"section_id": "opening", "title": "Opening", "start_slide": 1}],
            "title_sequence": [
                {"slide_number": 1, "title": "Start with the reader"},
                {"slide_number": 2, "title": "Follow the route"},
            ],
            "toc_entries": [{"toc_slide_number": 2, "section_title": "Opening"}],
        },
        "slide_number": {"mode": "automatic_powerpoint", "show_on_title_slide": False},
        "text_frame_default": {"horizontal_alignment": "center", "vertical_anchor": "middle", "exceptions": []},
        "intentional_settings": [
            {"setting_id": "slide_size", "value": "16:9", "reason": "presentation display target"},
            {"setting_id": "theme_font", "value": "Pretendard Variable", "reason": "Korean and Latin default"},
            {"setting_id": "slide_number", "value": "automatic_powerpoint", "reason": "native navigation"},
            {"setting_id": "text_frame_default", "value": "center/middle", "reason": "default shape text alignment"},
            {"setting_id": "outline_navigation", "value": "sections+TOC+title sequence", "reason": "ordered direction"},
        ],
        "raster_exceptions": [],
    }


def shape_xml(name: str, text: str, *, title: bool = False, vertical_anchor: str = "ctr", horizontal_alignment: str = "ctr") -> str:
    placeholder = '<p:ph type="title"/>' if title else ""
    return f"""
      <p:sp>
        <p:nvSpPr><p:cNvPr id="1" name="{name}"/><p:cNvSpPr txBox="1"/><p:nvPr>{placeholder}</p:nvPr></p:nvSpPr>
        <p:spPr/>
        <p:txBody><a:bodyPr anchor="{vertical_anchor}"/><a:lstStyle/><a:p><a:pPr algn="{horizontal_alignment}"/><a:r><a:t>{text}</a:t></a:r></a:p></p:txBody>
      </p:sp>
    """


def write_fixture_pptx(path: Path, *, vertical_anchor: str = "ctr") -> None:
    content_types = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/></Types>"""
    root_rels = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/></Relationships>"""
    presentation = """<?xml version="1.0" encoding="UTF-8"?>
<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst><p:sldId id="256" r:id="rId2"/><p:sldId id="257" r:id="rId3"/></p:sldIdLst><p:sldSz cx="12192000" cy="6858000"/><p14:sectionLst><p14:section id="1" name="Opening"><p14:sldIdLst><p14:sldId id="256"/><p14:sldId id="257"/></p14:sldIdLst></p14:section></p14:sectionLst></p:presentation>"""
    presentation_rels = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide2.xml"/></Relationships>"""
    master = """<?xml version="1.0" encoding="UTF-8"?>
<p:sldMaster xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><p:cSld><p:spTree><p:nvGrpSpPr/><p:grpSpPr/><p:sp><p:nvSpPr><p:cNvPr id="1" name="Master Slide Number"/><p:cNvSpPr/><p:nvPr><p:ph type="sldNum"/></p:nvPr></p:nvSpPr><p:spPr/></p:sp></p:spTree></p:cSld><p:sldLayoutIdLst><p:sldLayoutId id="1" r:id="rId1"/></p:sldLayoutIdLst><p:hf sldNum="1"/></p:sldMaster>"""
    master_rels = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>"""
    layout = """<?xml version="1.0" encoding="UTF-8"?>
<p:sldLayout xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr/><p:grpSpPr/><p:sp><p:nvSpPr><p:cNvPr id="1" name="Layout Title"/><p:cNvSpPr/><p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr><p:spPr/></p:sp></p:spTree></p:cSld></p:sldLayout>"""
    theme = """<?xml version="1.0" encoding="UTF-8"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Pretendard Theme"><a:themeElements><a:fontScheme name="Pretendard Variable"><a:majorFont><a:latin typeface="Pretendard Variable"/><a:ea typeface="Pretendard Variable"/></a:majorFont><a:minorFont><a:latin typeface="Pretendard Variable"/><a:ea typeface="Pretendard Variable"/></a:minorFont></a:fontScheme></a:themeElements></a:theme>"""
    slide1 = f"""<?xml version="1.0" encoding="UTF-8"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr/><p:grpSpPr/>{shape_xml('Title: Start with the reader', 'Start with the reader', title=True, vertical_anchor=vertical_anchor)}</p:spTree></p:cSld></p:sld>"""
    slide2 = f"""<?xml version="1.0" encoding="UTF-8"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr/><p:grpSpPr/>{shape_xml('Title: Follow the route', 'Follow the route', title=True)}{shape_xml('TOC: Opening', 'Opening')}</p:spTree></p:cSld></p:sld>"""
    slide_rel = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>"""
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        files = {
            "[Content_Types].xml": content_types,
            "_rels/.rels": root_rels,
            "ppt/presentation.xml": presentation,
            "ppt/_rels/presentation.xml.rels": presentation_rels,
            "ppt/slideMasters/slideMaster1.xml": master,
            "ppt/slideMasters/_rels/slideMaster1.xml.rels": master_rels,
            "ppt/slideLayouts/slideLayout1.xml": layout,
            "ppt/theme/theme1.xml": theme,
            "ppt/slides/slide1.xml": slide1,
            "ppt/slides/slide2.xml": slide2,
            "ppt/slides/_rels/slide1.xml.rels": slide_rel,
            "ppt/slides/_rels/slide2.xml.rels": slide_rel,
        }
        for name, content in files.items():
            archive.writestr(name, content)


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="pptx-native-conformance-") as directory:
        root = Path(directory)
        contract_path = root / "contract.json"
        valid_pptx = root / "valid.pptx"
        invalid_pptx = root / "invalid.pptx"
        write_json(contract_path, contract_fixture())
        write_fixture_pptx(valid_pptx)
        write_fixture_pptx(invalid_pptx, vertical_anchor="t")
        valid_report, _ = validate(valid_pptx, contract_path)
        invalid_report, invalid_plan = validate(invalid_pptx, contract_path)
        valid_ok = valid_report["status"] == "pass_local"
        invalid_codes = {item["code"] for item in invalid_report["findings"]}
        invalid_ok = invalid_report["status"] == "repair_required" and "PPTX_TEXT_VERTICAL_ALIGNMENT" in invalid_codes
        output = {
            "status": "pass_local" if valid_ok and invalid_ok else "fail",
            "valid_status": valid_report["status"],
            "invalid_status": invalid_report["status"],
            "invalid_codes": sorted(invalid_codes),
            "source_mutation_only": invalid_plan.get("source_mutation_only"),
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0 if valid_ok and invalid_ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pptx", type=Path, help="PPTX candidate to inspect")
    parser.add_argument("--contract", type=Path, help="pptx-native-conformance-contract.json")
    parser.add_argument("--report", type=Path, help="JSON report output")
    parser.add_argument("--repair-plan", type=Path, help="JSON source-level remediation plan output")
    parser.add_argument("--self-test", action="store_true", help="run synthetic valid and invalid package checks")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not all((args.pptx, args.contract, args.report, args.repair_plan)):
        parser.error("--pptx, --contract, --report, and --repair-plan are required unless --self-test is used")
    pptx_path = args.pptx.resolve()
    contract_path = args.contract.resolve()
    report_path = args.report.resolve()
    repair_path = args.repair_plan.resolve()
    if report_path == pptx_path or repair_path == pptx_path:
        parser.error("report and repair-plan must not overwrite the inspected PPTX")
    report, plan = validate(pptx_path, contract_path)
    write_json(report_path, report)
    write_json(repair_path, plan)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report.get("status") == "pass_local" else 1


if __name__ == "__main__":
    raise SystemExit(main())
