#!/usr/bin/env python3
"""Validate the expression-family prototype authorization contract.

This validator proves that the authoring gate was explicitly completed. It
does not score beauty, content quality, comprehension, or learning outcomes.

Usage:
    python3 validate_authoring_prototype_gate.py manifest.json
    python3 validate_authoring_prototype_gate.py manifest.json --require-authorized
    python3 validate_authoring_prototype_gate.py --self-test
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

DECISION_STATUSES = {"pass_local", "revise", "blocked", "needs_human_choice"}
SOURCE_ROLES = {
    "reference_only",
    "baseline_to_recreate",
    "legacy_to_improve",
    "asset_pool",
    "evidence_source",
    "skipped_no_original",
}
FAMILY_FIELDS = {
    "family",
    "representative_slide",
    "content_job",
    "relationship",
    "chosen_expression",
    "choice_rationale",
    "rejected_alternative",
    "native_plan",
    "prototype_artifact",
    "review_status",
}
CONTENT_FIT_DIMENSIONS = [
    "content_task_action",
    "semantic_relationship_hierarchy",
    "medium_editability_intent",
    "geometry_accessibility_reproducibility",
    "render_package_native_open",
    "human_outcome_evidence",
]


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _path_exists(value: str, base: Path) -> bool:
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        candidate = base / candidate
    return candidate.exists()


def _resolve_path(value: str, base: Path) -> Path:
    candidate = Path(value).expanduser()
    return candidate if candidate.is_absolute() else base / candidate


def _normalized(value: str) -> str:
    return " ".join(value.casefold().split())


def validate_manifest(data: Any, base: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, dict):
        return {"status": "invalid", "authorized": False, "errors": ["manifest must be a JSON object"], "warnings": []}

    for field in ("version", "artifact_type", "fixed", "flexible", "format_gate", "content_fit_review", "decisional", "full_scale_authorized"):
        if field not in data:
            errors.append(f"missing top-level field: {field}")

    fixed = data.get("fixed")
    if not isinstance(fixed, dict):
        errors.append("fixed must be an object")
        fixed = {}
    for field in ("source_role", "reader_action_contract", "content_fit_hierarchy", "proof_surface_separation"):
        if field not in fixed:
            errors.append(f"fixed.{field} is required")
    if fixed.get("source_role") not in SOURCE_ROLES:
        errors.append(f"fixed.source_role must be one of {sorted(SOURCE_ROLES)}")
    if not _is_nonempty_string(fixed.get("reader_action_contract")):
        errors.append("fixed.reader_action_contract must be a non-empty string")
    for field in ("content_fit_hierarchy", "proof_surface_separation"):
        value = fixed.get(field)
        if not isinstance(value, list) or not value or not all(_is_nonempty_string(item) for item in value):
            errors.append(f"fixed.{field} must be a non-empty string list")
    if fixed.get("content_fit_hierarchy") != CONTENT_FIT_DIMENSIONS:
        errors.append(f"fixed.content_fit_hierarchy must equal canonical order: {CONTENT_FIT_DIMENSIONS}")

    flexible = data.get("flexible")
    if not isinstance(flexible, dict):
        errors.append("flexible must be an object")
        flexible = {}
    if not _is_nonempty_string(flexible.get("project_sot")):
        errors.append("flexible.project_sot must be a non-empty string")
    elif not _path_exists(flexible["project_sot"], base):
        errors.append(f"flexible.project_sot not found: {flexible['project_sot']}")
    families = flexible.get("expression_families")
    if not isinstance(families, list) or not families:
        errors.append("flexible.expression_families must be a non-empty list")
        families = []

    family_names: list[str] = []
    choice_rationales: list[str] = []
    rejected_alternatives: list[str] = []
    for index, family in enumerate(families):
        prefix = f"flexible.expression_families[{index}]"
        if not isinstance(family, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = sorted(FAMILY_FIELDS - set(family))
        for field in missing:
            errors.append(f"{prefix}.{field} is required")
        name = family.get("family")
        if not _is_nonempty_string(name):
            errors.append(f"{prefix}.family must be a non-empty string")
        else:
            family_names.append(name)
        slide_number = family.get("representative_slide")
        if not isinstance(slide_number, int) or slide_number < 1:
            errors.append(f"{prefix}.representative_slide must be a positive integer")
        for field in ("content_job", "relationship", "chosen_expression", "choice_rationale", "rejected_alternative", "native_plan", "prototype_artifact"):
            if not _is_nonempty_string(family.get(field)):
                errors.append(f"{prefix}.{field} must be a non-empty string")
        if _is_nonempty_string(family.get("choice_rationale")):
            choice_rationales.append(_normalized(family["choice_rationale"]))
        if _is_nonempty_string(family.get("rejected_alternative")):
            rejected_alternatives.append(_normalized(family["rejected_alternative"]))
        status = family.get("review_status")
        if status not in DECISION_STATUSES:
            errors.append(f"{prefix}.review_status must be one of {sorted(DECISION_STATUSES)}")
        artifact = family.get("prototype_artifact")
        if _is_nonempty_string(artifact) and not _path_exists(artifact, base):
            errors.append(f"{prefix}.prototype_artifact not found: {artifact}")

    duplicates = sorted({name for name in family_names if family_names.count(name) > 1})
    if duplicates:
        errors.append(f"duplicate expression families: {duplicates}")
    if len(families) > 1:
        duplicated_choice = sorted({value for value in choice_rationales if choice_rationales.count(value) > 1})
        duplicated_rejection = sorted({value for value in rejected_alternatives if rejected_alternatives.count(value) > 1})
        if duplicated_choice:
            errors.append("choice_rationale must be family-specific; duplicated rationale detected")
        if duplicated_rejection:
            errors.append("rejected_alternative must be family-specific; duplicated rationale detected")

    format_gate = data.get("format_gate")
    if not isinstance(format_gate, dict):
        errors.append("format_gate must be an object")
        format_gate = {}
    target_format = format_gate.get("target_format")
    if not _is_nonempty_string(target_format):
        errors.append("format_gate.target_format must be a non-empty string")
    for field in ("prototype_built", "render_reviewed"):
        if not isinstance(format_gate.get(field), bool):
            errors.append(f"format_gate.{field} must be boolean")
    fresh_open = format_gate.get("fresh_powerpoint_open")
    if target_format == "pptx":
        if not isinstance(fresh_open, dict):
            errors.append("format_gate.fresh_powerpoint_open is required for pptx")
            fresh_open = {}
        if not isinstance(fresh_open.get("no_recovery_dialog"), bool):
            errors.append("format_gate.fresh_powerpoint_open.no_recovery_dialog must be boolean")
        if not isinstance(fresh_open.get("slide_count"), int) or fresh_open.get("slide_count", -1) < 0:
            errors.append("format_gate.fresh_powerpoint_open.slide_count must be a non-negative integer")
        open_evidence = fresh_open.get("evidence_path")
        if not _is_nonempty_string(open_evidence):
            errors.append("format_gate.fresh_powerpoint_open.evidence_path must be a non-empty string")
        elif not _path_exists(open_evidence, base):
            errors.append(f"format_gate.fresh_powerpoint_open.evidence_path not found: {open_evidence}")
        elif _resolve_path(open_evidence, base).suffix.casefold() == ".json":
            try:
                open_record = json.loads(_resolve_path(open_evidence, base).read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"format_gate.fresh_powerpoint_open.evidence_path is not valid JSON: {exc}")
            else:
                if open_record.get("result") != "no_recovery_dialog":
                    errors.append("fresh PowerPoint open evidence must record result=no_recovery_dialog")
                if open_record.get("slide_count") != fresh_open.get("slide_count"):
                    errors.append("fresh PowerPoint open evidence slide_count conflicts with manifest")

    content_review = data.get("content_fit_review")
    if not isinstance(content_review, dict):
        errors.append("content_fit_review must be an object")
        content_review = {}
    if not isinstance(content_review.get("reviewed"), bool):
        errors.append("content_fit_review.reviewed must be boolean")
    if content_review.get("status") not in DECISION_STATUSES:
        errors.append(f"content_fit_review.status must be one of {sorted(DECISION_STATUSES)}")
    for field in ("reviewer_role", "review_method"):
        if not _is_nonempty_string(content_review.get(field)):
            errors.append(f"content_fit_review.{field} must be a non-empty string")
    if not _is_nonempty_string(content_review.get("evidence_path")):
        errors.append("content_fit_review.evidence_path must be a non-empty string")
    elif not _path_exists(content_review["evidence_path"], base):
        errors.append(f"content_fit_review.evidence_path not found: {content_review['evidence_path']}")

    decisional = data.get("decisional")
    if not isinstance(decisional, dict):
        errors.append("decisional must be an object")
        decisional = {}
    for field in ("fixed_rule", "flexible_evidence_path", "next_action"):
        if not _is_nonempty_string(decisional.get(field)):
            errors.append(f"decisional.{field} must be a non-empty string")
    if _is_nonempty_string(decisional.get("flexible_evidence_path")) and not _path_exists(decisional["flexible_evidence_path"], base):
        errors.append(f"decisional.flexible_evidence_path not found: {decisional['flexible_evidence_path']}")
    if decisional.get("status") not in DECISION_STATUSES:
        errors.append(f"decisional.status must be one of {sorted(DECISION_STATUSES)}")

    authorized = data.get("full_scale_authorized")
    if not isinstance(authorized, bool):
        errors.append("full_scale_authorized must be boolean")
        authorized = False

    authorization_conditions = {
        "all_expression_families_pass_local": bool(families) and all(isinstance(f, dict) and f.get("review_status") == "pass_local" for f in families),
        "prototype_built": format_gate.get("prototype_built") is True,
        "render_reviewed": format_gate.get("render_reviewed") is True,
        "content_fit_review_pass_local": content_review.get("reviewed") is True and content_review.get("status") == "pass_local",
        "decisional_pass_local": decisional.get("status") == "pass_local",
    }
    if target_format == "pptx":
        authorization_conditions["fresh_powerpoint_open"] = (
            isinstance(fresh_open, dict)
            and fresh_open.get("no_recovery_dialog") is True
            and isinstance(fresh_open.get("slide_count"), int)
            and fresh_open.get("slide_count", 0) > 0
        )

    if authorized:
        for condition, passed in authorization_conditions.items():
            if not passed:
                errors.append(f"full_scale_authorized=true conflicts with failed condition: {condition}")

    return {
        "status": "invalid" if errors else ("pass_local" if authorized else decisional.get("status", "revise")),
        "authorized": bool(authorized and not errors),
        "authorization_conditions": authorization_conditions,
        "family_count": len(families),
        "errors": errors,
        "warnings": warnings,
        "claim_boundary": "This result verifies gate completion only; it does not prove visual quality or human outcomes.",
    }


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="visual-authoring-gate-") as tmp:
        base = Path(tmp)
        (base / "project").mkdir()
        (base / "project/README.md").write_text("SoT\n", encoding="utf-8")
        (base / "prototype.png").write_bytes(b"png")
        (base / "review.md").write_text("content-fit review\n", encoding="utf-8")
        (base / "open.json").write_text(json.dumps({"result": "no_recovery_dialog", "slide_count": 1}), encoding="utf-8")
        valid = {
        "version": 1,
        "artifact_type": "slide_deck",
        "fixed": {
            "source_role": "legacy_to_improve",
            "reader_action_contract": "decide and act",
            "content_fit_hierarchy": CONTENT_FIT_DIMENSIONS,
            "proof_surface_separation": ["content_fit", "render", "native_open", "human_outcome"],
        },
        "flexible": {
            "project_sot": "project/README.md",
            "expression_families": [{
                "family": "process",
                "representative_slide": 1,
                "content_job": "show sequence",
                "relationship": "before to after",
                "chosen_expression": "two-lane flow",
                "choice_rationale": "A visible lane change makes the before-to-after relationship scannable.",
                "rejected_alternative": "generic cards hide sequence",
                "native_plan": "editable shapes and connectors",
                "prototype_artifact": "prototype.png",
                "review_status": "pass_local",
            }],
        },
        "format_gate": {
            "target_format": "pptx",
            "prototype_built": True,
            "render_reviewed": True,
            "fresh_powerpoint_open": {"no_recovery_dialog": True, "slide_count": 1, "evidence_path": "open.json"},
        },
        "content_fit_review": {"reviewed": True, "status": "pass_local", "reviewer_role": "author-reviewer", "review_method": "relationship and action review", "evidence_path": "review.md"},
        "decisional": {"status": "pass_local", "fixed_rule": "prototype before scale", "flexible_evidence_path": "review.md", "next_action": "scale"},
        "full_scale_authorized": True,
        }
        cases: list[tuple[str, dict[str, Any], bool]] = [("valid_manifest", valid, True)]
        invalid_status = json.loads(json.dumps(valid))
        invalid_status["flexible"]["expression_families"][0]["review_status"] = "revise"
        cases.append(("unauthorized_manifest", invalid_status, False))
        missing_evidence = json.loads(json.dumps(valid))
        missing_evidence["content_fit_review"]["evidence_path"] = "missing.md"
        cases.append(("missing_evidence", missing_evidence, False))
        bad_hierarchy = json.loads(json.dumps(valid))
        bad_hierarchy["fixed"]["content_fit_hierarchy"] = list(reversed(CONTENT_FIT_DIMENSIONS))
        cases.append(("bad_hierarchy", bad_hierarchy, False))
        generic_rationale = json.loads(json.dumps(valid))
        second = json.loads(json.dumps(generic_rationale["flexible"]["expression_families"][0]))
        second.update({"family": "comparison", "representative_slide": 2})
        generic_rationale["flexible"]["expression_families"].append(second)
        cases.append(("generic_duplicate_rationale", generic_rationale, False))

        failures = []
        for name, payload, should_authorize in cases:
            result = validate_manifest(payload, base)
            if result["authorized"] is not should_authorize:
                failures.append({"case": name, "result": result})
        if failures:
            print(json.dumps({"status": "fail", "failures": failures}, ensure_ascii=False, indent=2))
            return 1
        print(json.dumps({"status": "pass", "tests": len(cases), "claim_boundary": "gate structure and evidence traceability only"}, ensure_ascii=False, indent=2))
        return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path)
    parser.add_argument("--require-authorized", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.manifest is None:
        parser.error("manifest is required unless --self-test is used")
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "invalid", "authorized": False, "errors": [str(exc)], "warnings": []}, ensure_ascii=False, indent=2))
        return 1
    result = validate_manifest(data, args.manifest.resolve().parent)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["errors"]:
        return 1
    if args.require_authorized and not result["authorized"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
