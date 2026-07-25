# PPTX Standard XML Generation

This reference keeps the reusable boundary between PPTX generation, native
PowerPoint editability, PresentationML/OPC compliance, and final PowerPoint open
evidence.

## Source Distillation Boundary

This reference was distilled from project-local PPTX tooling, but the source
paths are intentionally not bundled as runtime instructions. A host project
must provide its own compatible builder/verifier commands, preferably through
relative paths or `VISUAL_AUTHORING_NPM_WORKSPACE`. The global skill keeps the
reusable generation and validation shape; it does not copy a project's deck
content, generated PPTX files, downloaded spec bundles, audit outputs, or local
absolute paths.

## Tool Separation

| Surface | Purpose | Typical Evidence |
| --- | --- | --- |
| `pptxgenjs_helpers` or equivalent | Generate editable PPTX objects while respecting layout, text, image, SVG, code, and table helper boundaries | PPTX file, build log, native object audit |
| PPTX builder | Create a new PPTX package rather than repairing a recovered file | `*.pptx` |
| Compatible npm state runner | Create the system state, runbook, and release packet before build | `09-system-state.json`, `10-system-runbook.md`, `11-release-packet.md` |
| Native package verifier | Inspect package parts, content types, relationships, slide order, drawing IDs, table anchors, notes, master/layout/theme flow, and editable surfaces | `native-feature-audit.json` |
| Native object intent/geometry verifier | Compare named semantic units and declared relations to actual object types, bounds, order, and connector attachment | `native-object-intent-plan.json`, `native-object-audit.json` |
| PresentationML spec verifier | Prove local ECMA-376/MS-PPTX source coverage and map rules to deterministic checks | `spec_sources/presentationml/reports/presentationml-spec-audit.json` |
| Recovery-lineage gate | Record that stale incident artifacts are superseded by a fresh no-recovery check and cannot seed the next source family | lineage rejection result or repetition gate audit |
| PowerPoint open check | Confirm Microsoft PowerPoint opens the package without a recovery dialog | manual or automation-backed open-check record |
| Conversion-free render path | Produce viewing evidence without making an external conversion output the editable source or release proxy | slide-scoped PNG/contact sheet, HTML/SVG prototype, image scene-base integration proof |

## Compatible NPM Authoring Flow

When a target project exposes the compatible authoring scripts, run the full
sequence below. The commands are a release process contract, not a loose example:

```bash
npm run system:init -- <work-id> --title "<slide title>"
npm run system:run -- <work-id>
npm run build
npm run verify:presentationml-spec
npm run research:build
npm run verify:research
npm run verify:powerpoint
npm run compare:recovery
npm run verify:repetition-gate
# Open Document_Slide_Authoring_System_new.pptx in Microsoft PowerPoint.
# Record manual-open-checks/latest-powerpoint-open-check.json with result=no_recovery_dialog.
npm run verify:release
npm run agent-system:check
```

Required state outputs:

- `09-system-state.json`
- `10-system-runbook.md`
- `11-release-packet.md`

Required PPTX output:

- `Document_Slide_Authoring_System_new.pptx`

Required manual open check:

- `manual-open-checks/latest-powerpoint-open-check.json`
- `result: no_recovery_dialog`
- open-check timestamp newer than the PPTX build timestamp

Accepted release statuses:

- `release_status=pass`
- `release_status=pass_superseded_old_recovery_artifacts`

`npm test` can rebuild the PPTX because it runs the build path internally in
the compatible workspace. After a fresh PowerPoint open check, do not run
`npm test` unless the PPTX will be rebuilt intentionally and the PowerPoint
open check will be repeated.

## Normative Rule Families

Use local source bundles when available. The reusable rule families are:

- ECMA-376 Part 1: PresentationML, DrawingML, slide/master/layout/notes flow
- ECMA-376 Part 2: Open Packaging Conventions, content types, relationships
- ECMA-376 Part 3: Markup Compatibility and Extensibility
- ECMA-376 Part 4: transitional schema and migration features
- MS-PPTX: PowerPoint extension behavior

