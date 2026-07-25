# Retrospective — Fixed System, Open Materiality, Scene Meaning, Localization Reflow (2026-07-13)

## Context

This retrospective distills two comparable visual-authoring contexts and one
new materialization failure.

1. LinkageLab visual review, already recorded in
   `retrospective-design-system-default-bias-20260709.md`: the design system
   became a hidden layout/style default, visual forms converged, and scenes were
   too generic for the content.
2. AI-study business-assumption scenario report in
   `/Volumes/Extend/labs/skillWorks/output/`: the system was consistent and the
   semantic route was explicit, but the user still judged the visual experience
   unsatisfactory and requested high freedom, a fixed design system,
   scene-centered optimization, stronger meaning, and every visual form an LLM
   can generate as a candidate.
3. In the same report, English or abstract labels were translated and made more
   concrete in Korean. Longer phrases changed wrapping and available action
   space, so prior geometry/render evidence could not be reused. The affected
   cards required layout reserve/height correction and a fresh render.

Primary current evidence surfaces:

- `/Volumes/Extend/labs/skillWorks/output/ai-study-business-assumption-scenario-report.html`
- `/Volumes/Extend/labs/skillWorks/output/ai-study-business-assumption-scenario-manifest.md`
- `/Volumes/Extend/labs/skillWorks/output/ai-study-business-assumption-scenario-report.pdf`

## Exact Failure Signals

- A consistent palette, typography, border, and card grammar did not by itself
  create content-specific scenes.
- Reusing the same card/box/arrow silhouette made different semantic jobs feel
  interchangeable.
- Treating visual freedom as a short style list hid the larger candidate space
  available to image-capable LLMs.
- Treating translation as string replacement left previous text-fit, geometry,
  screenshot/PDF, and accessibility evidence stale.
- Label-masked review can test relationship, action, and state change, but it
  cannot require a viewer to infer exact Korean wording, numbers, or conditions.

## Pattern A — N=2 Promotion Signal

**Pattern**: artifact-level design-system lock + open-set visual materiality +
scene-centered semantic packet.

**N=2 evidence**: LinkageLab and the AI-study business-assumption report are
different artifacts with the same boundary failure: system consistency was
confused with repeated layout, while scene specificity and materially distinct
visual expressions were underexplored.

**Promotion decision**: strengthen `visual-authoring` as the domain owner. Do
not create another skill and do not make one visual style a global default.

The system lock freezes style grammar for one artifact:

- token/style namespace
- typography hierarchy
- spacing/density
- component grammar
- status semantics
- accessibility/contrast

The lock does not freeze layout, camera, silhouette, reading path, or visual
material. Materiality is an open set constrained only by source, brand,
license, safety, accessibility, target medium, and production capacity. Every
major semantic unit receives a scene mode, entities/anchors, action/state
change, reader inference/action, visible cue, semantic boundary, deterministic
meaning owner, materiality candidates, selected route, and recovery action.

## Pattern B — N=1 Adaptive Hypothesis

**Pattern**: translation or concretization invalidates affected layout and
render proof, then requires target-medium reflow and revalidation.

**N=1 evidence**: the AI-study report's Korean concretization changed text
length and card geometry. This is sufficient for a local release gate, not for a
portfolio-wide hard rule without another independent context.

**Current treatment**:

- `korean` owns language quality and wording.
- `visual-authoring` owns visible/accessibility materialization, reflow, and
  proof freshness.
- `translated_pending_reflow` and `concretized_pending_reflow` block release.
- Fresh proof must cover the affected target medium, not only an overflow count.

## Three-Layer Ledger

| Layer | This update |
|---|---|
| Fixed | packet fields, route/localization enums, lock id, pending blockers, stale-proof rule, deterministic validator |
| Flexible | actual Korean wording, design-system values, scene direction, open materiality candidates, geometry risks, evidence paths |
| Decisional | candidate selection, route, revise/block/release judgment, whether a real constraint closes materiality |

## Implemented Gates

- `Fixed Design System / Open Visual Materiality / Scene-Centered Meaning Contract`
- `Concrete-Language / Localization Reflow Gate`
- all-route Scene-Centered Meaning Gate before image-only Scene Specificity Gate
- expanded `scene_first_judgement_packet`
- deterministic `validate_scene_materiality_reflow_contract.py`
- checklist, glossary, concept map, routing eval, and interface metadata updates

## Validation Scenarios

1. “디자인 시스템은 고정하되 장면마다 자유롭게, 장면 중심으로 의미를 강화” triggers `visual-authoring`, locks artifact grammar, opens materiality candidates, and requires scene packets across SVG/image/native routes.
2. “이 한 문장만 한국어로 번역” routes to `korean` without the full visual pipeline.
3. Translating visible copy inside an existing report triggers `korean` for wording and `visual-authoring` for reflow; a pending localization state or stale proof blocks release.
4. An abstract SVG process still requires a scene-centered packet, while an image route additionally requires the image Scene Specificity Gate.

## Runtime And Ownership Closure

No new runtime dependency or provider was introduced. The ordinary skill stays
`visual-authoring`; image generation remains owned by `imagegen`, Korean wording
by `korean`, core cognitive metrics by `vector-language-cognition`, and format
building by the target format owners. Runtime compatibility remains
`runtime-delta implemented`.
