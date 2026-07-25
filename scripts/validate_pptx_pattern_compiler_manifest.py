#!/usr/bin/env python3
"""Validate the fixed PPTX pattern-compiler manifest.

This validator checks the declared construction boundary and proof-surface
separation. It does not inspect a PPTX package or decide content quality.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

sys.dont_write_bytecode = True

EVIDENCE_STATES = {"not_run", "pass", "fail", "blocked_by_manual_action"}
SOURCE_ROLES = {"legacy_to_improve", "reference_benchmark", "no_original"}
READER_TASKS = {"compare", "trace", "decide", "locate", "practice", "explain", "other"}
REQUIRED_LEDGERS = {"structural_package", "reading_content", "viewing_render", "native_runtime"}
REQUIRED_TOP_LEVEL = {
    "schema_version", "source_family_id", "compiler_version", "target_medium",
    "canvas", "source_role", "recovery_lineage_policy", "prohibited_lineage",
    "patterns", "slides", "evidence_ledgers",
}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(data: Any) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return {"status": "invalid", "errors": ["manifest must be a JSON object"], "claim_boundary": "schema only"}

    for field in sorted(REQUIRED_TOP_LEVEL - set(data)):
        errors.append(f"missing top-level field: {field}")
    if data.get("schema_version") != "1.0":
        errors.append("schema_version must equal '1.0'")
    for field in ("source_family_id", "compiler_version"):
        if not nonempty(data.get(field)):
            errors.append(f"{field} must be a non-empty string")
    if data.get("target_medium") != "powerpoint":
        errors.append("target_medium must equal 'powerpoint'")
    if data.get("source_role") not in SOURCE_ROLES:
        errors.append(f"source_role must be one of {sorted(SOURCE_ROLES)}")
    if data.get("recovery_lineage_policy") != "reject_as_source":
        errors.append("recovery_lineage_policy must equal 'reject_as_source'")
    prohibited = data.get("prohibited_lineage")
    if not isinstance(prohibited, list) or not prohibited or not all(nonempty(item) for item in prohibited):
        errors.append("prohibited_lineage must be a non-empty string list")

    canvas = data.get("canvas")
    if not isinstance(canvas, dict):
        errors.append("canvas must be an object")
    else:
        if canvas.get("aspect_ratio") != "16:9":
            errors.append("canvas.aspect_ratio must equal '16:9'")
        if canvas.get("width_emu") != 12192000 or canvas.get("height_emu") != 6858000:
            errors.append("canvas must use 16:9 PowerPoint dimensions 12192000 x 6858000 EMU")

    patterns = data.get("patterns")
    pattern_ids: set[str] = set()
    if not isinstance(patterns, list) or not patterns:
        errors.append("patterns must be a non-empty list")
        patterns = []
    for index, pattern in enumerate(patterns):
        prefix = f"patterns[{index}]"
        if not isinstance(pattern, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in ("id", "semantic_job"):
            if not nonempty(pattern.get(field)):
                errors.append(f"{prefix}.{field} must be a non-empty string")
        pattern_id = pattern.get("id")
        if nonempty(pattern_id):
            if pattern_id in pattern_ids:
                errors.append(f"duplicate pattern id: {pattern_id}")
            pattern_ids.add(pattern_id)
        for field in ("native_types", "payload_fields"):
            value = pattern.get(field)
            if not isinstance(value, list) or not value or not all(nonempty(item) for item in value):
                errors.append(f"{prefix}.{field} must be a non-empty string list")

    slides = data.get("slides")
    slide_ids: set[str] = set()
    if not isinstance(slides, list) or not slides:
        errors.append("slides must be a non-empty list")
        slides = []
    for index, slide in enumerate(slides):
        prefix = f"slides[{index}]"
        if not isinstance(slide, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in ("slide_id", "pattern_id", "relationship_type", "source_claim", "pattern_choice_reason"):
            if not nonempty(slide.get(field)):
                errors.append(f"{prefix}.{field} must be a non-empty string")
        slide_id = slide.get("slide_id")
        if nonempty(slide_id):
            if slide_id in slide_ids:
                errors.append(f"duplicate slide_id: {slide_id}")
            slide_ids.add(slide_id)
        if nonempty(slide.get("pattern_id")) and slide["pattern_id"] not in pattern_ids:
            errors.append(f"{prefix}.pattern_id is not declared: {slide['pattern_id']}")
        if slide.get("reader_task") not in READER_TASKS:
            errors.append(f"{prefix}.reader_task must be one of {sorted(READER_TASKS)}")

    ledgers = data.get("evidence_ledgers")
    if not isinstance(ledgers, dict):
        errors.append("evidence_ledgers must be an object")
        ledgers = {}
    for ledger in sorted(REQUIRED_LEDGERS):
        if ledgers.get(ledger) not in EVIDENCE_STATES:
            errors.append(f"evidence_ledgers.{ledger} must be one of {sorted(EVIDENCE_STATES)}")
    if ledgers.get("native_runtime") == "pass":
        proof = data.get("native_runtime_proof")
        if not isinstance(proof, dict) or proof.get("no_recovery_dialog") is not True or not nonempty(proof.get("candidate_sha256")):
            errors.append("native_runtime=pass requires native_runtime_proof with no_recovery_dialog=true and candidate_sha256")

    return {
        "status": "invalid" if errors else "pass",
        "pattern_count": len(pattern_ids),
        "slide_count": len(slide_ids),
        "errors": errors,
        "claim_boundary": "This result verifies manifest structure and proof separation only; it does not prove PPTX runtime compatibility, content fit, visual quality, or learning outcomes.",
    }


def self_test() -> int:
    valid = {
        "schema_version": "1.0", "source_family_id": "fresh-v10", "compiler_version": "fixed-pattern-compiler-v1",
        "target_medium": "powerpoint", "canvas": {"aspect_ratio": "16:9", "width_emu": 12192000, "height_emu": 6858000},
        "source_role": "legacy_to_improve", "recovery_lineage_policy": "reject_as_source",
        "prohibited_lineage": ["candidate-v9.pptx"],
        "patterns": [{"id": "process_loop", "semantic_job": "trace a loop", "native_types": ["shape", "connector"], "payload_fields": ["title", "states"]}],
        "slides": [{"slide_id": "S11", "pattern_id": "process_loop", "reader_task": "trace", "relationship_type": "feedback_loop", "source_claim": "A loop has state and action.", "pattern_choice_reason": "A path makes the loop traceable."}],
        "evidence_ledgers": {"structural_package": "not_run", "reading_content": "pass", "viewing_render": "not_run", "native_runtime": "blocked_by_manual_action"},
    }
    bad = json.loads(json.dumps(valid))
    bad["slides"][0]["pattern_id"] = "undeclared"
    cases = [(valid, "pass"), (bad, "invalid")]
    results = [validate(payload) for payload, _ in cases]
    if any(result["status"] != expected for result, (_, expected) in zip(results, cases)):
        print(json.dumps({"status": "fail", "results": results}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"status": "pass", "tests": len(cases), "claim_boundary": "manifest schema only"}, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", help="path to manifest JSON")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.manifest:
        parser.error("manifest is required unless --self-test is used")
    try:
        with open(args.manifest, encoding="utf-8") as handle:
            result = validate(json.load(handle))
    except (OSError, json.JSONDecodeError) as exc:
        result = {"status": "invalid", "errors": [str(exc)], "claim_boundary": "schema only"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
