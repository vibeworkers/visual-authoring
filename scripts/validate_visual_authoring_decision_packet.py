#!/usr/bin/env python3
"""Validate the bounded user-decision packet for visual-authoring."""

import argparse
import json
from pathlib import Path

SCHEMA = "visual-authoring.decision-preview.v1"
PHASES = {f"phase_{index}" for index in range(6)}
SOURCE_CHOICES = {"continue_improve", "fresh_start", "not_applicable_no_existing_work"}
SELECTION_STATUSES = {"user_selected", "reexplore_requested", "blocked_preview_generation"}
CREDIT_CHOICES = {"include_author_credit", "omit_author_credit", "custom_credit"}
HCI_CRITERIA = {
    "contrast",
    "legibility",
    "attention_hierarchy",
    "state_semantics",
    "color_vision",
    "tone",
}
WEB_OUTPUT_SURFACES = {"html", "web_ui"}
TOOLING_STATUSES = {"implemented", "blocked_tool_runtime"}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def require_path(root, value, label, errors):
    if not nonempty(value):
        errors.append(f"{label} must be a non-empty relative path")
        return
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        errors.append(f"{label} must be a safe relative path")
    elif not (root / path).is_file():
        errors.append(f"{label} is missing: {value}")


def validate_selection(packet, root, errors, key, preview_field, concept_required=False):
    selection = packet.get(key, {})
    status = selection.get("status")
    if status not in SELECTION_STATUSES:
        errors.append(f"{key}.status must be one of {sorted(SELECTION_STATUSES)}")
        return
    if status != "user_selected":
        return
    required = selection.get("required_surface_ids", [])
    candidates = selection.get("candidates", selection.get("options", []))
    if not isinstance(required, list) or not required or not all(nonempty(item) for item in required):
        errors.append(f"{key}.required_surface_ids must be a non-empty list")
    if not isinstance(candidates, list) or len(candidates) < 2:
        errors.append(f"{key} requires at least two comparable candidates")
    candidate_ids = []
    for index, candidate in enumerate(candidates if isinstance(candidates, list) else []):
        prefix = f"{key}[{index}]"
        candidate_id = candidate.get("id")
        if not nonempty(candidate_id):
            errors.append(f"{prefix}.id must be non-empty")
        else:
            candidate_ids.append(candidate_id)
        if concept_required:
            if candidate.get("concept_preview_type") != "image_generated":
                errors.append(f"{prefix}.concept_preview_type must be image_generated")
            require_path(root, candidate.get("concept_preview_path"), f"{prefix}.concept_preview_path", errors)
        require_path(root, candidate.get(preview_field), f"{prefix}.{preview_field}", errors)
        covered = set(candidate.get("covered_surface_ids", []))
        if set(required) - covered:
            errors.append(f"{prefix} does not cover every required surface")
    if selection.get("selected_id") not in candidate_ids:
        errors.append(f"{key}.selected_id must identify one candidate")
    if not nonempty(selection.get("confirmed_by")):
        errors.append(f"{key}.confirmed_by is required for user_selected")


def validate_tooling(packet, root, errors):
    tooling = packet.get("tooling_implementation", {})
    status = tooling.get("status")
    if status not in TOOLING_STATUSES:
        errors.append(f"tooling_implementation.status must be one of {sorted(TOOLING_STATUSES)}")
        return
    if status == "blocked_tool_runtime":
        if not nonempty(tooling.get("blocker")):
            errors.append("tooling_implementation.blocker is required when tool runtime is blocked")
        return
    adapters = tooling.get("adapters", [])
    if not isinstance(adapters, list):
        errors.append("tooling_implementation.adapters must be a list")
        return
    indexed = {adapter.get("capability"): adapter for adapter in adapters if isinstance(adapter, dict)}
    required = [
        ("concept_image", {("imagegen", "tool_call")}),
        ("target_surface_render", {("code_renderer", "code")}),
    ]
    if packet.get("goal_confirmation", {}).get("output_surface") in WEB_OUTPUT_SURFACES:
        required.append(("web_surface_inspection", {("in_app_browser", "tool_call"), ("portable_visual_runtime", "code")}))
    for capability, accepted_adapters in required:
        adapter = indexed.get(capability)
        if not isinstance(adapter, dict):
            errors.append(f"tooling_implementation requires {capability} adapter")
            continue
        actual = (adapter.get("adapter"), adapter.get("implementation"))
        if actual not in accepted_adapters:
            expected = " or ".join(f"{name} via {implementation}" for name, implementation in sorted(accepted_adapters))
            errors.append(f"{capability} must use {expected}")
        paths = adapter.get("evidence_paths", [])
        if not isinstance(paths, list) or not paths:
            errors.append(f"{capability}.evidence_paths must be a non-empty list")
        else:
            for index, path in enumerate(paths):
                require_path(root, path, f"{capability}.evidence_paths[{index}]", errors)
        if capability == "web_surface_inspection":
            if not nonempty(adapter.get("url")):
                errors.append("web_surface_inspection.url must be non-empty")
            assertions = adapter.get("assertions", [])
            if not isinstance(assertions, list) or not assertions or not all(nonempty(item) for item in assertions):
                errors.append("web_surface_inspection.assertions must be a non-empty list")


