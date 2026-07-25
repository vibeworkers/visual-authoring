# Source Notes

This reusable skill was distilled from a project-local document and slide authoring system in the AX-Groups training workspace.

The global skill keeps only the reusable architecture:

- representative agent routing
- local skill module shape
- cognitive document/visual authoring packet shape
- working-source clarification, conflict priority, and fixed/flexible/decisional classification
- semantic-fit and unfolding repair gate
- outline-notes gate before storyline review, visualization, or PPTX build
- intentional or intentionally unconstrained visual value specification
- PPTX standard XML generation helper boundary
- compatible npm authoring route shape
- writing and visualization split
- storyline/readability gate between writing and visualization
- session-feedback pattern gate
- semantic-staging design gate that preserves design freedom
- artifact-surface separation gate
- routing experiment shape
- open visualization planning and semantic variable rule
- PresentationML and PowerPoint workflow boundaries
- repeated issue and release gate separation
- deterministic scaffold and check scripts

The global skill does not copy project deck content, recovered PPTX files, audience-specific manual text, or target-specific audit files. Those remain in the target project.

## Working Source And Surface Distillation Boundary

`references/session-feedback-and-surface-gates.md` distills repeated review
patterns and artifact-surface boundaries into reusable checks. It does not make
one project's course deck, version label, feedback thread, or delivery folder a
global dependency.

Reusable:

- working source of truth and clarification fields
- conflict-resolution priority order
- fixed/flexible/decisional classification
- recurring feedback checks for title story, decorative load, metadata
  relevance, regulated-domain boundaries, citation links, table/prose fit, and
  prompt knowledge structure
- outline notes as a production-source surface when PPTX work needs story,
  spoken flow, evidence, and visual intent before generation
- staging-design brief fields for scene beat, attention entry, curiosity gap,
  reading path, listening cue, evidence reveal, semantic variables,
  accessibility/load, design-freedom boundary, open expression options,
  selected-expression rationale, and avoid-unnecessary-constraints decisions
- design-freedom boundary that keeps predefined style kits, templates, layout
  families, palettes, images, icons, motifs, animations, and typography scales optional
  unless the target project supplies a real constraint or a stated rationale
- artifact surface roles for learner-facing, instructor/facilitator, production
  source, evidence/fact table, render/native proof, and delivery handoff
- routing experiment shape with should-trigger, should-not-trigger, and
  near-miss cases

Not reusable:

- one project's exact comments
- one project's deck titles or visual style
- one project's output filenames
- one project's student data or source tables
- one project's internal version names unless a target project adopts them
  explicitly

## Cognitive Authoring Distillation Boundary

`references/cognitive-authoring-process.md` distills a project-local
`cognitive-document-visual-authoring` process into reusable packet fields,
stage gates, and validation expectations. The action is `distill + validate`,
not a runtime dependency merge.

Reusable:

- `cognitive-document-visual-authoring-v1` process lock
- R/P/M/W/A authoring stages
- reader situation, cognitive task, desired action, and semantic fit
- folded-unit diagnosis and unfolding trace
- declarative/procedural/situational knowledge split
- visual value spec for design intent, reader-path support,
  readability/accessibility, native medium constraints, chosen values, and
  intentionally unconstrained areas

Not reusable:

- one project's lecture content
- local survey data
- local PPTX artifacts
- local audit filenames unless the target project adopts them explicitly
- project-specific audience claims without target evidence

## PPTX Standard XML Tooling Boundary

`references/pptx-standard-xml-generation.md` distills local standard-PPTX
tooling into a reusable generation and validation contract.

Reusable:

- helper-based generation surface such as `pptxgenjs_helpers`
- compatible npm process order: `system:init`, `system:run`, `build`,
  PresentationML/native/research checks, recovery comparison, repetition gate,
  manual PowerPoint open check, release check, and agent-system check
- compatible npm state outputs: `09-system-state.json`,
  `10-system-runbook.md`, and `11-release-packet.md`
- new-PPTX build over recovered-artifact patching
- native editable object expectations
- ECMA-376/OPC/DrawingML/MS-PPTX validation families
- release-status acceptance limited to `pass` and
  `pass_superseded_old_recovery_artifacts`
- rebuild invalidation rule: a PPTX rebuild after manual open check makes that
  open evidence stale
- separate `pptx-standard-xml-build`, `native-powerpoint-check`,
  `presentationml-spec-check`, and `manual-powerpoint-open-check` evidence

Not reusable:

- one project's downloaded spec cache
- one project's generated PPTX files
- one project's exact helper implementation unless intentionally copied into the
  target project
- final release claims without a target-environment PowerPoint open check
- final release claims from a manual open check recorded before the current PPTX
  build

## Slide Authoring Research Boundary

`references/slide-authoring-methods.md` distills reusable guidance from slide
headline, assertion-evidence, multimedia learning, cognitive-load, text
structure, and practitioner presentation-writing sources. It does not make any
one project deck, title list, or learner outcome part of this global skill.

The global reusable rule is the gate shape: title-only story, assertion-evidence,
one-beat, 5-second scan, cognitive-load, evidence-boundary, and human-outcome
claim separation. Project-specific titles, lesson timelines, source IDs, and
audit files remain local to the target project.

## Semantic Staging Design Boundary

`references/semantic-staging-design-framework.md` distills reusable visual
staging decisions from the authoring workflow. It does not promote any design
kit, brand kit, template, motif, palette, image method, icon style,
animation plan, or typography scale into the directing layer for a deck.

Reusable:

- `staging-design-brief.json` before open visualization planning or PPTX build
- scene beat, attention entry, curiosity gap, reading path, listening cue, and
  evidence reveal as explicit production decisions
- semantic variables, accessibility/load, design-freedom boundary, open
  expression options, selected-expression rationale, and
  avoid-unnecessary-constraints fields
- constraint truthfulness boundary: style choices remain optional unless tied to
  audience, evidence, medium, accessibility, brand, license, production, or
  native-PPTX constraints

Not reusable:

- one project's decorative motif
- one project's exact slide style
- one project's style kit, brand, template, motif, palette, image, icon,
  animation, or typography choices
- claims that the visual staging improved learning without target human evidence

## Source And License Boundary

Treat this as an internal workspace skill unless the user explicitly asks to package it for external distribution. Before external distribution, review project-specific names, local paths, and any source material license obligations.

## PowerPoint Boundary

The checker can prove structure. It cannot prove that Microsoft PowerPoint will open a generated PPTX without a recovery dialog. That claim requires a fresh human or automation-backed PowerPoint open check in the target environment.

---

## visual-authoring 병합 provenance (2026-07-07)

- 흡수 소스 5종: document-slide-authoring-agent-system, ggaca-authoring, universal-visual-vlc, visual-implementation, geo-carbon-visual-integrator — 전체 스냅샷은 `../_absorbed/`
- Vivid 토큰 프로파일(`--viv-*`)과 `design-systems.md` 선택 루브릭은 2026-07-07 신규 저작(선례: tokens-css.md 구조).
- geo 계열 파일명 변경: process.md→visual-normalization-process.md, rubric-design.md→visual-rubric-design.md, gate-conditions.md→visual-gate-conditions.md
