# Retrospective — Strategy Sequencing / Prototype / Native Release Evidence

## Context

Two visual-authoring contexts exposed the same process weakness.

1. The 2026-07-09 LinkageLab retrospective found design-system default bias and
   late native-PPTX capability checks.
2. The 2026-07-10 Samsung SDI deck passed render and geometry/native-object
   proxy checks, but a fresh Microsoft PowerPoint open produced a recovery
   dialog. The release proof was therefore fail even though earlier technical
   surfaces looked healthy.

A later Samsung SDI rebuild repeated the same sequencing error after the N=2
written gate existed: the 86-slide artifact was expanded before its expression
families passed content-fit review. This is N=3 recurrence. It justifies an
executable production-boundary stop condition, but it is not evidence that one
project style, diagnostic tactic, or numeric threshold should become a
portfolio-wide default.

## Root Cause

- Completion framing drifted from content fit and proof-surface separation
  toward visible production progress.
- The full artifact was built before a small representative artifact exercised
  each materially different expression/native construction.
- Geometry, object coverage, render, and package checks were allowed to feel
  closer to overall design completion than their evidence supports.
- Binary slide isolation was useful after the failure, but risked being
  mistaken for the authoring method rather than incident response.

## Strategy Improvement

- Keep the universal authoring loop:
  `intent -> content architecture -> Fixed/Flexible/Decisional ledger ->
  expression route -> medium/native plan -> expression-family prototype ->
  full production -> separated proof surfaces -> retrospective`.
- Build a small prototype artifact containing one representative of every
  materially different expression family before full production.
- Record family review and format evidence in a project manifest; require
  `validate_authoring_prototype_gate.py --require-authorized` before scale.
- For native PPTX, require a fresh Microsoft PowerPoint open with
  `no_recovery_dialog` on the prototype and again after the final rebuild.
- Treat Carbon, Vivid, brand systems, editorial systems, and custom systems as
  optional expression tools. Select them only after the content strategy.
- Define improvement by current content, reader task, actionability,
  instructional clarity, intentional editability, and medium stability—not by
  1:1 similarity to a reference benchmark.
- Keep geometry/object-distance calculations as geometry evidence only.

## Incident Boundary

When a proof surface fails, record the exact signal, isolate the smallest
reproduction, fix the production source, regenerate, and rerun every invalidated
proof surface. Do not repair the generated PPTX in PowerPoint and treat that
repaired file as the deliverable. Do not convert a successful forensic tactic
into a design policy without repeated content-independent evidence.

## Carry-Forward Rule

No full slide-deck build is release-candidate until its expression-family
prototype has passed content-fit review and the target-format prototype gate.
For native PowerPoint, that target-format gate includes fresh-open
`no_recovery_dialog`. Final release still requires a fresh check on the final
artifact, and human outcome remains a separate evidence surface.

## Validation Scenarios

| Scenario | Expected behavior |
| --- | --- |
| A 90-slide training deck mixes openers, process maps, charts, exercises, and summaries | Build one representative per actual expression family, assemble a small native PPTX, and pass content-fit plus fresh-open proof before scaling |
| A 6-slide decision brief uses one repeated composition | Use the smallest representative prototype that exercises its real native features; do not invent extra families or a heavyweight benchmark comparison |
| A finished-looking deck triggers a PowerPoint recovery dialog | Mark native release fail, run the incident loop, fix source generation, and rerun stale geometry/native/render/open evidence |

## Three-Layer Closeout

| Layer | Record |
| --- | --- |
| Fixed | content-fit hierarchy, proof-surface separation, expression-family prototype gate, final fresh-open gate, no repaired deliverable |
| Flexible | project expression families, design system, object strategy, prototype composition, thresholds and evidence paths |
| Decisional | prototype sufficiency and `pass_local`/`revise`/`blocked`, citing the Fixed gate and current project evidence |
