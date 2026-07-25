#!/usr/bin/env python3
"""Validate an exact-candidate PowerPoint native-runtime observation.

This tool does not open or control PowerPoint and does not mutate a PPTX.  It
computes an evidence status from a compiler-created gate plus an independently
recorded observation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any


BASELINE_CRITERIA = {
    "fresh_process",
    "exact_candidate",
    "no_recovery_dialog",
    "all_slides_reviewed",
}
FIRST_OPEN_CRITERIA = ("fresh_process", "exact_candidate", "no_recovery_dialog")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def resolve_candidate(gate: dict[str, Any], gate_path: Path) -> Path | None:
    candidate = gate.get("candidate")
    if not isinstance(candidate, str) or not candidate.strip():
        return None
    path = Path(candidate)
    return path if path.is_absolute() else (gate_path.parent / path).resolve()


def gate_errors(gate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    criteria = gate.get("acceptance_criteria")
    if not isinstance(criteria, list) or not criteria:
        return ["acceptance_criteria must be a non-empty list"]
    ids: list[str] = []
    for item in criteria:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            errors.append("each acceptance criterion needs a string id")
            continue
        ids.append(item["id"])
    duplicate_ids = sorted({item for item in ids if ids.count(item) > 1})
    if duplicate_ids:
        errors.append(f"duplicate criterion ids: {', '.join(duplicate_ids)}")
    missing = sorted(BASELINE_CRITERIA - set(ids))
    if missing:
        errors.append(f"missing baseline criteria: {', '.join(missing)}")
    required_by_id = {
        item["id"]: item.get("required", True)
        for item in criteria
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    optional_baseline = sorted(
        criterion_id
        for criterion_id in BASELINE_CRITERIA
        if required_by_id.get(criterion_id) is not True
    )
    if optional_baseline:
        errors.append(
            "baseline criteria must be required: " + ", ".join(optional_baseline)
        )
    if not isinstance(gate.get("candidate_sha256"), str) or len(gate["candidate_sha256"]) != 64:
        errors.append("candidate_sha256 must be a 64-character SHA-256 string")
    slide_count = gate.get("slide_count")
    if not isinstance(slide_count, int) or slide_count < 1:
        errors.append("slide_count must be a positive integer")
    template = gate.get("observation_template", {})
    if not isinstance(template, dict):
        errors.append("observation_template must be an object")
    for criterion_id in ids:
        if criterion_id.endswith("_edit_roundtrip"):
            expected = template.get(criterion_id) if isinstance(template, dict) else None
            if not isinstance(expected, dict) or not isinstance(expected.get("object_name"), str):
                errors.append(f"{criterion_id} needs observation_template.{criterion_id}.object_name")
    return errors


def check_criterion(
    criterion_id: str,
    gate: dict[str, Any],
    observation: dict[str, Any],
    candidate: Path | None,
) -> dict[str, Any]:
    if criterion_id == "fresh_process":
        return {"id": criterion_id, "passed": observation.get("opened_in_fresh_process") is True}
    if criterion_id == "exact_candidate":
        actual_sha = sha256_file(candidate) if candidate and candidate.is_file() else None
        return {
            "id": criterion_id,
            "passed": actual_sha == gate.get("candidate_sha256"),
            "expected_sha256": gate.get("candidate_sha256"),
            "actual_sha256": actual_sha,
        }
    if criterion_id == "no_recovery_dialog":
        return {"id": criterion_id, "passed": observation.get("recovery_dialog_visible") is False}
    if criterion_id == "all_slides_reviewed":
        expected = list(range(1, int(gate["slide_count"]) + 1))
        return {
            "id": criterion_id,
            "passed": observation.get("reviewed_slides") == expected,
            "expected_slides": expected,
            "reviewed_slides": observation.get("reviewed_slides"),
        }
    if criterion_id.endswith("_edit_roundtrip"):
        expected = gate["observation_template"][criterion_id]
        actual = observation.get(criterion_id, {})
        if not isinstance(actual, dict):
            actual = {}
        return {
            "id": criterion_id,
            "passed": (
                actual.get("object_name") == expected["object_name"]
                and bool(actual.get("saved_copy"))
                and actual.get("reopened_without_recovery") is True
            ),
            "expected_object_name": expected["object_name"],
            "actual_object_name": actual.get("object_name"),
            "saved_copy": actual.get("saved_copy"),
            "reopened_without_recovery": actual.get("reopened_without_recovery"),
        }
    return {"id": criterion_id, "passed": False, "error": "unsupported criterion id"}


def evaluate(gate: dict[str, Any], observation: dict[str, Any], gate_path: Path) -> dict[str, Any]:
    errors = gate_errors(gate)
    candidate = resolve_candidate(gate, gate_path)
    if candidate is None:
        errors.append("candidate path is missing")
    if errors:
        return {
            "schema_version": "1.0",
            "status": "blocked_invalid_gate",
            "gate_errors": errors,
            "claim_boundary": "No native-runtime conclusion is valid when the gate cannot bind the observation to an exact candidate.",
        }

    criteria = [item for item in gate["acceptance_criteria"] if item.get("required", True)]
    checks = [check_criterion(item["id"], gate, observation, candidate) for item in criteria]
    by_id = {item["id"]: item for item in checks}
    completed = all(item["passed"] for item in checks)
    recovery_failed = observation.get("recovery_dialog_visible") is True
    hash_failed = by_id["exact_candidate"]["passed"] is False
    roundtrip_failed = any(
        observation.get(item["id"], {}).get("reopened_without_recovery") is False
        for item in criteria
        if item["id"].endswith("_edit_roundtrip") and isinstance(observation.get(item["id"], {}), dict)
    )
    first_open_passed = all(by_id[item]["passed"] for item in FIRST_OPEN_CRITERIA)
    status = (
        "pass_native_runtime" if completed else
        "fail_native_runtime" if recovery_failed or hash_failed or roundtrip_failed else
        "pass_native_first_open_pending_release" if first_open_passed else
        "pending_native_observation"
    )
    return {
        "schema_version": "1.0",
        "status": status,
        "candidate": str(candidate),
        "candidate_sha256": by_id["exact_candidate"].get("actual_sha256"),
        "checks": checks,
        "observation": observation,
        "claim_boundary": (
            "This receipt validates a recorded exact-candidate native-runtime observation. "
            "It does not prove visual quality, accessibility, instructional quality, learner outcome, or distribution outcome."
        ),
    }


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def self_test() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        candidate = root / "candidate.pptx"
        candidate.write_bytes(b"native runtime receipt fixture")
        digest = sha256_file(candidate)
        gate = {
            "candidate": str(candidate),
            "candidate_sha256": digest,
            "slide_count": 2,
            "acceptance_criteria": [
                {"id": "fresh_process", "required": True},
                {"id": "exact_candidate", "required": True},
                {"id": "no_recovery_dialog", "required": True},
                {"id": "all_slides_reviewed", "required": True},
                {"id": "title_edit_roundtrip", "required": True},
            ],
            "observation_template": {
                "title_edit_roundtrip": {"object_name": "Title: S01"},
            },
        }
        complete = {
            "opened_in_fresh_process": True,
            "recovery_dialog_visible": False,
            "reviewed_slides": [1, 2],
            "title_edit_roundtrip": {
                "object_name": "Title: S01",
                "saved_copy": "candidate-edited.pptx",
                "reopened_without_recovery": True,
            },
        }
        first_open = {**complete, "reviewed_slides": [], "title_edit_roundtrip": {"object_name": "Title: S01", "saved_copy": None, "reopened_without_recovery": None}}
        recovery = {**first_open, "recovery_dialog_visible": True}
        invalid_gate = {
            **gate,
            "acceptance_criteria": [
                {"id": item["id"], "required": False if item["id"] == "all_slides_reviewed" else True}
                for item in gate["acceptance_criteria"]
            ],
        }
        statuses = [
            evaluate(gate, complete, root / "gate.json")["status"],
            evaluate(gate, first_open, root / "gate.json")["status"],
            evaluate(gate, recovery, root / "gate.json")["status"],
            evaluate(invalid_gate, complete, root / "gate.json")["status"],
        ]
        expected = [
            "pass_native_runtime",
            "pass_native_first_open_pending_release",
            "fail_native_runtime",
            "blocked_invalid_gate",
        ]
        if statuses != expected:
            raise AssertionError(f"expected {expected}, got {statuses}")
    print(json.dumps({"status": "pass", "tests": 4, "statuses": expected, "action_mode": "observation_only"}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate", type=Path)
    parser.add_argument("--observation", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not all((args.gate, args.observation, args.report)):
        parser.error("--gate, --observation, and --report are required unless --self-test is used")
    outcome = evaluate(read_json(args.gate), read_json(args.observation), args.gate)
    write_json(args.report, outcome)
    print(json.dumps(outcome, ensure_ascii=False, indent=2))
    return 0 if outcome["status"] in {"pass_native_runtime", "pass_native_first_open_pending_release"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