## Generation Rules

1. Start from outline notes that make the reader situation, purpose, section
   flow, slide sequence, visible message, spoken notes, evidence links, visual
   intent, and open questions inspectable before PPTX construction.
2. Generate a new editable PPTX; do not patch a recovered PowerPoint repair
   artifact as the release candidate.
3. Create a Native Object Intent Plan and a `pptx-native-conformance-contract.json`
   before build. Keep text boxes, tables, charts, notes, hyperlinks, alt text,
   read order, semantic object names, groups, connectors, and presentation
   behavior native when meaning, expected edits, or teaching flow require them.
   The conformance contract also decides every core PowerPoint capability,
   requires Pretendard theme font faces, native title/section/TOC/automatic
   slide-number structures, default center/middle text in shapes, and named
   raster exceptions. Native object count alone is not proof.
4. Treat `visual_value_spec.typography` as a build input. DrawingML text sizes
   are represented in 1/100 point values, so 27pt is `2700` when direct XML
   inspection is used.
5. Preserve OPC package basics: `[Content_Types].xml`, root relationships,
   `ppt/presentation.xml`, presentation relationships, view properties, table
   styles, masters, layouts, themes, notes, and media relationships.
6. Avoid duplicate non-visual drawing IDs such as `cNvPr@id`.
7. Validate DrawingML table cell anchors against valid `ST_TextAnchoringType`
   values at source-build time. Invalid anchors block the build; they are not
   repaired into a new source lineage.
8. Keep generated hidden audit or metadata surfaces separate from learner-facing
   slides.
9. If the compatible npm route is used, run `system:run` before `build`, then
   treat the generated state, runbook, release packet, PPTX, native audit,
    recovery-lineage check, render evidence, and manual PowerPoint open check as separate evidence
    surfaces.
10. After build, run the native object/geometry audit and the native conformance
    validator against the exact PPTX and contract hashes. The conformance tool
    writes only a report and source-level repair plan; it never patches a PPTX.
    Rebuild makes geometry, native, render, and manual-open evidence stale.

## Verification Rules

A generated PPTX is not done because it rendered as PNG or exported as PDF.
Before release, preserve these separate evidence surfaces:

- build evidence: PPTX exists
- native feature evidence: editable surfaces and package structure pass
- native intent evidence: critical semantic units match object type and required
  relations; declared geometry constraints are calculated per slide/object
- native convention evidence: declared PowerPoint capability decisions, theme
  fonts, title/section/TOC/automatic-number structures, shape-text defaults,
  and raster exceptions match the exact package
- PresentationML evidence: ECMA-376/MS-PPTX source coverage and rule mapping pass
- repeated-issue evidence: known recovery patterns are not repeating silently
- render evidence: slide-scoped PNG/contact sheet, HTML/SVG prototype, or
  image scene-base integration proof; no render path becomes editable source
- final release evidence: Microsoft PowerPoint fresh open shows no recovery
  dialog and the open check is newer than the PPTX build
- compatible npm release evidence: accepted `release_status` is `pass` or
  `pass_superseded_old_recovery_artifacts`

## Claim Boundary

`pptx-standard-xml-build` can support a structural-generation claim only when a
new PPTX exists and the expected helper/build path was used.

`presentationml-spec-check` and `native-powerpoint-check` can support a package
and native-feature proxy claim.

`native-object-audit` can support an `observed_computation` claim about object
existence, type, bounds, alignment/spacing/overlap, order, connector attachment,
and semantic coverage. It cannot prove content fit, good design, edit-session
success, or learner understanding.

`validate_pptx_native_conformance.py` can support an observed native-convention
claim and a source-only remediation plan. It cannot repair a recovery incident,
prove a PowerPoint open, or prove that people can edit/read/understand the deck.

Only the PowerPoint open check can support the final no-recovery release claim.
That claim becomes stale if a later command rebuilds the PPTX.
