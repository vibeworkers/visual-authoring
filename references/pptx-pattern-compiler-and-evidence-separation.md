# PPTX Pattern Compiler and Evidence-Separation Contract

## Purpose

This contract applies when a PowerPoint deck is newly built, substantially
rebuilt, or restarted after a compatibility incident. It prevents a damaged,
recovered, normalized, or converted package from silently becoming the next
production source.

The governing principle is:

> Fixed patterns materialize a compatible PPTX; LLM judgment selects and fills
> those patterns; explicit decisions and proof ledgers keep neither layer from
> impersonating the other.

## No-repair lineage

A candidate that has shown a PowerPoint recovery dialog is an incident artifact.
It may be retained as a diagnostic reference, but it must not be:

- released;
- renamed as a clean candidate;
- used as an input to a full-deck build;
- used as the source family for normalization, ZIP/XML repair, conversion,
  PowerPoint resave, or preflight repair; or
- used as prototype authorization evidence for a fresh family.

The correct response is source-level diagnosis followed by a new, independently
identified source family. Rebuilding from new authored content and a declared
pattern manifest is different from repairing or converting an old package.

`source-level self-remediation` is the executable form of this rule. Run
`scripts/validate_pptx_native_conformance.py` with a declarative conformance
contract. If it reports `repair_required`, change the authored source, manifest,
or compiler and rebuild under a fresh `source_family_id`. The tool may write a
report and repair plan, but it must not alter the incident PPTX.

## The three layers

| Layer | Owns | Does not own |
| --- | --- | --- |
| Fixed | 16:9 canvas, typed scene payloads, a small pattern library, outline/sections/lists/tables/notes/native-object contracts, layout math, OOXML structure checks, hashes, lineage rejection, and status vocabulary | the truth or pedagogy of a scene |
| Flexible | Korean wording, examples, speaker transitions, scene materiality, visual grammar candidates, and the selection of a pattern for a reader task | package repair, schema exceptions, or proof substitution |
| Decisional | why a pattern was selected, why an exception is needed, content-fit review, and `pass_local`/`revise`/`blocked` next action | claiming native runtime success from a render or static audit |

The pattern library is deliberately small and semantic. A project chooses only
the families it needs, for example: `cover`, `question`, `assertion_evidence`,
`relationship_map`, `process_loop`, `comparison_matrix`, `decision_boundary`,
`workshop_board`, and `recap_action`. Pattern identity is not a mandate to use a
single visual template; it is a fixed construction contract for a recurring
semantic job.

## Fresh-family manifest

Before building, create a `pptx-pattern-compiler-manifest.json`. The executable
validator requires these facts:

```yaml
schema_version: 1.0
source_family_id: prompt-engineering-fresh-v10
compiler_version: fixed-pattern-compiler-v1
target_medium: powerpoint
canvas:
  aspect_ratio: 16:9
  width_emu: 12192000
  height_emu: 6858000
source_role: legacy_to_improve | reference_benchmark | no_original
recovery_lineage_policy: reject_as_source
prohibited_lineage: [<recovery/normalization/conversion artifact paths or ids>]
pptx_native_conformance_contract: pptx-native-conformance-contract.json
patterns:
  - id: process_loop
    semantic_job: make a time-ordered feedback loop traceable
    native_types: [shape, connector, text, notes]
    payload_fields: [title, states, transition, speaker_note]
slides:
  - slide_id: S11
    pattern_id: process_loop
    reader_task: trace
    relationship_type: feedback_loop
    source_claim: ''
    pattern_choice_reason: ''
evidence_ledgers:
  structural_package: not_run | pass | fail
  reading_content: not_run | pass | fail
  viewing_render: not_run | pass | fail
  native_runtime: not_run | pass | fail | blocked_by_manual_action
```

The manifest has two important properties.

1. Every slide points to an allowed, declared pattern and records why it fits
   the learner task. LLMs may decide the route but cannot invent an undeclared
   construction while building.
2. `native_runtime` remains independent. It is `pass` only after a fresh
   Microsoft PowerPoint open of the exact candidate hash reports no recovery
   dialog. A static OOXML check, PDF, QuickLook/PNG, image scene-base proof, or
   old open evidence cannot change that state.

### Quick Look attachment-bag gate

Quick Look may expose a PPTX preview as HTML plus a directory of globally named
`Attachment*.pdf` files. That HTML is useful for discovery, but it is **not** a
render proof when attachment references are reused across slide containers or
when a browser-side PDF-to-SVG rewrite changes their stacking context. In that
case a contact sheet can show foreign panels over otherwise unrelated text.

Record that state as `invalid_render_route`, not as a PPTX visual failure and
not as a reason to patch the source layout. Keep `viewing_render: not_proven`.
The next valid route must be a slide-scoped PNG/contact sheet, HTML/SVG
prototype, or manually authorized native render of the exact candidate hash,
with its render command/action packet recorded. A Quick Look attachment
collision is a renderer-evidence failure; it does not authorize a repair, a
PowerPoint re-save, a conversion output, or a claim that the deck is visually
approved.

## Prototype before scale

Create one genuine construction for every selected pattern family. Run static
structure and native-object checks, then perform the manual PowerPoint open
against the prototype exact hash. Only a prototype with `no_recovery_dialog`
may authorize that family for scale. If any prototype changes, its prior render
and native-open proof is stale.

Until manual verification occurs, the project may build a static candidate for
reading and render review, but must report `full_scale_authorized: false` and
`native_runtime: blocked_by_manual_action` or `not_run`. It must not masquerade
as a released deck.

## Evidence is four ledgers, not one grade

| Ledger | Question | Typical evidence | Cannot prove |
| --- | --- | --- | --- |
| `structural_package` | Is this package structurally coherent? | OPC/PresentationML checks, hashes, intent audit | native PowerPoint opening, readability, learning |
| `reading_content` | Does the text convey the intended claim, boundary, and instructional sequence? | outline, extracted text, content review | visual readability or runtime compatibility |
| `viewing_render` | Does a rendered frame show intended hierarchy and relationships? | image contact sheet, HTML/SVG prototype, bounded visual review, image scene-base integration proof | editability or native runtime opening |
| `native_runtime` | Does the exact hash open in PowerPoint without recovery and retain intended native features? | fresh manually recorded open evidence | learning outcome |

One green ledger never turns another ledger green. A recovery incident sets
`native_runtime: fail` for that exact hash and invalidates its use as an
authorization source; it does not falsify the other ledgers.

The native conformance report is part of `structural_package` evidence. It can
show that the intended feature catalog, Pretendard theme, native navigation,
automatic number, text alignment, and raster exception contract match package
observations. It cannot change `native_runtime` to pass.

## Candidate handoff record

Every candidate family records: `source_family_id`, `compiler_version`,
`content_packet_hash`, `pattern_manifest_hash`, `candidate_sha256`,
`fixed_checks`, `flexible_decisions`, and `evidence_ledgers`. This record makes
the pattern compiler reproducible while preserving the distinction between
deterministic construction and contextual teaching judgment.
