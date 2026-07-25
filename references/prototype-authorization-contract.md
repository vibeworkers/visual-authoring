# Expression-Family Prototype Authorization Contract

## Problem and recurrence signal

A written “prototype before scale” rule did not prevent a large deck from
being produced before its expression families had passed content-fit review.
The failure recurred after prior retrospectives, so the owner skill needs an
executable state contract, not another prose-only reminder.

## Fixed / Flexible / Decisional ledger

| Layer | Contract |
| --- | --- |
| Fixed | Content fit precedes format and geometry; proof surfaces stay separate; every materially different expression family is reviewed before scale; native PPTX prototypes receive a fresh PowerPoint open with no recovery dialog. |
| Flexible | Project SoT, expression-family names, representative slides, content jobs, chosen/rejected expressions, native plans, artifact paths, and target format. |
| Decisional | `pass_local`, `revise`, `blocked`, or `needs_human_choice`, with the Fixed rule, current Flexible evidence path, and next action. |

## Code / LLM boundary

Code validates manifest structure, canonical content-fit dimension coverage,
expression-family coverage, rationale specificity, evidence-path existence,
prototype render evidence, format-gate evidence, and authorization consistency.
Code must reject `full_scale_authorized: true` when any required condition is
false. Repeating one generic rationale across materially different families is
not content-fit traceability and is rejected.

The author/reviewer judges whether the content job, relationship, chosen
expression, hierarchy, density, and native plan fit the current material. That
judgment is bounded to observable content-fit evidence and never becomes a
claim of learner comprehension or learning outcome without human evidence.

## Manifest and command

The project owns a JSON manifest with these top-level fields:

- `version`, `artifact_type`
- `fixed`
- `flexible.project_sot` and `flexible.expression_families`
- `format_gate`
- `content_fit_review`
- `decisional`
- `full_scale_authorized`

Each expression family records `family`, `representative_slide`, `content_job`,
`relationship`, `chosen_expression`, `choice_rationale`,
`rejected_alternative`, `native_plan`, `prototype_artifact`, and
`review_status`. The content-fit review records `reviewer_role`, `review_method`,
and an existing `evidence_path`.

The Fixed hierarchy uses these canonical dimension IDs in this order:

1. `content_task_action`
2. `semantic_relationship_hierarchy`
3. `medium_editability_intent`
4. `geometry_accessibility_reproducibility`
5. `render_package_native_open`
6. `human_outcome_evidence`

```bash
scripts/visual-authoring-runtime run scripts/validate_authoring_prototype_gate.py project-gate.json
scripts/visual-authoring-runtime run scripts/validate_authoring_prototype_gate.py project-gate.json --require-authorized
```

The first command validates the record even when the current status is
`revise`. The second is the mass-production blocker and returns non-zero until
the gate is authorized.

## Rubric

### Must

- The family list is derived from the project, not a global template.
- Every family has one representative and explicit content-fit reasoning.
- The project SoT, every prototype artifact, and content-fit review evidence exist.
- Content-fit review names the reviewer role and review method.
- Authorization remains false while any family is not `pass_local`.
- PPTX authorization remains false without prototype render review and fresh
  PowerPoint `no_recovery_dialog` evidence.
- Geometry, object distance, XML, and render evidence are not promoted to
  content-fit or human-outcome proof.

### Should

- The prototype is the smallest artifact that exercises every materially
  different semantic and native construction.
- Rejected alternatives explain the content relationship they would obscure,
  not merely a style preference.
- A rebuild makes prior render/native/open evidence stale.
