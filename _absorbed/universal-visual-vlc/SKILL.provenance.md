---
name: universal-visual-vlc
description: >
  시각화, 장표, PPTX/PDF/HTML 설명 자료, 인포그래픽, 다이어그램, 이미지-first
  semantic schema, visual storytelling, 브로셔형 랜딩, 교육/제안서/보고서 시각 자료,
  dashboard/app 설명 자료, "시각화가 어렵다", "상징이 불명확하다",
  "한눈에 이해되는가", "고품질 slide인가" 같은 요청을 제작 전에 검토하는
  Universal Visual VLC ordinary skill. Surface VLC Gate를 visual/storytelling
  adapter로 사용해 언어 단위, 목표, 맥락, scene-first packet, image-required
  route gate, target profile, human-outcome boundary를 분리하고, 시각화 관련
  요청은 일단 review gate로 잡는다.
metadata:
  display-name: Universal Visual VLC
  short-description: Visual/storytelling review gate for Surface VLC
  cogarch-role: visual-review-gate
  runtime-compatibility: runtime-delta implemented
---

# universal-visual-vlc

## Rubric (Must/Should)

### Must

- Follow local `AGENTS.md` before implementing, validating, or exporting outputs from this skill.
- Preserve the skill's declared workflow, receiver contract, and verification path.

### Should

- Keep outputs concise, evidence-backed, and aligned with the intended receiver level.

## Purpose

`universal-visual-vlc` is the ordinary skill surface for visual/storytelling review in the `cogarch` system.

It does not replace image generation, slide authoring, PDF export, or human validation. It reviews whether a visual artifact or planned visual artifact has enough language/context/goal structure to proceed to the next production, format, or human-outcome gate.

Core identity:

- Core gate: `Universal Surface VLC` / `Surface VLC Gate`.
- Visual adapter alias: `Universal Visual VLC`.
- Official image-required gate: `scene_first_judgement_packet` -> `image_production_manifest` -> `deterministic_semantic_layer` -> `delivery/profile validation`.
- Execution tools: `/Volumes/Extend/cogarch/tools/surface_vlc_gate.py` and `/Volumes/Extend/cogarch/tools/run_surface_delivery_gate.py`.
- Generic design SoT: `/Volumes/Extend/cogarch/docs/20260507_universal_vlp_surface_proxy_gate_design.md`.
- Visual adapter design SoT: `/Volumes/Extend/cogarch/docs/20260507_vlp_visual_quality_tool_design.md`.

External SoT pointer: review theory is defined in `/Volumes/Extend/cogarch/docs/20260507_universal_vlp_surface_proxy_gate_design.md` and visual adaptation is defined in `/Volumes/Extend/cogarch/docs/20260507_vlp_visual_quality_tool_design.md`.

## When To Use

Use this skill whenever the user asks about or is about to produce a visual surface.

Trigger examples:

- "시각화", "visualization", "visual storytelling", "인포그래픽", "다이어그램", "키비주얼".
- "장표", "slide", "PPTX", "PDF 장표", "브로셔", "랜딩", "교육 자료", "제안서".
- "한눈에 이해", "상징이 불명확", "시각화가 어렵다", "영화처럼", "몰입", "고품질 slide".
- Image-first workflows that later become HTML/PPTX/PDF.
- Existing visual artifacts that need review before release or iteration.

Default rule:

- If the request is visual-related, first create or request a `visual_vlc_review_packet`.
- Do not go straight to image generation, SVG/Carbon, PPTX, PDF, or HTML rendering unless the review gate is explicitly out of scope.
- If the user only asks for pure image generation and no quality, understanding, slide, document, or release claim is made, keep this skill as a lightweight preflight and hand execution to `imagegen`.
- If the request includes a slide/deck/document visual that should be understandable, memorable, cinematic, realistic, or externally publishable, decide `route_status` before production. A route that is `ROUTED_IMAGE_REQUIRED` cannot close with SVG-only proxy art.

## Inputs

Minimum review packet:

```yaml
visual_vlc_review_packet:
  source:
  artifact_type: slide | pptx | pdf | html | markdown | semantic_schema | dashboard | image_prompt | storyboard | other
  surface_role: explain | decide | teach | propose | govern | operate | record | converse
  goal_text:
  requested_claim:
  target_profile:
  audience_or_operator:
  constraints:
    - string
  external_evidence:
    scene_first:
    image_production_manifest:
    target_profile:
    file_format:
    screenshot:
    human_outcome:
```

If `source` or `goal_text` is missing and the request cannot be reviewed without inventing it, ask one bundled clarification question. Otherwise proceed with `TODO/unknown` and mark the gate as `hypothesis only` or `candidate`.

## Review Flow

1. **Bound the claim**.
   - Separate `observable proxy`, `inferred risk`, and `human outcome claim`.
   - Human understanding, persuasion, immersion, transfer, or edit success cannot be passed by this skill alone.
