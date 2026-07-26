---
name: document-slide-authoring-agent-system
description: Scaffold and validate a reusable modular agent and skill system for cognitive document/visual authoring, working-source clarification, course-flow to slide-planning to symbol-inventory to semantic-design-system sequencing, layout element tradeoff/placement/front-back-order calculation, semantic-fit gates, outline-note gates before PPTX work, evidence-backed storyline/readability gates, semantic-staging design gates that preserve design freedom, image-first semantic-fit visualization, VLPP expression-distance monitoring, session-feedback pattern gates, artifact-surface separation, compatible npm authoring flows, PPTX, open visualization planning, PresentationML compliance, and PowerPoint release gates across projects.
metadata:
  display-name: Document Slide Authoring Agent System
  runtime-compatibility: shared-core only / no-delta
  source-kind: distilled reusable skill
---

# Document Slide Authoring Agent System

Use this skill when a project needs a reusable modular agent system for document writing, slide planning, cognitive document/visual authoring, working-source clarification, whole-course-flow mapping, slide planning by learning situation and learner action, symbol inventory, semantic design-system construction, layout element calculation, semantic-fit checks, mandatory outline notes before PPTX work, evidence-backed storyline/readability checks, semantic-staging design that preserves design freedom, image-first semantic-fit visualization, VLPP expression-distance monitoring, session-feedback pattern gates, artifact-surface separation, compatible npm authoring flows, open visualization planning, native PPTX generation, PresentationML compliance, repeated-issue gates, and Microsoft PowerPoint open-check release boundaries.

## Trigger Contract

Use this skill when the user asks to:

- make the document/slide authoring agent system usable outside one project
- create a representative agent for a slide or PPTX authoring workflow
- lock the working source of truth, clarification packet, conflict priority, and fixed/flexible/decisional classification before authoring
- enforce the file-order dependency `course-flow-map.md -> slide-planning-map.json -> symbol-inventory.json -> semantic-design-system.json` before visual design or PPTX build
- prevent a design system, template, palette, motif, or style kit from being fixed before the whole lecture flow, slide plan, and symbol inventory exist
- require each slide to state `visual_situation`, `cognitive_operation`, `learner_action`, `output_artifact`, timing, evidence boundary, and reuse policy
- require each layout element to calculate `element_tradeoff` (거래), `placement` (배치), `front_back_order` (앞뒤 순서), reading order, native object order, and overlap risk before PPTX object placement
- create a cognitive authoring packet before drafting, slide design, report writing, or visualization
- make context, topic, purpose, reader problem, desired action, and evidence boundary fit before wording or visual form is chosen
- repair weak or folded content by asking cognitive-task-analysis style questions and unfolding the hidden judgment, constraint, or action
- require outline notes that connect audience situation, section flow, visible message, spoken notes, evidence, and visual intent before a PPTX build begins
- require a semantic-staging design brief when a deck needs attention, curiosity, guided reading, spoken flow, evidence reveal, action exit, and explicit design-freedom boundaries
- record intentional or intentionally unconstrained visual values without forcing a predefined style kit, template, layout family, palette, fixed image-generation method, icon style, animation plan, or typography scale
- create image-first visual candidates or contact sheets before HTML/PPTX implementation when visual direction, density, or expression fit must be inspected
- monitor visual candidates with VLPP as computed distance between target symbolic expression and rendered expression, not as psychological interpretation or learner-outcome proof
- scaffold modular local skills for writing, visualization, PPTX build, PresentationML, repetition gates, or PowerPoint open checks
- include a compatible npm authoring flow with `system:init`, `system:run`, build, PresentationML/native checks, recovery comparison, manual PowerPoint open check, release check, and agent-system check
- validate that a project has agent, skill, tool, workflow, and release gate wiring
- turn repeated review comments into reusable checks for title story, expression naturalness, decorative load, internal metadata relevance, legal/regulated-domain AI boundaries, citation links, table/prose fit, and prompt knowledge structure
- separate learner-facing artifacts, instructor/facilitator artifacts, production source, evidence/fact tables, render/native proof, and delivery handoff before closeout
- test routing with should-trigger, should-not-trigger, and near-miss examples before treating the reusable system as stable
- preserve the PPTX standard XML generation boundary between helper-based generation, PresentationML/OPC validation, native editability checks, and Microsoft PowerPoint open evidence
- prevent a fresh PowerPoint open check from being reused after a PPTX rebuild
- prevent repeated PowerPoint recovery errors from being treated as solved by zip/XML checks alone
- prevent learner-facing decks from passing release review without title-only story, assertion-evidence, one-beat, scan, cognitive-load, and evidence-boundary checks