def validate(packet, root):
    errors = []
    if packet.get("schema_version") != SCHEMA:
        errors.append(f"schema_version must equal {SCHEMA}")

    goal = packet.get("goal_confirmation", {})
    if goal.get("status") != "confirmed":
        errors.append("goal_confirmation.status must be confirmed")
    for field in ("goal", "audience", "output_surface", "success_condition", "confirmed_by"):
        if not nonempty(goal.get(field)):
            errors.append(f"goal_confirmation.{field} must be non-empty")

    continuity = packet.get("source_continuity", {})
    existing = continuity.get("existing_work")
    choice = continuity.get("choice")
    if existing not in {"present", "absent"}:
        errors.append("source_continuity.existing_work must be present or absent")
    if choice not in SOURCE_CHOICES:
        errors.append(f"source_continuity.choice must be one of {sorted(SOURCE_CHOICES)}")
    if existing == "present" and choice == "not_applicable_no_existing_work":
        errors.append("existing work cannot use not_applicable_no_existing_work")
    if existing == "absent" and choice != "not_applicable_no_existing_work":
        errors.append("absent work must use not_applicable_no_existing_work")
    if not nonempty(continuity.get("confirmed_by")):
        errors.append("source_continuity.confirmed_by must be non-empty")

    progress = packet.get("progress", {})
    if progress.get("display_mode") != "step_by_step_progress_bar":
        errors.append("progress.display_mode must be step_by_step_progress_bar")
    closed = progress.get("closed_phases", [])
    if not isinstance(closed, list) or not set(closed).issubset(PHASES):
        errors.append("progress.closed_phases must contain only known phases")
    if progress.get("current_phase") not in PHASES:
        errors.append("progress.current_phase must be a known phase")

    validate_selection(packet, root, errors, "strategy_selection", "target_surface_preview_path", concept_required=True)
    validate_selection(packet, root, errors, "color_selection", "complete_surface_preview_path")
    color = packet.get("color_selection", {})
    if color.get("status") == "user_selected" and set(color.get("hci_criteria", [])) != HCI_CRITERIA:
        errors.append("color_selection.hci_criteria must cover all six HCI criteria")
    validate_tooling(packet, root, errors)

    credit = packet.get("release_credit", {})
    if credit.get("release_stage") != "pre_release":
        errors.append("release_credit.release_stage must be pre_release")
    if credit.get("choice") not in CREDIT_CHOICES:
        errors.append(f"release_credit.choice must be one of {sorted(CREDIT_CHOICES)}")
    if not nonempty(credit.get("confirmed_by")):
        errors.append("release_credit.confirmed_by must be non-empty")
    if credit.get("choice") == "custom_credit":
        for field in ("credit_text", "placement"):
            if not nonempty(credit.get(field)):
                errors.append(f"release_credit.{field} is required for custom_credit")

    feedback = packet.get("human_feedback", {})
    if feedback.get("mode") not in {"off", "on"}:
        errors.append("human_feedback.mode must be off or on")
    if not nonempty(feedback.get("questionnaire_reference")):
        errors.append("human_feedback.questionnaire_reference must be non-empty")
    if feedback.get("mode") == "on":
        for field in ("audience", "consent_status", "collection_channel", "retention_policy", "stop_condition"):
            if not nonempty(feedback.get(field)):
                errors.append(f"human_feedback.{field} is required when mode is on")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate a visual-authoring decision-preview packet.")
    parser.add_argument("packet", help="JSON decision packet")
    parser.add_argument("--root", default=".", help="root for relative preview paths")
    args = parser.parse_args()
    packet_path = Path(args.packet)
    root = Path(args.root)
    try:
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "fail_local", "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        raise SystemExit(2)
    errors = validate(packet, root)
    closed = len(packet.get("progress", {}).get("closed_phases", []))
    result = {
        "status": "pass_local" if not errors else "fail_local",
        "progress_bar": "█" * min(closed, 6) + "░" * max(0, 6 - min(closed, 6)),
        "errors": errors,
        "claim_boundary": "This verifies decision-packet structure and declared tool adapters; it does not run tools or prove preview quality, accessibility, preference, comprehension, behavior change, or release approval.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
