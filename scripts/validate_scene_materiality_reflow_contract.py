#!/usr/bin/env python3
"""Validate design-system lock, all-route scene packets, and localization reflow proof."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from pathlib import Path
from typing import Any


LOCK_STATES = {"locked", "not_applicable"}
SCENE_MODES = {"concrete_world", "operational_state", "abstract_relationship"}
ROUTE_STATUSES = {
    "SVG_ALLOWED",
    "ROUTED_IMAGE_REQUIRED",
    "INTEGRATED_HYBRID",
    "SVG_PROXY_ONLY",
    "BLOCKED_IMAGEGEN",
}
BLOCKING_ROUTE_STATUSES = {"SVG_PROXY_ONLY", "BLOCKED_IMAGEGEN"}
LOCALIZATION_STATES = {
    "not_applicable",
    "source_copy",
    "translated_pending_reflow",
    "concretized_pending_reflow",
    "reflow_verified",
}
BLOCKING_LOCALIZATION_STATES = {
    "translated_pending_reflow",
    "concretized_pending_reflow",
}
LOCK_FIELDS = (
    "lock_id",
    "token_style_namespace",
    "typography_hierarchy",
    "spacing_density",
    "component_grammar",
    "status_semantics",
    "accessibility_contrast",
)
SCENE_SCALAR_FIELDS = (
    "unit_id",
    "source_sentence",
    "artifact_role",
    "one_scene_statement",
    "action_or_state_change",
    "core_read_3s",
    "reader_inference_or_action",
    "semantic_boundary",
    "design_system_lock_ref",
    "selected_materiality_reason",
    "pattern_class",
    "recovery_action",
)
SCENE_LIST_FIELDS = (
    "concrete_entities",
    "visible_cue",
    "deterministic_meaning_items",
    "open_materiality_candidates",
)
REFLOW_SCALAR_FIELDS = (
    "unit_id",
    "language_owner",
    "source_phrase",
    "rendered_phrase",
    "recovery_action",
)
REFLOW_LIST_FIELDS = (
    "preserved_facts",
    "affected_surfaces",
    "geometry_risks",
    "stale_proofs",
    "reflow_evidence",
)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot load JSON: {error}") from error
    if not isinstance(value, dict):
        raise ValueError("contract root must be a JSON object")
    return value


def nonempty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return value is not None


def require_fields(
    value: dict[str, Any], fields: tuple[str, ...], prefix: str, errors: list[str]
) -> None:
    for field in fields:
        if not nonempty(value.get(field)):
            errors.append(f"{prefix}.{field} must be non-empty")


def require_lists(
    value: dict[str, Any], fields: tuple[str, ...], prefix: str, errors: list[str]
) -> None:
    for field in fields:
        candidate = value.get(field)
        if not isinstance(candidate, list) or not candidate:
            errors.append(f"{prefix}.{field} must be a non-empty list")


def project_path(root: Path, raw_path: Any) -> Path | None:
    if not isinstance(raw_path, str) or not raw_path.strip():
        return None
    candidate = (root / raw_path).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def validate_reflow_evidence(
    evidence: Any, prefix: str, root: Path, errors: list[str]
) -> None:
    if not isinstance(evidence, list) or not evidence:
        return
    for index, item in enumerate(evidence):
        item_prefix = f"{prefix}[{index}]"
        if not isinstance(item, dict):
            errors.append(
                f"{item_prefix} must be an object with surface, proof_type, path, and freshness"
            )
            continue
        require_fields(item, ("surface", "proof_type", "path"), item_prefix, errors)
        if item.get("fresh_after_copy_change") is not True:
            errors.append(f"{item_prefix}.fresh_after_copy_change must be true")
        path = project_path(root, item.get("path"))
        if path is None or not path.is_file():
            errors.append(f"{item_prefix}.path is missing or outside root")


def validate(contract: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    if contract.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    lock = contract.get("design_system_lock")
    lock_id: str | None = None
    if not isinstance(lock, dict):
        errors.append("design_system_lock must be an object")
    else:
        state = lock.get("state")
        if state not in LOCK_STATES:
            errors.append(f"design_system_lock.state must be one of {sorted(LOCK_STATES)}")
        elif state == "locked":
            require_fields(lock, LOCK_FIELDS, "design_system_lock", errors)
            raw_lock_id = lock.get("lock_id")
            lock_id = raw_lock_id if isinstance(raw_lock_id, str) else None
        elif not nonempty(lock.get("reason")):
            errors.append("design_system_lock.reason is required when state is not_applicable")

    scenes = contract.get("scene_units")
    scene_ids: set[str] = set()
    verified_scene_ids: set[str] = set()
    if not isinstance(scenes, list) or not scenes:
        errors.append("scene_units must be a non-empty list")
        scenes = []
    for index, scene in enumerate(scenes):
        prefix = f"scene_units[{index}]"
        if not isinstance(scene, dict):
            errors.append(f"{prefix} must be an object")
            continue
        require_fields(scene, SCENE_SCALAR_FIELDS, prefix, errors)
        require_lists(scene, SCENE_LIST_FIELDS, prefix, errors)
        unit_id = scene.get("unit_id")
        if isinstance(unit_id, str) and unit_id.strip():
            if unit_id in scene_ids:
                errors.append(f"{prefix}.unit_id is duplicated: {unit_id}")
            scene_ids.add(unit_id)

        scene_mode = scene.get("scene_mode")
        if scene_mode not in SCENE_MODES:
            errors.append(f"{prefix}.scene_mode must be one of {sorted(SCENE_MODES)}")
        if scene.get("materiality_candidate_space") != "open_set":
            errors.append(f"{prefix}.materiality_candidate_space must be open_set")
        route = scene.get("route_status")
        if route not in ROUTE_STATUSES:
            errors.append(f"{prefix}.route_status must be one of {sorted(ROUTE_STATUSES)}")
        elif route in BLOCKING_ROUTE_STATUSES:
            errors.append(f"{prefix}.route_status is a blocking release state: {route}")
        localization_state = scene.get("localization_state")
        if localization_state not in LOCALIZATION_STATES:
            errors.append(
                f"{prefix}.localization_state must be one of {sorted(LOCALIZATION_STATES)}"
            )
        elif localization_state in BLOCKING_LOCALIZATION_STATES:
            errors.append(
                f"{prefix}.localization_state is pending and blocks release: {localization_state}"
            )
        elif localization_state == "reflow_verified" and isinstance(unit_id, str):
            verified_scene_ids.add(unit_id)
        if lock_id and scene.get("design_system_lock_ref") != lock_id:
            errors.append(f"{prefix}.design_system_lock_ref must equal {lock_id!r}")
        if not nonempty(scene.get("semantic_variable_ledger")):
            errors.append(f"{prefix}.semantic_variable_ledger must be non-empty")
        if not nonempty(scene.get("visual_vocabulary_budget")):
            errors.append(f"{prefix}.visual_vocabulary_budget must be non-empty")

    reflows = contract.get("localization_reflow", [])
    reflow_ids: set[str] = set()
    if not isinstance(reflows, list):
        errors.append("localization_reflow must be a list")
        reflows = []
    for index, reflow in enumerate(reflows):
        prefix = f"localization_reflow[{index}]"
        if not isinstance(reflow, dict):
            errors.append(f"{prefix} must be an object")
            continue
        require_fields(reflow, REFLOW_SCALAR_FIELDS, prefix, errors)
        require_lists(reflow, REFLOW_LIST_FIELDS, prefix, errors)
        unit_id = reflow.get("unit_id")
        if isinstance(unit_id, str) and unit_id.strip():
            if unit_id not in scene_ids:
                errors.append(f"{prefix}.unit_id does not match a scene unit: {unit_id}")
            if unit_id in reflow_ids:
                errors.append(f"{prefix}.unit_id is duplicated: {unit_id}")
            reflow_ids.add(unit_id)
        if reflow.get("localization_state") != "reflow_verified":
            errors.append(f"{prefix}.localization_state must be reflow_verified for release")
        validate_reflow_evidence(reflow.get("reflow_evidence"), f"{prefix}.reflow_evidence", root, errors)

    missing_reflow = verified_scene_ids - reflow_ids
    for unit_id in sorted(missing_reflow):
        errors.append(f"scene unit {unit_id!r} is reflow_verified without localization_reflow evidence")
    return errors


def valid_fixture(proof_path: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "design_system_lock": {
            "state": "locked",
            "lock_id": "report-system-v1",
            "token_style_namespace": "--report-*",
            "typography_hierarchy": {"display": "32/40", "body": "16/24"},
            "spacing_density": {"unit": 8, "mode": "editorial"},
            "component_grammar": {"container": "outlined", "radius": 12},
            "status_semantics": {"green": "verified", "amber": "pending"},
            "accessibility_contrast": {"body_min": "4.5:1", "reading_order": "dom"},
        },
        "scene_units": [
            {
                "unit_id": "journey-01",
                "source_sentence": "가져온 자료를 150분 동안 결과물로 바꾸고 7일 안에 재사용한다.",
                "artifact_role": "explanation",
                "one_scene_statement": "입력이 실습과 결과물을 거쳐 재사용으로 이어진다.",
                "scene_mode": "abstract_relationship",
                "concrete_entities": ["input bundle", "workbench", "finished output", "reuse loop"],
                "action_or_state_change": "input becomes output and enters reuse",
                "core_read_3s": "input to output to reuse",
                "reader_inference_or_action": "bring material and leave with a reusable artifact",
                "visible_cue": ["left-to-right transformation", "return loop"],
                "semantic_boundary": "does not claim learning outcome",
                "deterministic_meaning_items": ["가져온 자료", "150분", "완성 결과물", "7일"],
                "design_system_lock_ref": "report-system-v1",
                "materiality_candidate_space": "open_set",
                "open_materiality_candidates": ["native process scene", "object collage", "hybrid storyboard"],
                "selected_materiality_reason": "deterministic process structure preserves exact labels",
                "route_status": "SVG_ALLOWED",
                "semantic_variable_ledger": {"return_loop": "reuse"},
                "pattern_class": "transform-and-return",
                "visual_vocabulary_budget": {"return_loop": 1},
                "localization_state": "reflow_verified",
                "recovery_action": "increase reserved text/action zone and rerender",
            }
        ],
        "localization_reflow": [
            {
                "unit_id": "journey-01",
                "language_owner": "korean",
                "source_phrase": "Bring Your Work",
                "rendered_phrase": "가져온 자료",
                "preserved_facts": ["input belongs to participant", "no outcome claim"],
                "affected_surfaces": ["journey card", "accessible label"],
                "geometry_risks": ["wrap", "reserved action zone"],
                "stale_proofs": ["previous mobile screenshot", "previous PDF render"],
                "reflow_evidence": [
                    {
                        "surface": "mobile-report",
                        "proof_type": "render",
                        "path": proof_path,
                        "fresh_after_copy_change": True,
                    }
                ],
                "localization_state": "reflow_verified",
                "recovery_action": "return to source layout when fresh render fails",
            }
        ],
    }


def run_self_test() -> int:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        proof = root / "proof" / "reflow.png"
        proof.parent.mkdir()
        proof.write_bytes(b"fresh-render-proof")
        fixture = valid_fixture("proof/reflow.png")
        if errors := validate(fixture, root):
            print("[FAIL] valid fixture:", *errors, sep="\n  - ")
            return 1

        pending = copy.deepcopy(fixture)
        pending["scene_units"][0]["localization_state"] = "translated_pending_reflow"
        if not validate(pending, root):
            print("[FAIL] pending localization state was not rejected")
            return 1

        drift = copy.deepcopy(fixture)
        drift["scene_units"][0]["design_system_lock_ref"] = "report-system-v2"
        if not validate(drift, root):
            print("[FAIL] design-system lock drift was not rejected")
            return 1

        missing_proof = copy.deepcopy(fixture)
        missing_proof["localization_reflow"][0]["reflow_evidence"][0]["path"] = "proof/missing.png"
        if not validate(missing_proof, root):
            print("[FAIL] missing reflow proof was not rejected")
            return 1
    print("[PASS] scene/materiality/reflow contract self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", nargs="?", type=Path, help="scene/materiality/reflow contract JSON")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="project root for evidence paths")
    parser.add_argument("--self-test", action="store_true", help="run deterministic valid and failing fixtures")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()
    if args.contract is None:
        parser.error("contract is required unless --self-test is used")
    try:
        errors = validate(load_json(args.contract), args.root)
    except ValueError as error:
        print(f"[FAIL] {error}")
        return 1
    if errors:
        print("[FAIL] scene/materiality/reflow contract")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("[PASS] scene/materiality/reflow contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