Do not use this skill for:

- a one-off wording rewrite for a slide
- simple PPTX generation where no reusable agent system is requested
- Canva-only or Google Slides-only work that does not involve this native PPTX workflow
- a single visual-style recommendation with no reusable document/slide authoring workflow
- unrelated project governance that has no document, slide, or presentation workflow

## Operating Modes

### Scaffold

Create the portable agent-system files inside a target project:

```bash
node ~/.cogarch/skills/document-slide-authoring-agent-system/scripts/portable_agent_system.js scaffold /path/to/project
```

This writes:

- `authoring-agent-system.json`
- `authoring_agent_system.js`
- `agent-system/README.md`
- `agent-system/skills/*/SKILL.md`

By default existing files are not overwritten. Use `--force` only when the target files are generated or explicitly replaceable.

### Check

Validate an existing target project:

```bash
node ~/.cogarch/skills/document-slide-authoring-agent-system/scripts/portable_agent_system.js check /path/to/project
```

The checker writes `authoring-agent-system-audit.json` in the target project. A structural pass means the agent system is wired. It does not mean a PPTX is releasable in Microsoft PowerPoint.

### Local Target Check

After scaffolding, a project can run its own checker:

```bash
cd /path/to/project
node authoring_agent_system.js
```

If the project has `package.json`, add an equivalent local script only after confirming that package ownership allows the edit.

### Compatible NPM Authoring Process

Use this route when the target project exposes the compatible authoring scripts.
The sequence is part of the release contract, not a loose example:

