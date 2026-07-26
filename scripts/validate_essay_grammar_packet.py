#!/usr/bin/env python3
"""Validate a corpus-derived essay grammar packet without touching source texts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SCHEMA = "visual-authoring.essay-grammar.v1"
ROLES = {"entry_tension", "exploration_question", "context_bridge", "thought_shift", "open_end"}
SOURCE_ROLES = {"author_corpus_reference", "conversation_corpus_reference"}
REQUIRED_CORPUS_ROLES = {"entry_tension", "context_bridge", "open_end"}
REQUIRED_NON_CLAIMS = {"not_official_brunch_platform_grammar", "not_a_human_outcome_claim"}
CONVERSATION_LENSES = {
    "linguistics",
    "counseling_psychology",
    "coaching",
    "behavior_change",
    "symbolic_systems",
    "cognitive_science",
}
SURFACES = {"web", "document", "hybrid"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--root", type=Path, help="Optional corpus root used only to confirm source paths exist")
    args = parser.parse_args()

    errors: list[str] = []
    try:
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "fail", "errors": [str(exc)]}, ensure_ascii=False))
        return 2

    if packet.get("schema_version") != SCHEMA:
        fail(errors, f"schema_version must be {SCHEMA}")
    if not isinstance(packet.get("corpus_id"), str) or not packet["corpus_id"].strip():
        fail(errors, "corpus_id must be a non-empty string")
    source_role = packet.get("source_role")
    if source_role not in SOURCE_ROLES:
        fail(errors, f"source_role must be one of: {sorted(SOURCE_ROLES)}")

    samples = packet.get("sample_sources")
    if not isinstance(samples, list) or len(samples) < 3:
        fail(errors, "sample_sources must contain at least three sources")
        samples = []

    seen_ids: set[str] = set()
    observed_roles: set[str] = set()
    root = args.root.resolve() if args.root else None
    for index, source in enumerate(samples):
        if not isinstance(source, dict):
            fail(errors, f"sample_sources[{index}] must be an object")
            continue
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id.strip() or source_id in seen_ids:
            fail(errors, f"sample_sources[{index}].id must be unique and non-empty")
        else:
            seen_ids.add(source_id)
        path_text = source.get("source_path")
        relative_path = Path(path_text) if isinstance(path_text, str) else None
        if (
            not isinstance(path_text, str)
            or not path_text.strip()
            or relative_path is None
            or relative_path.is_absolute()
            or ".." in relative_path.parts
        ):
            fail(errors, f"sample_sources[{index}].source_path must be a non-empty, non-escaping relative path")
        elif root and not (root / path_text).is_file():
            fail(errors, f"sample_sources[{index}].source_path does not exist under --root: {path_text}")
        if not isinstance(source.get("title"), str) or not source["title"].strip():
            fail(errors, f"sample_sources[{index}].title must be a non-empty string")
        roles = source.get("observed_roles")
        if not isinstance(roles, list) or not roles:
            fail(errors, f"sample_sources[{index}].observed_roles must be a non-empty list")
        else:
            invalid = set(roles) - ROLES
            if invalid:
                fail(errors, f"sample_sources[{index}].observed_roles contains invalid values: {sorted(invalid)}")
            observed_roles.update(role for role in roles if role in ROLES)

    flow = packet.get("observed_flow")
    if not isinstance(flow, list) or not set(flow).issubset(ROLES) or len(flow) < 3:
        fail(errors, "observed_flow must be a list of at least three allowed roles")
    if not REQUIRED_CORPUS_ROLES.issubset(observed_roles):
        fail(errors, f"corpus coverage must include: {sorted(REQUIRED_CORPUS_ROLES)}")
    non_claims = set(packet.get("non_claims", [])) if isinstance(packet.get("non_claims"), list) else set()
    required_non_claims = set(REQUIRED_NON_CLAIMS)
    if source_role == "conversation_corpus_reference":
        required_non_claims = {"not_a_human_outcome_claim", "not_a_clinical_assessment", "not_empirical_theory_validation"}
    if not required_non_claims.issubset(non_claims):
        fail(errors, f"non_claims must include: {sorted(required_non_claims)}")

    if source_role == "conversation_corpus_reference":
        provenance = packet.get("provenance")
        if not isinstance(provenance, dict):
            fail(errors, "conversation_corpus_reference requires provenance")
        else:
            if provenance.get("source_kind") not in {"conversation_and_local_artifacts", "conversation_only"}:
                fail(errors, "provenance.source_kind must identify an accessible conversation source")
            for key in ("accessible_surfaces", "unavailable_surfaces"):
                if not isinstance(provenance.get(key), list):
                    fail(errors, f"provenance.{key} must be a list")
            if not isinstance(provenance.get("transformation"), str) or not provenance["transformation"].strip():
                fail(errors, "provenance.transformation must state verbatim/paraphrase handling")
            if not isinstance(provenance.get("source_boundary"), str) or not provenance["source_boundary"].strip():
                fail(errors, "provenance.source_boundary must state the evidence boundary")

        theory = packet.get("theory_validation")
        if not isinstance(theory, list):
            fail(errors, "conversation_corpus_reference requires theory_validation")
        else:
            lenses = set()
            for index, entry in enumerate(theory):
                if not isinstance(entry, dict):
                    fail(errors, f"theory_validation[{index}] must be an object")
                    continue
                lens = entry.get("lens")
                if lens not in CONVERSATION_LENSES:
                    fail(errors, f"theory_validation[{index}].lens must be one of: {sorted(CONVERSATION_LENSES)}")
                else:
                    lenses.add(lens)
                for key in ("observation", "bounded_interpretation", "not_claim"):
                    if not isinstance(entry.get(key), str) or not entry[key].strip():
                        fail(errors, f"theory_validation[{index}].{key} must be a non-empty string")
            missing_lenses = CONVERSATION_LENSES - lenses
            if missing_lenses:
                fail(errors, f"theory_validation missing lenses: {sorted(missing_lenses)}")

    adaptation = packet.get("target_adaptation")
    if not isinstance(adaptation, dict):
        fail(errors, "target_adaptation must be an object")
    else:
        if adaptation.get("target_surface") not in SURFACES:
            fail(errors, f"target_adaptation.target_surface must be one of: {sorted(SURFACES)}")
        for key in ("preserve", "transfer", "discard"):
            if not isinstance(adaptation.get(key), list):
                fail(errors, f"target_adaptation.{key} must be a list")
        if not isinstance(adaptation.get("open_end_policy"), str) or not adaptation["open_end_policy"].strip():
            fail(errors, "target_adaptation.open_end_policy must be a non-empty string")

    report = {
        "status": "pass_local" if not errors else "fail",
        "schema_version": SCHEMA,
        "packet": str(args.packet),
        "checked_source_paths": bool(root),
        "observed_roles": sorted(observed_roles),
        "errors": errors,
        "claim_boundary": "This verifies packet structure, source-path presence, provenance shape, and bounded theory-lens coverage only. It does not prove author intent, diagnosis, platform grammar, theory validity, visual quality, behavior change, or reader outcomes.",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