2. **Map to Surface VLC**.
   - Convert or describe the artifact as language-bearing units with context and goal anchors.
   - Keep `target_profile`, scene packet, screenshots, and file-format evidence as external gates, not core metric names.
3. **Run the applicable gate**.
   - Use `surface_vlc_gate.py` for language/context/goal proxy review.
   - Use `run_surface_delivery_gate.py` when slide/PDF/HTML delivery profile evidence is part of the requested claim.
   - If no source file exists, produce a structured preflight packet and route the smallest missing evidence.
4. **Return a bounded decision**.
   - Allowed labels: `usable`, `candidate`, `blocked`, `hypothesis only`.
   - Never report `human_pass`, `high_quality_slide_pass`, or `cinematic_pass` without the required external evidence.
5. **Route execution**.
   - Scene/image production: `creator-agent`, `imagegen`, `geo-carbon-visual-integrator`.
   - Slides/PPTX: `presentations`, `hybrid-slide-pipeline`, `hybrid-deck-factory`.
   - Documents/PDF/HTML: `documents`, `doc-converter`, `pdf`, target-format owner.
   - Core VLP metric/schema/validator changes: `vector-language-cognition`.
6. **Close or block the image-required route**.
   - If `route_status=ROUTED_IMAGE_REQUIRED`, require preserved image output, prompt/source ledger, integration evidence, and verification evidence before calling the visual production loop done.
   - If the route is `SVG_PROXY_ONLY` or `BLOCKED_IMAGEGEN`, do not mark the production loop `usable` for visual quality. Return `candidate`, `blocked`, or `hypothesis only` with a recovery owner.

## Official Image-Required Route Gate

Use this gate for every visual/storytelling slide, explainer, public document, key visual, diagram, or landing surface where the claim depends on concrete visual recognition, affective scene-setting, or cinematic immersion.

Allowed `route_status` values:

- `CLASSIFICATION_PENDING`: source/goal/scene is not yet stable enough to route.
- `SVG_ALLOWED`: the visual claim is structural, abstract, or data/diagram-first; deterministic SVG/HTML/Carbon may be the primary visual.
- `ROUTED_IMAGE_REQUIRED`: the surface needs generated/photographic/illustrated image material as the base scene.
- `IMAGE_ASSET_PRESENT`: a preserved image exists, but integration or validation is not yet closed.
- `INTEGRATED_HYBRID`: image base layer and deterministic semantic layer are both present in the target format.
- `SVG_PROXY_ONLY`: SVG/vector marks are being used where a concrete image scene is required. This is a failed close state, not an acceptable delivery state.
- `BLOCKED_IMAGEGEN`: image generation is required but unavailable because of model/tool/credential/policy/runtime constraints.

When `route_status=ROUTED_IMAGE_REQUIRED`, the closeout must include:

```yaml
image_production_manifest:
  product_anchor: ChatGPT Images 2.0 | OpenAI image API | local image source | stock/source image | other
  model_or_source:
  output_form_slug: photorealistic-natural | illustration-story | infographic-diagram | logo-brand
  prompt_or_source_ledger:
  image_output_path:
  integration_path:
  verification_path:
  deterministic_semantic_layer:
    owner: svg | html | pptx | carbon | other
    controls:
      - exact Korean labels
      - arrows and attention path
      - evidence callouts
      - accessibility/contrast/readability
  read_tests:
    three_second_read:
    five_second_proxy:
    label_hidden_thumbnail:
  human_outcome_validation: not_run | candidate | conditional | pass
```

The base image owns scene, atmosphere, concrete objects, texture, and recognizability. The deterministic semantic layer owns exact Korean text, labels, arrows, evidence, citations, ordering, and final presentation constraints. Do not ask image generation to be the source of truth for exact labels or research claims.

Completion rule:

- `INTEGRATED_HYBRID` with evidence may be `candidate` or `usable` depending on proxy results.
- `SVG_ALLOWED` may be `usable` only when the visual claim is explicitly structural/diagrammatic.
- `SVG_PROXY_ONLY` and `BLOCKED_IMAGEGEN` cannot be reported as `Done`, `cinematic_pass`, `high_quality_slide_pass`, or `human_pass`.
- Human comprehension, persuasion, immersion, or learning transfer claims remain `not_run`, `candidate`, or `conditional` until actual human evidence exists.

## CLI Use

For a general surface proxy review:

```sh
python3 /Volumes/Extend/cogarch/tools/surface_vlc_gate.py \
  --source /path/to/artifact.md \
  --artifact-type markdown \
  --surface-id my-surface \
  --surface-role explain \
  --goal-text "what the viewer should understand or do" \
  --requested-claim candidate_for_share \
  --external-gate scene_first \
  --external-gate target_profile \
  --out-dir /Volumes/Extend/cogarch/runs/run-YYYYMMDD-my-surface-vlc
```