```bash
cd /Volumes/Extend/lecture-works/AX-Groups/AX/Training/.work/agentic_paradigm_editable
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

`system:run` must produce:

- `09-system-state.json`
- `10-system-runbook.md`
- `11-release-packet.md`

The build must produce `Document_Slide_Authoring_System_new.pptx`.
The manual check must write
`manual-open-checks/latest-powerpoint-open-check.json` with
`result: no_recovery_dialog`, and that check must be newer than the PPTX build.
Accepted release statuses are `pass` and
`pass_superseded_old_recovery_artifacts`.

Do not run `npm test` after the fresh PowerPoint open check unless the open
check will be repeated. In this compatible route, `npm test` can rebuild the
PPTX, which invalidates the previous PowerPoint open evidence.

## Working Source Of Truth And Clarification Intake

Before drafting, visual planning, or PPTX generation, fix the current working
source of truth. The reusable system must name:

- `goal`
- `scope`
- `excluded_surfaces`
- `working_source_of_truth`
- `success_condition`
- `evidence_target`
- `runtime_target`
- `provider_provenance`
- `output_brand`

If the source set is incomplete, do not fill the gap with generic assumptions.
Mark it as `TODO`, `question`, `uncertain`, or `blocked`, then keep the workflow
inside the verified scope.

## Conflict Resolution

When requirements conflict, resolve them in this order:

1. the user's latest explicit requirement
2. project `AGENTS.md` and workspace source of truth
3. target artifact role and audience
4. source evidence and license boundary
5. native tool and release constraints
6. general style preferences

Record the lower-priority item as deferred, `blocked`, or target-specific instead
of silently blending it into the output.

## 3-Layer Classification

Every reusable workflow change must classify decisions into three layers:

- `Fixed`: workflow order, release gates, artifact surface roles, evidence
  labels, runtime compatibility status.
- `Flexible`: wording, examples, visual tone, layout expression,
  project-specific filenames.
- `Decisional`: audience action, claim strength, evidence sufficiency, surface
  inclusion/exclusion, manual release status.

A flexible adaptation cannot change fixed workflow gates or decisional claim
boundaries without an explicit version bump and routing experiment.

The scaffold/checker must enforce this split. A target system fails validation
when the workflow order is missing or reordered, when the three layers are not
declared, or when important implementation values are not traceable to semantic
role, reader situation, medium constraint, safe area, readable size, density,
scan path, or action exit.

## Course Flow To Design System Dependency

Do not start a lecture-slide project by choosing a design system, template,
palette, motif, or style kit. The reusable sequence is fixed:

1. `course-flow-map.md`: the whole lecture flow, fixed schedule, module sequence,
   session timing, learning arc, output chain, and non-goals.
2. `slide-planning-map.json`: every slide's source module, slide goal,
   visual situation, cognitive operation, learner action, output artifact,
   timing budget, evidence boundary, and reuse policy.
3. `symbol-inventory.json`: symbols that can carry the planned meanings,
   including semantic role, source context, target expression vector, possible
   confusion, visual candidates, selection reason, and learner-facing boundary.
4. `semantic-design-system.json`: design principles, symbol mapping, layout
   families, typography rules, color logic, image style rules, PPTX element use,
   layout element calculations, accessibility/density, calculated values, and
   implementation trace.

`semantic-design-system.json` must be derived from the first three files. It is
not a place to import a ready-made visual taste unless the project has a real
brand, accessibility, medium, or delivery constraint that requires it.

Every layout element that reaches PPTX placement must include:

- `element_id`
- `semantic_role`
- `element_tradeoff`: the attention cost and space cost paid for the semantic gain
- `attention_cost`
- `space_cost`
- `semantic_gain`
- `placement`
- `front_back_order`
- `reading_order`
- `native_object_order`
- `overlap_risk`

## Agent Architecture

The scaffolded system uses this representative-agent chain:

1. `representative-agent`
2. `evidence-intake-agent`
3. `cognitive-authoring-agent`
4. `writing-agent`
5. `storyline-readability-agent`
6. `session-feedback-agent`
7. `visualization-agent`
8. `pptx-build-agent`
9. `artifact-surface-agent`
10. `presentationml-compliance-agent`
11. `repetition-gate-agent`
12. `powerpoint-open-check-agent`

The corresponding local skills are:

- `evidence-freeze-skill`
- `working-source-clarification-skill`
- `ziphyun-particle-research-skill`
- `cognitive-document-visual-authoring-skill`
- `writing-flow-skill`
- `storyline-readability-gate-skill`
- `session-feedback-pattern-gate-skill`
- `semantic-staging-design-skill`
- `visualization-flow-skill`
- `pptx-native-build-skill`
- `drawingml-table-anchor-sanitizer-skill`
- `artifact-surface-separation-skill`
- `presentationml-compliance-skill`
- `repetition-release-gate-skill`
- `powerpoint-human-open-check-skill`
- `routing-experiment-gate-skill`

## Process

Follow this order:

1. Freeze evidence, source inventory, uncertainty, and research bundle.
2. Lock the working source of truth, clarification packet, conflict priority, and fixed/flexible/decisional classification.
3. Build `course-flow-map.md` before slide planning: whole lecture flow, fixed schedule, module sequence, session timing, learning arc, output chain, and non-goals.
4. Normalize research into corpus, particles, concept map, and Ziphyun handoff where relevant.
5. Build the cognitive authoring packet: reader situation, cognitive task, desired action, semantic fit, evidence boundary, output route, and verification surface.
6. Repair weak or folded content with the unfolding loop: folded unit, weakness diagnosis, cognitive-task-analysis probes, unfolding trace, and reader-facing rewrite.
7. Write brief, seed, MCII, outline, outline notes, slide specs, and reader judgment from the authoring packet.
8. Run the outline-notes gate before storyline, visualization, or PPTX work continues.
9. Build `slide-planning-map.json` before symbol collection: slide goal, visual situation, cognitive operation, learner action, output artifact, timing budget, evidence boundary, and reuse policy.
10. Run the storyline/readability gate before visualization: title-only story, assertion-evidence, one-beat, 5-second scan, cognitive-load, and evidence-boundary checks.
11. Run the session-feedback pattern gate so repeated review comments become reusable checks before more visual work.
12. Build `symbol-inventory.json` before design-system work: symbols, semantic roles, target-expression vectors, possible confusion, visual candidates, selection reasons, and learner-facing boundary.
13. Build `semantic-design-system.json` from the course-flow map, slide-planning map, and symbol inventory. Do not fix a design system before those files exist.
14. Calculate layout element tradeoff, placement, front/back order, reading order, native object order, and overlap risk before PPTX object placement.
15. Run the semantic-staging design framework gate when visual direction must support attention, curiosity, reading path, spoken flow, evidence reveal, and action exit without forcing a predefined style.
16. Produce image-first visual candidates or a contact sheet when visual direction is unsettled, before HTML/PPTX implementation.
17. Run VLPP expression-distance monitoring on candidate visuals when a calculable target-expression vector is useful. Treat this as symbolic distance observation, not a psychological reading of learners.
18. Run open visualization planning before PPTX implementation.
19. Convert chosen visual decisions, real medium/accessibility constraints, and intentionally unconstrained areas into explicit semantic variables and visual value specs.
20. Generate compatible npm system state, runbook, and release packet when the target project exposes that route.
21. Generate a new editable PPTX through standard XML-aware helpers instead of repairing a recovered PPTX.
22. Validate PresentationML, OPC relationships, DrawingML anchors, content types, notes, theme, custom layout, and native editable objects.
23. Separate learner-facing, instructor/facilitator, production source, evidence/fact table, render/native proof, and delivery handoff surfaces.
24. Run the repeated-issue and recovery-comparison gate.
25. Keep Microsoft PowerPoint open-check evidence as a separate manual release gate.
26. Run routing experiments for should-trigger, should-not-trigger, and near-miss behavior after structural changes to this reusable system.

## Cognitive Document/Visual Authoring Gate

Read `references/cognitive-authoring-process.md` before writing, slide design,
report writing, visualization, or native PPTX implementation when the reader's
situation, problem, or action is in scope.

The reusable process lock is `cognitive-document-visual-authoring-v1`:

1. `R. Research / Evidence Freeze`
2. `P. Person / Problem Model`
3. `M. Message / Mental Model`
4. `W. Writing / Visual Realization`
5. `A. Audit / Artifact Release`

The gate produces an authoring packet with these required fields:

- `process_lock`
- `reader_situation`
- `cognitive_task`
- `desired_action`
- `semantic_fit`
- `evidence_boundary`
- `output_route`
- `verification_surface`
- `folded_unit`
- `weakness_diagnosis`
- `cta_interview_log`
- `unfolding_trace`
- `seed_sentence`
- `title_sequence`
- `knowledge_split`
- `visual_rationale`
- `visual_value_spec`
- `cognitive_load_risks`
- `transfer_artifact`
- `stage_gate_log`

This gate does not replace writing, storyline, visualization, or PPTX checks. It
sets the semantic basis they must inherit. If the packet cannot state why the
reader needs this artifact, what action it supports, what evidence boundary
applies, and how visual values support the meaning, the workflow returns to the
unfolding loop before production continues.

`visual_value_spec` must state the design intent, reader-path support,
readability/accessibility rationale, native medium constraints, chosen values,
and intentionally unconstrained areas. It must not require canvas, grid,
hierarchy, typography, color, spacing, alignment, density, palette, motif,
animation, image, icon, or template choices unless the target project, medium,
accessibility, brand, or native-PPTX constraint actually requires them.

## Outline Notes Gate

Before storyline review, visualization, or native PPTX build, write outline notes
as a production source that makes the deck's intended flow inspectable. Outline
notes must include:

- `reader_situation`
- `deck_or_document_purpose`
- `section_flow`
- `slide_sequence`
- `title_story_draft`
- `visible_message`
- `spoken_or_facilitation_notes`
- `evidence_links`
- `visual_intent`
- `open_questions`

Do not start `pptx-standard-xml-build` or `pptx-build` from slide specs alone.
If outline notes are missing, the workflow returns to writing rather than moving
to visualization or PPTX implementation.

## Storyline And Cognitive Readability Gate

Read `references/slide-authoring-methods.md` when a deck's learner-facing flow,
slide titles, evidence use, or cognitive-load risk is in scope.

Run this gate after the cognitive authoring packet and writing flow have produced
a seed sentence, title sequence, knowledge split, outline notes, and draft slide
specs.

The gate checks six things before visual production:

- `Title-Only Story Test`: slide titles alone show the learner-facing story.
- `Assertion-Evidence Test`: each slide body supports the title's claim or action.
- `One Beat Test`: each slide does one main teaching job.
- `5-Second Scan Test`: the main action or judgment is quickly visible.
- `Cognitive Load Test`: coherence, signaling, contiguity, redundancy, and split-attention risks are reduced.
- `Evidence Boundary Test`: source IDs and uncertainty remain auditable without taking over the learner-facing slide.

This gate creates a proxy judgment, not a human outcome claim. Do not claim
learner comprehension, retention, transfer, or behavior change unless a separate
human test or learner artifact supports it.

## Session Feedback Pattern Gate

Read `references/session-feedback-and-surface-gates.md` when a project has
review comments, diff comments, or repeated feedback about slide story,
expression, visual load, prompt structure, citation handling, or artifact
handoff.

This gate turns repeated comments into reusable checks:

- `title_story_naturalness`: slide titles should read as a natural story, not as
  imported framework labels.
- `decorative_load`: visual effects should earn their place by reducing
  attention cost or clarifying meaning.
- `internal_metadata_relevance`: version labels, process labels, or source
  workflow names should not appear in learner-facing artifacts unless the
  learner needs them.
- `legal_or_regulated_ai_boundary`: when legal, financial, medical, or other
  regulated contexts appear, state where AI can support reading, drafting,
  comparison, or question generation, and where human/expert verification is
  required.
- `citation_link_integrity`: source citations must keep source labels and links
  in the appropriate evidence surface.
- `table_or_slide_body_fit`: dense comparisons, criteria, or evidence should
  become a table when prose would hide the structure.
- `prompt_structure_knowledge_split`: prompt examples should show declarative,
  procedural, and situational knowledge where that helps the reader perform the
  task.

The gate produces a revision queue. It is not a guarantee that the final copy is
beautiful, only that recurring known weaknesses are no longer invisible.

## Semantic Staging Design Framework Gate

Read `references/semantic-staging-design-framework.md` when the artifact needs
stronger visual direction: attention entry, curiosity, guided reading, spoken
flow, evidence reveal, action exit, and explicit design freedom.

This gate runs after storyline/readability and session-feedback checks, before
open visualization planning or PPTX implementation. It produces
`staging-design-brief.json` or an equivalent production-source section with:

- `scene_beat`
- `attention_entry`
- `curiosity_gap`
- `reading_path`
- `listening_cue`
- `evidence_reveal`
- `semantic_variables`
- `accessibility_and_load`
- `design_freedom_boundary`
- `open_expression_options`
- `selected_expression_rationale`
- `avoid_unnecessary_constraints`

Do not force a predefined style kit, template, layout family, palette, fixed
image-generation method, icon style, motif, animation plan, or recurring visual
language. Use those only when the target project supplies a real constraint or
when the staging brief selects them for a stated reason.

## Image-First Semantic Fit And VLPP Expression-Distance Gate

Use this gate after semantic-staging design and before HTML/PPTX implementation
when the visual direction is still being negotiated, when the user asks to see
images before building slides, or when visual candidates need a calculable
comparison.

The gate produces `image-first-visualization-packet.json`,
`visual-candidate-contact-sheet.png`, `vlpp-expression-distance-monitor.json`,
or equivalent production-source sections with:

- `image_first_visualization_surface`
- `visual_candidate_set`
- `candidate_semantic_role`
- `target_expression_vector`
- `expression_vector_dimensions`
- `candidate_expression_vectors`
- `distance_metric`
- `distance_to_target`
- `candidate_strength_formula`
- `selected_candidate`
- `monitoring_rules`
- `evidence_state`
- `claim_boundary`
- `learner_facing_boundary`

Rules:

- Image-first means a visual surface is inspected before committing to HTML,
  PPTX, template, palette, motif, or animation details.
- Every chosen value should be traceable to semantic role, learner situation,
  schedule/session constraint, medium constraint, safe area, text size, density,
  scan path, or action exit.
- VLPP observes computable distance between symbols or expressions. It does not
  infer learner psychology, comprehension, persuasion, motivation, retention, or
  behavior change.
- A VLPP monitor must state `evidence_state: observed_computation` or a stricter
  local equivalent, and must keep human outcome claims out of the result.
- Candidate ranking defaults to the shortest distance to the target-expression
  vector. A separate human, brand, accessibility, or production constraint may
  override the ranking only when the override reason is recorded.
- Keep VLPP details out of learner-facing slides unless the learners are being
  taught the method itself.

## PPTX Standard XML Generation Gate

Read `references/pptx-standard-xml-generation.md` when a workflow creates a
native PPTX. Keep outline notes, generation, and validation separate:

- `outline-note-gate`: confirm the deck or PPTX has inspectable outline notes
  before build work starts.
- `system-run`: when the compatible npm route is available, produce
  `09-system-state.json`, `10-system-runbook.md`, and `11-release-packet.md`
  before the PPTX build.
- `pptx-standard-xml-build`: create a new editable PPTX through helpers or
  builders that respect PresentationML/OPC constraints.
- `pptx-build`: produce `Document_Slide_Authoring_System_new.pptx` or the
  target project's declared new PPTX output.
- `native-powerpoint-check`: inspect native editable objects, package parts,
  relationships, slide order, drawing IDs, table anchors, notes, master/layout,
  and theme flow.
- `presentationml-spec-check`: prove ECMA-376/MS-PPTX source coverage and
  rule-to-check mapping.
- `recovery-compare-check`: compare recovery artifacts or record that no active
  recovery artifact blocks the current build.
- `manual-powerpoint-open-check`: prove final Microsoft PowerPoint no-recovery
  release readiness.

Do not treat the helper-based build, XML/package validation, PDF render, or
QuickLook preview as a substitute for outline notes or the fresh PowerPoint open
check. If a command rebuilds the PPTX after the open check, the previous
PowerPoint open evidence is stale and cannot support release readiness.

## Artifact Surface Separation Gate

Read `references/session-feedback-and-surface-gates.md` before closeout when a
workflow produces more than one kind of artifact. The reusable system separates:

- `learner_facing`: the deck, document, report, or visualization the reader sees.
- `instructor_facilitator`: notes, teaching cues, facilitation guide, or handoff
  commentary.
- `production_source`: Markdown, scripts, templates, JSON, data, and build
  inputs.
- `evidence_fact_table`: source tables, verification tables, citation maps, and
  uncertainty logs.
- `render_native_proof`: screenshots, PDFs, native open checks, and editable
  object audits.
- `delivery_handoff`: final package, client handoff, or distribution folder.

Do not close a task with one blended status such as `slides done` when some
surfaces are complete and others are `blocked` or intentionally out of scope.

## Code / LLM Boundary

Deterministic code owns:

- schema and file presence checks
- required agent, skill, tool, workflow, and release-gate IDs
- local skill module heading checks
- fixed workflow stage order and stage-order dependency checks
- audit JSON creation
- release blocker classification
- presence of working-source clarification fields
- presence of conflict-resolution and fixed/flexible/decisional contracts
- presence of intentional implementation fields: `fixed`, `flexible`,
  `decisional`, `calculated_values`, and `implementation_trace`
- presence of calculated-value fields for semantic role, reader situation,
  medium constraint, safe area, readable size, density, scan path, action exit,
  element tradeoff, element placement, and front/back order
- presence and order of `course-flow-map.md`, `slide-planning-map.json`,
  `symbol-inventory.json`, and `semantic-design-system.json` before visual
  design or PPTX build
- presence of layout element calculation fields for tradeoff, attention cost,
  space cost, semantic gain, placement, front/back order, reading order, native
  object order, and overlap risk
- presence of cognitive authoring packet fields when scaffolded projects adopt the full system
- presence of semantic-fit, unfolding-trace, and visual-value-spec gates before writing or visualization
- presence of outline notes before storyline, visualization, or PPTX build
- presence of storyline/readability gate artifacts when scaffolded projects adopt the full system
- presence of session-feedback pattern checks when scaffolded projects adopt the full system
- presence of semantic-staging design fields before visualization or PPTX build
- presence of image-first visualization surfaces and contact-sheet evidence when visual direction is unsettled or requested before HTML/PPTX
- presence of VLPP expression-vector schema, target vector, distance metric, candidate ranking, `evidence_state`, and claim boundary when VLPP monitoring is used
- presence of artifact-surface separation roles before closeout
- presence of routing experiment fields when the reusable system changes
- presence of PPTX standard XML generation, native package, and PresentationML spec-check tool surfaces
- presence of compatible npm process fields: `system:init`, `system:run`,
  required state outputs, new PPTX output, PresentationML/native/research
  verification commands, recovery comparison, manual open-check path, accepted
  release statuses, and rebuild warning

LLM judgment owns:

- project-specific wording
- audience framing
- quality of the whole-course flow and whether the module/session sequence fits
  the target learners
- quality of the slide planning map by visual situation, cognitive operation,
  learner action, output artifact, timing, evidence, and reuse policy
- quality of symbol selection and semantic design-system rationale
- whether a layout element's attention cost and space cost are worth its
  semantic gain
- reader situation, cognitive task, desired action, and semantic-fit judgment
- cognitive-task-analysis probe quality and unfolding interpretation
- slide-level narrative decisions
- title-only story coherence, assertion-evidence fit, and cognitive-load proxy interpretation
- whether a repeated review comment is a reusable pattern or a one-off taste issue
- whether an artifact surface is necessary for the target audience and handoff
- visual semantics and visual value choices
- semantic-staging choices such as attention entry, curiosity gap, reading path, listening cue, evidence reveal, design-freedom boundary, open expression options, selected-expression rationale, and unnecessary-constraint removal
- image-first candidate interpretation, target-expression dimension rationale, selected-candidate rationale, and whether a non-distance constraint should override a distance ranking
- whether the outline notes are sufficiently concrete for the target audience and session
- whether the compatible npm route is actually available in the target project
  and which work id/title should be used
- whether a missing evidence item is acceptable, `blocked`, or out of scope

Do not let an LLM claim PowerPoint release readiness from zip integrity, XML structure, PNG previews, PDF export, QuickLook, or an old manual-open check after rebuild. Do not let an LLM claim human learning outcomes from storyline/readability proxy checks alone. Do not let an LLM treat VLPP expression-distance monitoring as psychological interpretation.

## Runtime Compatibility Gate

Status: `shared-core only / no-delta`.

Reason: the portable system is encoded as Markdown, JSON, and Node.js scripts. It does not require a separate agent runtime. Codex, Claude, Gemini, and other local skill consumers can use the same scaffold/check contract through the shared `~/.cogarch/skills` expression point.

## Provider / Provenance vs Output Brand

Keep provider provenance and output brand separate:

- `provider_provenance`: which agent, model, skill, source corpus, tool, or
  manual process produced or verified a surface.
- `output_brand`: what the reader should see as the artifact identity, such as
  a course name, report name, client package, or internal handoff.

Provider provenance belongs in evidence, audit, notes, or handoff surfaces. It
should not leak into learner-facing titles or visible deck labels unless the
reader needs that information for the task.

## Runtime Adaptation Default

Default status is `shared-core only / no-delta`. Runtime-specific adapters may
change invocation paths, local command names, or UI handoff details, but they
must not change fixed workflow gates, release boundaries, source roles, or
artifact surface roles without a version bump and routing experiment.

## Legacy Package Distillation Gate

This skill is a distilled reusable package from a project-local authoring system. Treat the source project as provenance and example evidence, not as a runtime dependency.

When adapting an older project-local system:

- distill the agent/skill/workflow shape
- distill working-source clarification, conflict resolution, and 3-layer classification instead of importing one project's assumptions
- distill cognitive document/visual authoring into packet fields, checks, and references instead of keeping a project-local runtime dependency
- distill recurring session feedback into reusable pattern checks instead of keeping one deck's comments
- distill artifact-surface separation into roles and gates instead of merging learner copy, source files, evidence tables, and proof artifacts
- distill compatible npm authoring as command order, expected state outputs,
  build output, native/research/repetition checks, manual-open evidence, release
  statuses, and rebuild invalidation rule instead of copying one deck's content
- keep project content, PPTX filenames, recovered artifacts, and deck-specific audits in the target project
- do not merge unrelated deck outputs into the global skill
- keep the PowerPoint manual open check as a release gate, not as a structural check

## Dependencies And Permissions

Required:

- Node.js
- read/write access to the target project for scaffold mode
- read/write access to write `authoring-agent-system-audit.json` for check mode

Not required:

- network
- external credentials
- Microsoft PowerPoint automation APIs
- image model credentials

Permission boundary:

- `scaffold` writes only the generated authoring-agent files under the target root
- `check` reads the target system files and writes one audit JSON
- neither mode deletes project files

## References

The reusable cognitive authoring process is defined in
`references/cognitive-authoring-process.md`. The reusable slide-authoring method
is defined in `references/slide-authoring-methods.md`. See
`references/source-notes.md` for source and license boundaries.

- `references/glossary.md`
- `references/concept-map.md`
- `references/cognitive-authoring-process.md`
- `references/course-flow-to-design-system-sequence.md`
- `references/pptx-standard-xml-generation.md`
- `references/semantic-staging-design-framework.md`
- `references/session-feedback-and-surface-gates.md`
- `references/slide-authoring-methods.md`
- `references/source-notes.md`

## Rubric

Must:

- A target project can run scaffold without overwriting existing files by default.
- A target project can run check and receive `authoring-agent-system-audit.json`.
- The audit distinguishes structural readiness from PowerPoint release readiness.
- The architecture includes working-source clarification before cognitive authoring.
- The architecture includes conflict resolution and fixed/flexible/decisional classification with a drift rule.
- The checker enforces the fixed workflow order and fails when required stages are missing or reordered.
- The checker enforces `course-flow-map.md -> slide-planning-map.json -> symbol-inventory.json -> semantic-design-system.json` before semantic staging, image-first visualization, and PPTX build.
- The architecture prevents a design system, template, palette, motif, or style kit from being fixed before the whole lecture flow, slide planning, and symbol inventory exist.
- The checker enforces intentional implementation fields: `fixed`, `flexible`, `decisional`, `calculated_values`, and `implementation_trace`.
- The checker enforces calculated value fields for semantic role, reader situation, medium constraint, safe area, readable size, density, scan path, action exit, element tradeoff, element placement, and front/back order.
- The checker enforces layout element calculation fields for element ID, semantic role, element tradeoff, attention cost, space cost, semantic gain, placement, front/back order, reading order, native object order, and overlap risk.
- The architecture includes a cognitive authoring packet gate before writing, storyline/readability, visualization, and PPTX implementation.
- The cognitive authoring packet requires reader situation, cognitive task, desired action, semantic fit, evidence boundary, output route, verification surface, unfolding trace, title sequence, knowledge split, visual rationale, visual value spec, and stage-gate log.
- The architecture includes writing and visualization as separate processes.
- The architecture includes an outline-notes gate before storyline, visualization, and PPTX build.
- The architecture includes a storyline/readability gate between writing and visualization.
- The storyline/readability gate covers title-only story, assertion-evidence, one-beat, 5-second scan, cognitive-load, evidence-boundary, and human-outcome claim boundaries.
- The architecture includes a session-feedback pattern gate between storyline/readability and visualization.
- The session-feedback pattern gate covers title story naturalness, decorative load, internal metadata relevance, legal/regulated-domain AI boundary, citation link integrity, table/body fit, and prompt knowledge structure.
- The architecture includes a semantic-staging design framework gate before visualization and PPTX build when attention, curiosity, reading path, listening cue, evidence reveal, and action exit must be planned without freezing a predefined style.
- The semantic-staging design framework requires scene beat, attention entry, curiosity gap, reading path, listening cue, evidence reveal, semantic variables, accessibility/load, design-freedom boundary, open expression options, selected-expression rationale, and avoid-unnecessary-constraints fields.
- The architecture includes an image-first semantic-fit gate before HTML/PPTX implementation when visual direction is unsettled or explicitly requested.
- The image-first gate can produce visual candidates, a contact sheet, calculated value manifest, and selected-candidate rationale before build work.
- The architecture includes VLPP expression-distance monitoring when symbolic expression candidates need calculable comparison.
- The VLPP gate distinguishes computed symbol/expression distance from psychological interpretation and human learning outcomes.
- The visualization flow requires open planning, semantic variable capture, selected visual decisions, intentionally unconstrained areas, and real medium/accessibility constraints.
- The PPTX build flow requires outline notes before standard XML-aware generation and separates generation from native package validation, PresentationML spec coverage, and manual PowerPoint open evidence.
- The PPTX flow preserves PresentationML, OPC, DrawingML, native feature, and manual PowerPoint open-check boundaries.
- The compatible npm route declares `system:init`, `system:run`, `build`,
  PresentationML/native/research verification, recovery comparison,
  repetition gate, manual PowerPoint open check, release check, and
  agent-system check in order.
- The compatible npm route declares `09-system-state.json`,
  `10-system-runbook.md`, `11-release-packet.md`,
  `Document_Slide_Authoring_System_new.pptx`, and
  `manual-open-checks/latest-powerpoint-open-check.json` with
  `result=no_recovery_dialog` as the release evidence surface.
- The compatible npm route accepts only `release_status=pass` or
  `release_status=pass_superseded_old_recovery_artifacts`, and warns that a
  post-check rebuild invalidates the manual open evidence.
- The architecture includes artifact-surface separation before closeout and keeps learner-facing, instructor/facilitator, production source, evidence/fact table, render/native proof, and delivery/handoff surfaces distinct.
- The architecture includes routing experiments with should-trigger, should-not-trigger, expected behavior, and near-miss rationale.
- Runtime compatibility is declared as exactly one status: `shared-core only / no-delta`.

Should:

- The target project should connect the local checker to its package scripts when appropriate.
- Project-specific manuals, prompts, and deck builders should remain local to the project.
- Repeated PowerPoint recovery issues should produce pattern entries and release blockers instead of silent retries.
- Repeated review comments should become reusable pattern checks when they affect story, meaning, evidence, legality, or handoff quality.
- Internal metadata such as version labels or source workflow names should stay out of learner-facing artifacts unless it helps the reader.
- Visual option reports should show why one candidate is stronger by semantic fit, calculable expression distance, accessibility/load, medium fit, and layout element tradeoff instead of style preference alone.

## Preflight

Before closing a task that uses this skill:

1. Run the global selfcheck.
2. Run the checker against the target project.
3. Confirm working-source, conflict-resolution, and 3-layer checks are present in the scaffold/check output.
4. Confirm fixed workflow order and stage-order dependency checks pass.
5. Confirm course-flow, slide-planning, symbol-inventory, and semantic-design-system sequence checks pass.
6. Confirm intentional implementation, calculated-value, and layout-element calculation checks pass.
7. Confirm cognitive authoring packet field checks are present in the scaffold/check output.
8. Confirm outline-notes checks are present before storyline, visualization, and PPTX build.
9. Confirm semantic-design-system and semantic-staging design checks are present before visualization and PPTX build.
10. Confirm image-first visualization and contact-sheet evidence exist when visual direction was requested before HTML/PPTX.
11. Confirm VLPP expression-distance monitoring, `observed_computation` evidence state, and non-psychological claim boundary exist when VLPP is used.
12. Confirm session-feedback pattern and artifact-surface separation checks are present in the scaffold/check output.
13. Confirm compatible npm process checks are present when the route is declared: state outputs, PPTX output, manual open-check path, accepted release statuses, command tools, and rebuild warning.
14. Confirm routing experiment checks exist after structural changes.
15. Report structural status, proxy/readability status, course-flow/design-system sequence status, image-first/VLPP status, artifact-surface status, compatible npm route status, and release-readiness status separately.
