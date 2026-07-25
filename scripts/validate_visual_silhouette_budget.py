#!/usr/bin/env python3
"""Validate a project-declared semantic silhouette diversity budget."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


REQUIRED_POLICY = {
    "minimum_families",
    "max_consecutive_same",
    "dominant_family_cap",
    "semantic_visualization_target",
    "excluded_roles",
}
REQUIRED_SLIDE = {
    "slide",
    "role",
    "relationship_type",
    "silhouette_family",
    "semantic_visual",
    "semantic_visual_eligible",
    "diversity_exception",
}
REQUIRED_COGNITIVE = {
    "unit_id",
    "source_claim",
    "reader_task",
    "inference_goal",
    "candidate_grammars",
    "selected_grammar",
    "selection_reason",
    "visible_cues",
    "suppressed_cues",
    "reading_path",
    "evidence_state",
    "claim_boundary",
    "validation_boundary",
    "recovery_action",
}
REQUIRED_VALIDATION_BOUNDARY = {
    "technical_editability_proxy",
    "semantic_structure_proxy",
    "cognitive_readability_proxy",
    "human_outcome_validation",
}
EVIDENCE_STATES = {
    "observed_computation",
    "inferred_proxy",
    "calibrated_proxy",
    "human_outcome",
    "blocked_external",
}
CLAIM_BOUNDARIES = {"observable_proxy", "inferred_risk", "human_outcome_claim"}
PROXY_STATUSES = {"pass", "fail", "not_run", "not_applicable"}
HUMAN_STATUSES = {"pass", "fail", "not_run", "blocked_by_human_input"}


def fail(message: str) -> None:
    raise ValueError(message)


def require_nonempty_string(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(f"{field} must be a non-empty string")


def require_string_list(value: Any, field: str, *, allow_empty: bool = False) -> None:
    if not isinstance(value, list) or (not value and not allow_empty):
        fail(f"{field} must be a {'possibly empty ' if allow_empty else 'non-empty '}list")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        fail(f"{field} must contain only non-empty strings")


def validate_cognitive_slide(slide: dict[str, Any], index: int) -> None:
    missing = REQUIRED_COGNITIVE - set(slide)
    if missing:
        fail(f"slides[{index}] missing cognitive fields: {sorted(missing)}")
    for field in (
        "unit_id",
        "source_claim",
        "reader_task",
        "inference_goal",
        "selected_grammar",
        "selection_reason",
        "reading_path",
        "recovery_action",
    ):
        require_nonempty_string(slide[field], f"slides[{index}].{field}")
    require_string_list(slide["candidate_grammars"], f"slides[{index}].candidate_grammars")
    require_string_list(slide["visible_cues"], f"slides[{index}].visible_cues")
    require_string_list(
        slide["suppressed_cues"], f"slides[{index}].suppressed_cues", allow_empty=True
    )
    if slide["selected_grammar"] not in slide["candidate_grammars"]:
        fail(f"slides[{index}].selected_grammar must appear in candidate_grammars")
    if slide["evidence_state"] not in EVIDENCE_STATES:
        fail(f"slides[{index}].evidence_state must be one of {sorted(EVIDENCE_STATES)}")
    if slide["claim_boundary"] not in CLAIM_BOUNDARIES:
        fail(f"slides[{index}].claim_boundary must be one of {sorted(CLAIM_BOUNDARIES)}")
    boundary = slide["validation_boundary"]
    if not isinstance(boundary, dict):
        fail(f"slides[{index}].validation_boundary must be an object")
    missing_boundary = REQUIRED_VALIDATION_BOUNDARY - set(boundary)
    if missing_boundary:
        fail(f"slides[{index}].validation_boundary missing fields: {sorted(missing_boundary)}")
    for field in REQUIRED_VALIDATION_BOUNDARY - {"human_outcome_validation"}:
        if boundary[field] not in PROXY_STATUSES:
            fail(f"slides[{index}].validation_boundary.{field} has an invalid status")
    human_status = boundary["human_outcome_validation"]
    if human_status not in HUMAN_STATUSES:
        fail(f"slides[{index}].validation_boundary.human_outcome_validation has an invalid status")
    if human_status == "pass" and slide["evidence_state"] != "human_outcome":
        fail(f"slides[{index}] human outcome pass requires evidence_state=human_outcome")
    if slide["evidence_state"] == "human_outcome" and human_status != "pass":
        fail(f"slides[{index}] evidence_state=human_outcome requires human outcome pass")
    if slide["claim_boundary"] == "human_outcome_claim" and (
        slide["evidence_state"] != "human_outcome" or human_status != "pass"
    ):
        fail(f"slides[{index}] human_outcome_claim requires verified human outcome evidence")


def load_manifest(path: Path, *, require_cognitive_encoding: bool = False) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail("manifest must be a JSON object")
    if "policy" not in data or "slides" not in data:
        fail("manifest requires policy and slides")
    schema_version = int(data.get("schema_version", 1))
    if schema_version not in {1, 2}:
        fail("schema_version must be 1 or 2")
    if require_cognitive_encoding and schema_version < 2:
        fail("schema_version 2 is required for cognitive visual encoding")
    missing_policy = REQUIRED_POLICY - set(data["policy"])
    if missing_policy:
        fail(f"policy missing fields: {sorted(missing_policy)}")
    if not isinstance(data["slides"], list) or not data["slides"]:
        fail("slides must be a non-empty list")
    for index, slide in enumerate(data["slides"], start=1):
        if not isinstance(slide, dict):
            fail(f"slides[{index}] must be an object")
        missing_slide = REQUIRED_SLIDE - set(slide)
        if missing_slide:
            fail(f"slides[{index}] missing fields: {sorted(missing_slide)}")
        if schema_version >= 2:
            validate_cognitive_slide(slide, index)
    return data


def validate(data: dict[str, Any]) -> dict[str, Any]:
    schema_version = int(data.get("schema_version", 1))
    policy = data["policy"]
    slides = sorted(data["slides"], key=lambda item: item["slide"])
    numbers = [item["slide"] for item in slides]
    if numbers != list(range(1, len(slides) + 1)):
        fail("slide numbers must be consecutive and start at 1")

    minimum_families = int(policy["minimum_families"])
    max_consecutive_same = int(policy["max_consecutive_same"])
    dominant_family_cap = float(policy["dominant_family_cap"])
    semantic_target = float(policy["semantic_visualization_target"])
    excluded_roles = set(policy["excluded_roles"])
    if minimum_families < 1 or max_consecutive_same < 1:
        fail("minimum_families and max_consecutive_same must be positive")
    if not 0 < dominant_family_cap <= 1:
        fail("dominant_family_cap must be in (0, 1]")
    if not 0 <= semantic_target <= 1:
        fail("semantic_visualization_target must be in [0, 1]")

    eligible = [
        item
        for item in slides
        if item["role"] not in excluded_roles and not item["diversity_exception"]
    ]
    if not eligible:
        fail("no diversity-eligible slides remain after exclusions")

    family_counts = Counter(item["silhouette_family"] for item in eligible)
    dominant_family, dominant_count = family_counts.most_common(1)[0]
    dominant_share = dominant_count / len(eligible)

    longest_run = 0
    longest_family = None
    current_family = None
    current_run = 0
    for item in slides:
        if item["role"] in excluded_roles or item["diversity_exception"]:
            current_family = None
            current_run = 0
            continue
        family = item["silhouette_family"]
        if family == current_family:
            current_run += 1
        else:
            current_family = family
            current_run = 1
        if current_run > longest_run:
            longest_run = current_run
            longest_family = family

    semantic_eligible = [item for item in slides if item["semantic_visual_eligible"]]
    semantic_count = sum(bool(item["semantic_visual"]) for item in semantic_eligible)
    semantic_share = semantic_count / len(semantic_eligible) if semantic_eligible else 1.0

    checks = {
        "minimum_families": len(family_counts) >= minimum_families,
        "max_consecutive_same": longest_run <= max_consecutive_same,
        "dominant_family_cap": dominant_share <= dominant_family_cap,
        "semantic_visualization_target": semantic_share >= semantic_target,
        "cognitive_visual_encoding": schema_version >= 2,
    }
    pass_checks = dict(checks)
    if schema_version < 2:
        pass_checks.pop("cognitive_visual_encoding")
    return {
        "passed": all(pass_checks.values()),
        "schema_version": schema_version,
        "checks": checks,
        "observed": {
            "slide_count": len(slides),
            "diversity_eligible_count": len(eligible),
            "family_count": len(family_counts),
            "family_counts": dict(sorted(family_counts.items())),
            "dominant_family": dominant_family,
            "dominant_family_share": round(dominant_share, 4),
            "longest_consecutive_same": longest_run,
            "longest_consecutive_family": longest_family,
            "semantic_visual_eligible_count": len(semantic_eligible),
            "semantic_visual_count": semantic_count,
            "semantic_visualization_share": round(semantic_share, 4),
            "cognitive_encoded_slide_count": len(slides) if schema_version >= 2 else 0,
        },
        "policy": policy,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path, nargs="?")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-cognitive-encoding", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.manifest is None:
        parser.error("manifest is required unless --self-test is used")
    try:
        result = validate(
            load_manifest(
                args.manifest,
                require_cognitive_encoding=args.require_cognitive_encoding,
            )
        )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        result = {"passed": False, "error": str(error)}
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result.get("passed") else 1


def self_test() -> int:
    slide = {
        "slide": 1,
        "unit_id": "S01-U01",
        "source_claim": "경로를 파악한다",
        "reader_task": "locate",
        "role": "content",
        "relationship_type": "sequence",
        "inference_goal": "시작점과 도착점을 구분한다",
        "candidate_grammars": ["path", "staged_progression"],
        "selected_grammar": "path",
        "selection_reason": "방향과 도착점을 함께 보인다",
        "visible_cues": ["direction", "checkpoint"],
        "suppressed_cues": [],
        "reading_path": "left_to_right",
        "evidence_state": "inferred_proxy",
        "claim_boundary": "observable_proxy",
        "validation_boundary": {
            "technical_editability_proxy": "pass",
            "semantic_structure_proxy": "pass",
            "cognitive_readability_proxy": "not_run",
            "human_outcome_validation": "not_run",
        },
        "recovery_action": "방향 cue를 source에서 재설계",
        "silhouette_family": "path",
        "semantic_visual": True,
        "semantic_visual_eligible": True,
        "diversity_exception": None,
    }
    data = {
        "schema_version": 2,
        "policy": {
            "minimum_families": 1,
            "max_consecutive_same": 1,
            "dominant_family_cap": 1.0,
            "semantic_visualization_target": 1.0,
            "excluded_roles": [],
        },
        "slides": [slide],
    }
    valid = validate(data)
    if not valid["passed"] or valid["observed"]["cognitive_encoded_slide_count"] != 1:
        fail("self-test valid schema v2 fixture did not pass")
    invalid = json.loads(json.dumps(data))
    invalid["slides"][0]["validation_boundary"]["human_outcome_validation"] = "pass"
    try:
        validate_cognitive_slide(invalid["slides"][0], 1)
    except ValueError:
        print(json.dumps({"passed": True, "self_test": "ok"}, indent=2))
        return 0
    fail("self-test failed to reject unsupported human outcome pass")


if __name__ == "__main__":
    raise SystemExit(main())
