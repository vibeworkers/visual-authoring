#!/usr/bin/env python3
"""Validate the deterministic parts of a public publication surface contract."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any


VALID_CONFORMANCE_CLAIMS = {"not_claimed", "validated_with_evidence"}
VALID_FEATURE_STATUSES = {"used", "not_applicable", "blocked"}


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot load JSON: {error}") from error
    if not isinstance(value, dict):
        raise ValueError("contract root must be a JSON object")
    return value


def project_path(root: Path, raw_path: Any) -> Path | None:
    if not isinstance(raw_path, str) or not raw_path.strip():
        return None
    candidate = (root / raw_path).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def file_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def validate(contract: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    if contract.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    artifact_profile = contract.get("artifact_profile")
    if artifact_profile not in {"single_publication", "textbook_with_workbook"}:
        errors.append("artifact_profile must be single_publication or textbook_with_workbook")

    reader_public = contract.get("reader_public")
    if not isinstance(reader_public, dict):
        errors.append("reader_public must be an object")
    else:
        public_files = reader_public.get("files")
        forbidden_terms = reader_public.get("forbidden_terms")
        if not isinstance(public_files, list) or not public_files:
            errors.append("reader_public.files must contain focused public-surface text files")
        if not isinstance(forbidden_terms, list) or not all(
            isinstance(term, str) and term.strip() for term in forbidden_terms
        ):
            errors.append("reader_public.forbidden_terms must contain non-empty strings")
            forbidden_terms = []
        if isinstance(public_files, list):
            for raw_path in public_files:
                path = project_path(root, raw_path)
                if path is None:
                    errors.append(f"reader_public file is outside root or invalid: {raw_path!r}")
                    continue
                if not path.is_file():
                    errors.append(f"reader_public file is missing: {raw_path}")
                    continue
                text = file_text(path)
                for term in forbidden_terms:
                    if term in text:
                        errors.append(f"public surface contains forbidden term {term!r}: {raw_path}")

    roles = contract.get("artifact_roles")
    if artifact_profile == "textbook_with_workbook":
        if not isinstance(roles, dict):
            errors.append("artifact_roles must be an object for textbook_with_workbook")
        else:
            for role_name in ("textbook_main", "workbook_companion"):
                role = roles.get(role_name)
                if not isinstance(role, dict):
                    errors.append(f"artifact_roles.{role_name} must be an object")
                    continue
                path = project_path(root, role.get("path"))
                if path is None or not path.is_file():
                    errors.append(f"artifact role file is missing or invalid: {role_name}")
                    continue
                markers = role.get("required_markers")
                if not isinstance(markers, list) or not all(
                    isinstance(marker, str) and marker.strip() for marker in markers
                ):
                    errors.append(f"artifact_roles.{role_name}.required_markers must be non-empty strings")
                    continue
                text = file_text(path)
                for marker in markers:
                    if marker not in text:
                        errors.append(f"artifact role marker missing ({role_name}): {marker!r}")

    profiles = contract.get("format_standard_profile")
    if not isinstance(profiles, dict) or not profiles:
        errors.append("format_standard_profile must declare at least one delivery format")
    else:
        for format_name, profile in profiles.items():
            if not isinstance(profile, dict) or not isinstance(profile.get("profile"), str):
                errors.append(f"format_standard_profile.{format_name} needs a profile name")
                continue
            features = profile.get("features")
            if not isinstance(features, list) or not features:
                errors.append(
                    f"format_standard_profile.{format_name}.features must declare applicable standard features"
                )
            else:
                seen_feature_ids: set[str] = set()
                for index, feature in enumerate(features):
                    if not isinstance(feature, dict):
                        errors.append(f"format_standard_profile.{format_name}.features[{index}] must be an object")
                        continue
                    feature_id = feature.get("id")
                    status = feature.get("status")
                    if not isinstance(feature_id, str) or not feature_id.strip():
                        errors.append(
                            f"format_standard_profile.{format_name}.features[{index}].id must be a non-empty string"
                        )
                        continue
                    if feature_id in seen_feature_ids:
                        errors.append(f"duplicate standard feature id ({format_name}): {feature_id!r}")
                    seen_feature_ids.add(feature_id)
                    if status not in VALID_FEATURE_STATUSES:
                        errors.append(
                            f"format_standard_profile.{format_name}.features[{index}].status must be one of "
                            f"{sorted(VALID_FEATURE_STATUSES)}"
                        )
                        continue
                    if status == "used":
                        evidence_path = project_path(root, feature.get("evidence_path"))
                        if evidence_path is None or not evidence_path.is_file():
                            errors.append(
                                f"used standard feature lacks evidence_path ({format_name}): {feature_id!r}"
                            )
                    else:
                        reason = feature.get("reason")
                        if not isinstance(reason, str) or not reason.strip():
                            errors.append(
                                f"{status} standard feature lacks reason ({format_name}): {feature_id!r}"
                            )
                        if status == "blocked":
                            errors.append(f"blocked standard feature prevents release ({format_name}): {feature_id!r}")
            claim = profile.get("conformance_claim")
            if claim not in VALID_CONFORMANCE_CLAIMS:
                errors.append(
                    f"format_standard_profile.{format_name}.conformance_claim must be one of "
                    f"{sorted(VALID_CONFORMANCE_CLAIMS)}"
                )
            if claim == "validated_with_evidence":
                evidence_path = project_path(root, profile.get("evidence_path"))
                if evidence_path is None or not evidence_path.is_file():
                    errors.append(
                        f"format_standard_profile.{format_name} claims validation without evidence_path"
                    )
    return errors


def run_self_test() -> int:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        (root / "proof").mkdir()
        (root / "proof" / "cover-public.txt").write_text("독자를 위한 표지", encoding="utf-8")
        (root / "proof" / "pdf-metadata.txt").write_text("metadata verified", encoding="utf-8")
        (root / "textbook.md").write_text("핵심 개념\n사례\n판단 기준", encoding="utf-8")
        (root / "workbook.md").write_text("실습\n기록\n본권", encoding="utf-8")
        contract = {
            "schema_version": 1,
            "artifact_profile": "textbook_with_workbook",
            "reader_public": {"files": ["proof/cover-public.txt"], "forbidden_terms": ["draft"]},
            "artifact_roles": {
                "textbook_main": {
                    "path": "textbook.md",
                    "required_markers": ["핵심 개념", "사례", "판단 기준"],
                },
                "workbook_companion": {
                    "path": "workbook.md",
                    "required_markers": ["실습", "기록", "본권"],
                },
            },
            "format_standard_profile": {
                "pdf": {
                    "profile": "standard_informed_distribution_pdf",
                    "features": [
                        {
                            "id": "metadata",
                            "status": "used",
                            "evidence_path": "proof/pdf-metadata.txt",
                        },
                        {
                            "id": "pdfua_conformance",
                            "status": "not_applicable",
                            "reason": "No PDF/UA conformance profile was requested.",
                        },
                    ],
                    "conformance_claim": "not_claimed",
                }
            },
        }
        if errors := validate(contract, root):
            print("[FAIL] self-test valid fixture:", *errors, sep="\n  - ")
            return 1
        (root / "proof" / "cover-public.txt").write_text("draft", encoding="utf-8")
        if not validate(contract, root):
            print("[FAIL] self-test did not detect forbidden public term")
            return 1
        (root / "proof" / "cover-public.txt").write_text("독자를 위한 표지", encoding="utf-8")
        contract["format_standard_profile"]["pdf"]["features"][0]["evidence_path"] = "proof/missing.txt"
        if not validate(contract, root):
            print("[FAIL] self-test did not detect missing standard-feature evidence")
            return 1
    print("[PASS] publication surface contract self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", nargs="?", type=Path, help="publication surface contract JSON")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="project root for relative paths")
    parser.add_argument("--self-test", action="store_true", help="run deterministic fixtures")
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
        print("[FAIL] publication surface contract")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("[PASS] publication surface contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
