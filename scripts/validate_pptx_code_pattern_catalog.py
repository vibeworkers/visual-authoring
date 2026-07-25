#!/usr/bin/env python3
"""Fail-closed validator for the PPTX code-pattern catalog.

This validator binds four surfaces before the emitter runs:

1. authored slide payload and renderer routing;
2. instructional scene patterns;
3. manifest layouts and OOXML capability decisions;
4. concrete source/report evidence paths.

It is deliberately structural.  It does not claim that a pattern is
pedagogically correct, visually effective, or compatible with native
PowerPoint.  Those decisions remain in their separate evidence ledgers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ALLOWED_CAPABILITY_STATUSES = {"used", "intentionally_not_used", "not_applicable"}
REQUIRED_LAYERS = {
    "instructional_scene",
    "native_object",
    "ooxml_capability",
    "verification_evidence",
}
REQUIRED_PRE_EMIT_GATES = {
    "catalog_binding",
    "reader_surface_admission",
    "ooxml_contract",
    "evidence_ledger_separation",
}
REQUIRED_FORBIDDEN_DECISIONS = {
    "raw_ooxml",
    "validation_status_override",
    "gateway_bypass",
    "evidence_ledger_status_override",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def get_path(data: dict[str, Any], dotted_path: str) -> Any:
    cursor: Any = data
    for part in dotted_path.split("."):
        if not isinstance(cursor, dict) or part not in cursor:
            raise KeyError(dotted_path)
        cursor = cursor[part]
    return cursor


def parse_source(source: str) -> tuple[list[dict[str, str]], dict[str, str], set[str]]:
    slide_specs = [
        {"slide_id": slide_id, "kind": kind}
        for slide_id, kind in re.findall(r"\{id:'(S\d{2})',\s*kind:'([^']+)'", source)
    ]
    routes = dict(
        re.findall(
            r"(?:if|else if)\(spec\.kind==='([^']+)'\)\s*(render[A-Za-z0-9_]+)\(slide,spec\)",
            source,
        )
    )
    functions = set(re.findall(r"^function\s+([A-Za-z0-9_]+)\s*\(", source, re.MULTILINE))
    return slide_specs, routes, functions


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a PPTX code-pattern catalog against its manifest and authored source."
    )
    parser.add_argument("catalog")
    parser.add_argument("manifest")
    parser.add_argument("source")
    parser.add_argument("report")
    args = parser.parse_args()

    catalog_path = Path(args.catalog).resolve()
    manifest_path = Path(args.manifest).resolve()
    source_path = Path(args.source).resolve()
    report_path = Path(args.report).resolve()
    base = catalog_path.parent

    findings: list[dict[str, str]] = []
    checks: list[dict[str, Any]] = []

    def fail(code: str, message: str) -> None:
        findings.append({"code": code, "message": message})

    def record(check_id: str, passed: bool, detail: Any) -> None:
        checks.append({"check_id": check_id, "passed": passed, "detail": detail})

    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        source = source_path.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        print(f"catalog input error: {exc}", file=sys.stderr)
        return 2

    source_slides, source_routes, source_functions = parse_source(source)
    source_slide_ids = [entry["slide_id"] for entry in source_slides]
    manifest_slide_ids = [entry.get("slide_id") for entry in manifest.get("slides", [])]

    family_match = catalog.get("source_family_id") == manifest.get("source_family_id")
    record(
        "source_family_match",
        family_match,
        {
            "catalog": catalog.get("source_family_id"),
            "manifest": manifest.get("source_family_id"),
        },
    )
    if not family_match:
        fail("SOURCE_FAMILY_MISMATCH", "catalog and manifest source_family_id values differ")

    layer_set = set(catalog.get("pattern_layers", []))
    layers_ok = REQUIRED_LAYERS.issubset(layer_set)
    record("required_pattern_layers", layers_ok, sorted(layer_set))
    if not layers_ok:
        fail("PATTERN_LAYER_MISSING", f"missing layers: {sorted(REQUIRED_LAYERS - layer_set)}")

    control = catalog.get("control_model", {})
    flexible_surface = control.get("flexible_decision_surface", {})
    fixed_surface = control.get("fixed_code_surface", {})
    control_ok = (
        control.get("mode") == "fixed_code_orchestrates_flexible_decisions"
        and flexible_surface.get("owner") in {"LLM_or_human_author", "human_or_LLM_author"}
        and REQUIRED_FORBIDDEN_DECISIONS.issubset(set(flexible_surface.get("forbidden", [])))
        and fixed_surface.get("owner") == "compiler_and_validators"
        and REQUIRED_PRE_EMIT_GATES.issubset(set(fixed_surface.get("required_pre_emit_gates", [])))
        and fixed_surface.get("write_condition") == "all_pre_emit_gates_pass"
    )
    record("fixed_code_control_model", control_ok, control)
    if not control_ok:
        fail(
            "FIXED_CODE_CONTROL_MODEL",
            "fixed code must own pre-emit gates and file writing; flexible decisions may not own raw OOXML or validation status",
        )

    declared_slide_count = catalog.get("authored_slide_count")
    source_order_ok = (
        bool(source_slide_ids)
        and source_slide_ids == manifest_slide_ids
        and (declared_slide_count is None or len(source_slide_ids) == declared_slide_count)
    )
    record(
        "authored_source_manifest_order",
        source_order_ok,
        {"source": source_slide_ids, "manifest": manifest_slide_ids},
    )
    if not source_order_ok:
        fail("SLIDE_ORDER_MISMATCH", "authored source and manifest must declare the same non-empty slide order and optional authored_slide_count")

    scene_patterns = catalog.get("scene_patterns", [])
    scene_ids = [pattern.get("id") for pattern in scene_patterns]
    scene_kinds = [pattern.get("kind") for pattern in scene_patterns]
    if len(scene_ids) != len(set(scene_ids)):
        fail("DUPLICATE_SCENE_PATTERN_ID", "scene pattern ids must be unique")
    if len(scene_kinds) != len(set(scene_kinds)):
        fail("DUPLICATE_SCENE_KIND", "each authored source kind must map to one scene pattern")

    source_kind_to_slides: dict[str, list[str]] = {}
    for entry in source_slides:
        source_kind_to_slides.setdefault(entry["kind"], []).append(entry["slide_id"])

    catalog_kind_to_pattern = {pattern.get("kind"): pattern for pattern in scene_patterns}
    missing_kinds = sorted(set(source_kind_to_slides) - set(catalog_kind_to_pattern))
    extra_kinds = sorted(set(catalog_kind_to_pattern) - set(source_kind_to_slides))
    kind_coverage_ok = not missing_kinds and not extra_kinds
    record(
        "scene_kind_coverage",
        kind_coverage_ok,
        {"missing": missing_kinds, "extra": extra_kinds},
    )
    if not kind_coverage_ok:
        fail("SCENE_KIND_COVERAGE", f"missing={missing_kinds}; extra={extra_kinds}")

    layout_map = manifest.get("slide_layout_map", {})
    catalog_slide_coverage: list[str] = []
    scene_route_failures: list[str] = []
    layout_failures: list[str] = []
    for kind, pattern in catalog_kind_to_pattern.items():
        declared_slides = pattern.get("slides", [])
        expected_slides = source_kind_to_slides.get(kind, [])
        catalog_slide_coverage.extend(declared_slides)
        renderer = pattern.get("renderer")
        if source_routes.get(kind) != renderer or renderer not in source_functions:
            scene_route_failures.append(
                f"{kind}: catalog={renderer}, route={source_routes.get(kind)}, function_exists={renderer in source_functions}"
            )
        if declared_slides != expected_slides:
            scene_route_failures.append(
                f"{kind}: catalog slides={declared_slides}, source slides={expected_slides}"
            )
        expected_layout = pattern.get("layout_family")
        for slide_id in declared_slides:
            if layout_map.get(slide_id) != expected_layout:
                layout_failures.append(
                    f"{slide_id}: catalog={expected_layout}, manifest={layout_map.get(slide_id)}"
                )

    route_ok = not scene_route_failures
    record("scene_renderer_routes", route_ok, scene_route_failures or "all routes bound")
    if not route_ok:
        fail("SCENE_ROUTE_MISMATCH", "; ".join(scene_route_failures))

    scene_slide_ok = sorted(catalog_slide_coverage) == sorted(source_slide_ids) and len(
        catalog_slide_coverage
    ) == len(set(catalog_slide_coverage))
    record("scene_slide_exact_coverage", scene_slide_ok, catalog_slide_coverage)
    if not scene_slide_ok:
        fail("SCENE_SLIDE_COVERAGE", "every authored slide must occur in exactly one scene pattern")

    layout_ok = not layout_failures
    record("scene_layout_binding", layout_ok, layout_failures or "all layouts bound")
    if not layout_ok:
        fail("LAYOUT_BINDING_MISMATCH", "; ".join(layout_failures))

    declared_pattern_ids = {pattern.get("id") for pattern in manifest.get("patterns", [])}
    used_pattern_ids = {slide.get("pattern_id") for slide in manifest.get("slides", [])}
    pattern_library_ok = used_pattern_ids.issubset(declared_pattern_ids) and declared_pattern_ids.issubset(
        used_pattern_ids
    )
    record(
        "manifest_pattern_library_usage",
        pattern_library_ok,
        {
            "declared": sorted(declared_pattern_ids),
            "used": sorted(used_pattern_ids),
        },
    )
    if not pattern_library_ok:
        fail("MANIFEST_PATTERN_LIBRARY_DRIFT", "declared pattern families and used slide pattern ids differ")

    capability_patterns = catalog.get("capability_patterns", [])
    capability_ids = [pattern.get("id") for pattern in capability_patterns]
    if len(capability_ids) != len(set(capability_ids)):
        fail("DUPLICATE_CAPABILITY_ID", "capability pattern ids must be unique")

    capability_failures: list[str] = []
    evidence_failures: list[str] = []
    for pattern in capability_patterns:
        pattern_id = pattern.get("id", "<missing-id>")
        status = pattern.get("status")
        evidence = pattern.get("evidence", [])
        reason = str(pattern.get("reason", "")).strip()
        if status not in ALLOWED_CAPABILITY_STATUSES:
            capability_failures.append(f"{pattern_id}: invalid status {status!r}")
        if not isinstance(evidence, list) or not evidence:
            capability_failures.append(f"{pattern_id}: evidence must be a non-empty list")
        if status != "used" and not reason:
            capability_failures.append(f"{pattern_id}: non-use status requires a reason")
        for entry in evidence if isinstance(evidence, list) else []:
            rel = entry.get("file")
            needle = entry.get("contains")
            evidence_path = (base / rel).resolve() if rel else None
            if not rel or not needle:
                evidence_failures.append(f"{pattern_id}: evidence requires file and contains")
                continue
            if evidence_path is None or not evidence_path.is_file():
                evidence_failures.append(f"{pattern_id}: missing evidence file {rel}")
                continue
            try:
                evidence_text = evidence_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                evidence_failures.append(f"{pattern_id}: evidence file is not UTF-8 text: {rel}")
                continue
            if needle not in evidence_text:
                evidence_failures.append(f"{pattern_id}: {rel} does not contain {needle!r}")

    capability_ok = not capability_failures
    evidence_ok = not evidence_failures
    record("capability_status_and_reason", capability_ok, capability_failures or "all classified")
    record("capability_source_evidence", evidence_ok, evidence_failures or "all evidence anchors found")
    if not capability_ok:
        fail("CAPABILITY_CLASSIFICATION", "; ".join(capability_failures))
    if not evidence_ok:
        fail("CAPABILITY_EVIDENCE", "; ".join(evidence_failures))

    contract_failures: list[str] = []
    for contract_path in catalog.get("required_manifest_contract_paths", []):
        try:
            value = get_path(manifest.get("ooxml_feature_contract", {}), contract_path)
            if value in (None, "", [], {}):
                contract_failures.append(f"{contract_path}: empty")
        except KeyError:
            contract_failures.append(f"{contract_path}: missing")
    contracts_ok = not contract_failures
    record("required_ooxml_contract_paths", contracts_ok, contract_failures or "all present")
    if not contracts_ok:
        fail("OOXML_CONTRACT_PATH", "; ".join(contract_failures))

    required_ledgers = {"structural_package", "reading_content", "viewing_render", "native_runtime"}
    ledger_keys = set(manifest.get("evidence_ledgers", {}))
    ledgers_ok = ledger_keys == required_ledgers
    record("four_evidence_ledgers", ledgers_ok, sorted(ledger_keys))
    if not ledgers_ok:
        fail("EVIDENCE_LEDGER_SET", f"expected={sorted(required_ledgers)}, actual={sorted(ledger_keys)}")

    report = {
        "schema_version": "1.0",
        "status": "pass_local" if not findings else "fail",
        "catalog_id": catalog.get("catalog_id"),
        "source_family_id": catalog.get("source_family_id"),
        "counts": {
            "authored_slides": len(source_slides),
            "source_kinds": len(source_kind_to_slides),
            "scene_patterns": len(scene_patterns),
            "capability_patterns": len(capability_patterns),
            "used_capabilities": sum(1 for item in capability_patterns if item.get("status") == "used"),
            "intentionally_not_used_capabilities": sum(
                1 for item in capability_patterns if item.get("status") == "intentionally_not_used"
            ),
            "not_applicable_capabilities": sum(
                1 for item in capability_patterns if item.get("status") == "not_applicable"
            ),
        },
        "hashes": {
            "catalog_sha256": sha256(catalog_path),
            "manifest_sha256": sha256(manifest_path),
            "source_sha256": sha256(source_path),
        },
        "checks": checks,
        "findings": findings,
        "claim_boundary": (
            "This report proves deterministic catalog-to-source-to-manifest binding and evidence-anchor presence only. "
            "It does not prove instructional quality, visual readability, OOXML runtime behavior, or native PowerPoint opening."
        ),
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