For combined Surface VLC + delivery profile review:

```sh
python3 /Volumes/Extend/cogarch/tools/run_surface_delivery_gate.py \
  --source /path/to/artifact.html \
  --artifact-type html \
  --surface-id my-surface \
  --surface-role explain \
  --goal-text "what the viewer should understand or do" \
  --profile web_scroll_surface \
  --requested-claim candidate_for_share \
  --external-evidence /path/to/screenshot-or-format-evidence.json \
  --out-dir /Volumes/Extend/cogarch/runs/run-YYYYMMDD-my-surface-delivery
```

## Output Contract

Return or write the review result in this shape:

```yaml
visual_vlc_review_result:
  decision: usable | candidate | blocked | hypothesis only
  route_status: CLASSIFICATION_PENDING | SVG_ALLOWED | ROUTED_IMAGE_REQUIRED | IMAGE_ASSET_PRESENT | INTEGRATED_HYBRID | SVG_PROXY_ONLY | BLOCKED_IMAGEGEN
  claim_boundary:
    observable_proxy:
    inferred_risk:
    human_outcome_claim:
  image_production_manifest:
  evidence_paths:
    - path
  failed_conditions:
    - condition
  recovery_action:
  next_owner:
```

Audience-facing artifacts should not expose internal method labels by default. Use this contract for internal review, run reports, and handoff only.

## Boundaries

- This skill is a review gate, not a visual production engine.
- This skill can support `candidate_for_share`; it cannot prove actual human comprehension or persuasion.
- This skill owns the official decision of whether a visual surface must route to image production before deterministic SVG/Carbon/PPTX/HTML integration.
- `Universal Surface VLC` core metric names stay generic. New contexts add adapters and profile contracts, not new domain-specific core scores.
- `Universal Visual VLC` owns visual/storytelling review routing. `vector-language-cognition` owns core VLP metric/schema/validator changes.
- `cogarch` coordinates umbrella entry and monitors ownership drift; it does not replace this skill's visual review gate.

## Runtime Compatibility

Closure state: `runtime-delta implemented`.

- Runtime-local adapter is explicitly owned by this `cogarch` workspace.
- Tool paths are fixed local adapters: `/Volumes/Extend/cogarch/tools/surface_vlc_gate.py` and `/Volumes/Extend/cogarch/tools/run_surface_delivery_gate.py`.
- If those tools are unavailable, do not fabricate a score. Return a structured `visual_vlc_review_packet` and mark the runtime gate `blocked`.
- No new model dependency is introduced by this skill package.

## Rubric

### Must

- Visual-related requests are treated as review-gate candidates before production.
  - Evidence: `When To Use` and `Review Flow`.
- The skill preserves `Universal Surface VLC` core and `Universal Visual VLC` adapter separation.
  - Evidence: `Purpose` and `Boundaries`.
- The skill keeps proxy evidence separate from human outcome claims.
  - Evidence: `Review Flow`, `Output Contract`, and `Boundaries`.
- The skill routes production and core metric changes to specialist owners.
  - Evidence: `Review Flow`.
- Image-required visual claims cannot close as SVG-only proxy work.
  - Evidence: `Official Image-Required Route Gate`.
- Every `ROUTED_IMAGE_REQUIRED` closeout includes preserved image, ledger, integration, and verification evidence.
  - Evidence: `Official Image-Required Route Gate` and `Output Contract`.
- Runtime compatibility is closed with exactly one state.
  - Evidence: `Runtime Compatibility`.

### Should

- Prefer executable CLI evidence when a source file exists.
- Preserve target-profile and file-format evidence as external gates.
- Keep audience-facing artifacts free of internal method labels unless requested.
- Return the smallest recovery action when `blocked`.
- Prefer `imagegen` or preserved image sourcing for concrete scene bases, then deterministic SVG/HTML/PPTX/Carbon for exact labels and meaning.

## References

- `/Volumes/Extend/cogarch/docs/20260507_universal_vlp_surface_proxy_gate_design.md`
- `/Volumes/Extend/cogarch/docs/20260507_vlp_visual_quality_tool_design.md`
- `/Volumes/Extend/cogarch/tools/surface_vlc_gate.py`
- `/Volumes/Extend/cogarch/tools/run_surface_delivery_gate.py`
- `/Volumes/Extend/.codex-relocated/skills/cogarch/SKILL.md`
- `/Volumes/Extend/.codex-relocated/skills/generate-skill/references/global-skill-management.md`
- `/Volumes/Extend/.codex-relocated/skills/universal-visual-vlc/references/image-required-route-gate.md`
- `/Volumes/Extend/.codex-relocated/skills/vector-language-cognition/SKILL.md`
