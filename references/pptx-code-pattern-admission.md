# PPTX Code-Pattern and Reader-Admission Contract

Use this contract when authored lecture or presentation content is converted into an editable PPTX by code. It extends the source-lineage contract with a fixed-code control surface, a complete pattern catalog, and a fail-closed reader-public admission gate.

## Control Model

`fixed_code_orchestrates_flexible_decisions` is the required mode.

| Layer | Owner | May decide | May not decide |
| --- | --- | --- | --- |
| Fixed | compiler, validator, composer | schemas, allowed renderers, native object gateways, OOXML contracts, pre/post gates, file writing, evidence status computation | instructional meaning or the best scene for this audience |
| Flexible | LLM or human author | slide copy, semantic job, scene-pattern selection, reading sequence, layout-tuning intent | raw OOXML, raw emission calls, validator result, ledger pass status |
| Decision | LLM proposes; code admits or rejects | why this scene/pattern fits, which capability is used or not used, what to revise | bypassing a failed gate or widening policy only to obtain a pass |

The LLM directs the fixed renderer with declarative values. It does not become the renderer and it cannot certify its own output. Fixed code must reject an unknown field, route, renderer, raw OOXML fragment, status override, or unregistered visible string.

## Four-layer pattern catalog

Every new PPTX family needs one `pptx-code-pattern-catalog.json` before emission.

```json
{
  "schema_version": "1.0",
  "catalog_id": "replace-me",
  "source_family_id": "replace-me",
  "authored_slide_count": 1,
  "pattern_layers": [
    "instructional_scene",
    "native_object",
    "ooxml_capability",
    "verification_evidence"
  ],
  "control_model": {
    "mode": "fixed_code_orchestrates_flexible_decisions",
    "flexible_decision_surface": {
      "owner": "LLM_or_human_author",
      "allowed": ["slide_copy", "scene_pattern_selection", "semantic_job", "layout_tuning_intent"],
      "forbidden": ["raw_ooxml", "validation_status_override", "gateway_bypass", "evidence_ledger_status_override"]
    },
    "fixed_code_surface": {
      "owner": "compiler_and_validators",
      "required_pre_emit_gates": ["catalog_binding", "reader_surface_admission", "ooxml_contract", "evidence_ledger_separation"],
      "write_condition": "all_pre_emit_gates_pass"
    }
  },
  "scene_patterns": [],
  "capability_patterns": [],
  "required_manifest_contract_paths": []
}
```

The four layers mean:

1. `instructional_scene`: authored kind, semantic job, reading sequence, chosen scene pattern.
2. `native_object`: renderer, layout family, editable shape/table/list/image/notes/connector/group.
3. `ooxml_capability`: each relevant function is `used`, `intentionally_not_used`, or `not_applicable`, with reason and source evidence.
4. `verification_evidence`: the exact output is checked by separate structural, reading, viewing, and native-runtime ledgers.

## Fixed pipeline

```text
LLM/human declarative decision payload
  -> fixed schema and catalog validator
  -> fixed reader-public registration and gateway audit
  -> fixed renderer registry and native-object emitters
  -> fixed OOXML composer
  -> fixed structural/read/render/native evidence routing
  -> file write only after all pre-emit gates pass
```

Every authored slide kind maps exactly once to a scene pattern. The catalog renderer must exist in source, the source dispatch must call it, the listed slides must match authored source order, and the layout family must match the manifest. No default renderer is allowed to hide an unknown kind.

## Reader-public admission

Reader-public admission is separate from production metadata and instructor notes.

- Route every visible string through one registration function before `slide.addText` or native-table emission.
- Keep each raw emission API in exactly one shared gateway. A second raw call is a bypass and must fail before output is written.
- Exclude notes, transitions, evidence labels, IDs, and internal routing fields from the visible-copy expectation.
- Define allowed domain, brand, role, and interface terms narrowly. Unknown English or internal build vocabulary is a finding, not a reason to expand the allowlist.
- Scan exact visible records, not only the source file, so computed strings and native table cells are covered.

Start from `references/reader-surface-admission-policy.example.json`; replace the artifact identifier and explicitly justify every allowed reader term.

## Capability decisions

For every relevant PPTX feature, record one status.

- `used`: evidence points to the exact implementation and verifier.
- `intentionally_not_used`: the feature is applicable but would weaken this teaching or presentation behavior; record the reason.
- `not_applicable`: the content has no semantic job for the feature; record the reason.

Do not add charts, SmartArt, media, animation, or decoration merely to raise feature count. Do not omit sections, notes, editable tables/lists, navigation, accessibility, or native relations when the scene actually needs them.

For the full PowerPoint-native baseline, keep this catalog aligned with
`pptx-native-conformance-contract.json`. That contract adds theme-font,
automatic-slide-number, native-section/TOC/title-story, default shape-text
alignment, raster-exception, and source-level self-remediation checks. The
pattern catalog controls what the compiler may emit; the conformance contract
checks whether the emitted package follows the intended PowerPoint convention.

## Evidence ledgers

Keep four exact-artifact ledgers. A pass in one ledger cannot be copied to another.

| Ledger | Proves | Does not prove |
| --- | --- | --- |
| `structural_package` | OPC/PresentationML structure and declared native objects | readable rendering or native PowerPoint behavior |
| `reading_content` | extracted text, order, claims, notes, transitions | text fit, visual hierarchy, audience learning |
| `viewing_render` | image/contact-sheet appearance for the same hash | native open/edit/show behavior |
| `native_runtime` | exact-hash PowerPoint open/edit/show observations | audience comprehension or learning transfer |

## Validation

Run the catalog validator before the emitter:

```bash
scripts/visual-authoring-runtime run scripts/validate_pptx_code_pattern_catalog.py \
  pptx-code-pattern-catalog.json \
  pptx-pattern-compiler-manifest.json \
  build-deck.mjs \
  build/pattern-catalog-report.json
```

Import `scripts/reader_surface_admission.mjs` in the compiler, register visible text through its API, and call `assertReaderSurfaceAdmission(...)` before `pptx.writeFile(...)`.

Validate the fixed compiler contract and the emitted native objects as separate gates:

```bash
scripts/visual-authoring-runtime run scripts/validate_pptx_pattern_compiler_manifest.py \
  pptx-pattern-compiler-manifest.json

scripts/visual-authoring-runtime run scripts/audit_pptx_native_objects.py \
  --pptx build/deck.pptx \
  --intent native-object-intent-plan.json \
  --output build/native-object-audit.json
```

Together, these validators prove code-to-declaration binding, reader-surface policy enforcement, compiler evidence routing, connector and relation attachment, native-object coverage, and reading-order proxies. They do not prove content fit, visual quality, native PowerPoint compatibility, or learner transfer.
