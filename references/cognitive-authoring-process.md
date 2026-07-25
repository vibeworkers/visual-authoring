# Cognitive Document/Visual Authoring Process

This reference defines the reusable process for turning evidence and context into
documents, slides, reports, visualizations, and native presentation artifacts.

## Source Distillation Boundary

This process was distilled from the project-local
`cognitive-document-visual-authoring` skill used in the `[새싹4기] 생성형 AI 및
IT 도구 활용` workspace.

The global package keeps only the reusable authoring process:

- reader cognitive work starts before output format
- semantic fit comes before wording and visual form
- weak or folded content is repaired through cognitive-task-analysis style questions
- unfolded meaning becomes sentence order, title order, and visual hierarchy
- outline notes make the intended deck or PPTX flow inspectable before build work starts
- visual values are intentional semantic choices when selected, and may remain
  intentionally unconstrained when no real constraint exists
- semantic staging and design-freedom boundaries come before visualization or
  PPTX build
- image-first visual candidates can be inspected before HTML/PPTX build when
  visual direction, density, or expression fit is still unsettled
- VLPP-style monitoring, when used, observes computable distance between
  symbolic expressions and never claims learner psychology or human outcomes

Project-specific lecture content, deck names, survey results, local examples, and
audit files remain in the target project. This global skill does not depend on
the project-local runtime path.

## Process Lock

Use process lock `cognitive-document-visual-authoring-v1`.

| Stage | Name | Required Decision |
| --- | --- | --- |
| R | Research / Evidence Freeze | What is known, inferred, uncertain, or blocked? |
| P | Person / Problem Model | Who is reading or listening, and what situation are they trying to handle? |
| M | Message / Mental Model | What schema, distinction, sequence, or judgment must become easier? |
| W | Writing / Visual Realization | What sentences and visual values make that mental work visible? |
| A | Audit / Artifact Release | What can be claimed from proxy checks, and what still needs human evidence? |

## Universal Authoring Strategy Loop

The reusable method is stable even when the design system, tool, or output
format changes. Run the work in this order:

1. Lock the reader situation, desired state change, and success evidence.
2. Decompose the source and expose the content architecture, sequence, and
   decision points.
3. Record the Fixed / Flexible / Decisional strategy ledger.
4. Route each semantic unit to an expression family before choosing a style
   system or drawing objects.
5. Plan the medium capability, edit boundary, and native/image/vector/chart
   ownership.
6. Build one representative from each selected expression family and assemble
   a small prototype artifact.
7. Pass content-fit review and the format-specific release checks on that
   prototype, record them in the prototype authorization manifest, and pass
   `validate_authoring_prototype_gate.py --require-authorized` before scaling
   to the full artifact.
8. Produce the full artifact, then verify each proof surface separately.
9. Close with a retrospective that keeps local incidents local unless the same
   failure pattern recurs with evidence.

An expression family is project-derived. Examples include opener, concept
relationship, process, comparison, table/chart, exercise, and transfer summary.
The list is not a mandatory template. The gate is that every materially
different semantic/technical construction is represented before mass
production. For native PPTX, the prototype artifact must receive a fresh
Microsoft PowerPoint open check with `no_recovery_dialog`; zip/XML, render, and
geometry checks do not substitute for it.
A prose checklist or retrospective is not authorization. The project manifest
and validator provide the executable stop condition; the reviewer still owns
the bounded content-fit judgment recorded in that manifest.

"Better" means better fit to the current content, reader task, action,
instructional sequence, intentional editability, and target-medium stability.
It does not mean closer visual similarity to a reference benchmark or a higher
object/spacing score.

### Strategy Ledger

| Layer | Stable role | Project evidence |
| --- | --- | --- |
| Fixed | source role, reader/action contract, content-fit hierarchy, claim boundary, proof-surface separation, required native-open gate | skill/reference rule and validator output |
| Flexible | content structure, expression families, design-system candidates, layout, color, density, native/image mix, project thresholds | project SoT, authoring packet, prototype artifact |
| Decisional | preserve/transform choices, expression route, prototype sufficiency, native payoff, `pass_local`/`revise`/`blocked` judgment | Fixed rule applied + Flexible evidence path + next action |

Code may calculate bounds, overlap, alignment, spacing, connector relations,
coverage, and package structure. Those calculations strengthen the geometry or
technical proof surface only. They do not prove visual improvement, content
fit, edit experience, comprehension, or learning outcome.

## Authoring Loop vs Incident-Response Loop

Keep the two loops connected but distinct.

### Authoring loop

`intent -> content architecture -> strategy ledger -> expression route ->
medium/native plan -> expression-family prototype -> full production ->
surface-separated verification -> retrospective`

### Incident-response loop

`exact failure signal -> affected proof surface -> smallest diagnostic ->
source-level repair -> rebuild -> rerun every invalidated proof surface`

Binary isolation, XML inspection, object-distance calculation, render diff, and
single-slide reproduction are legitimate incident diagnostics. They do not
replace the authoring loop and must not become global design rules solely
because they helped isolate one failure. Repair the production source and
regenerate; never promote a PowerPoint-repaired artifact to the release file.

### Retrospective promotion gate

- First occurrence: record a local hypothesis and the smallest remediation.
- Repeated occurrence in a second comparable context: strengthen the owner
  skill's gate and test it in both contexts.
- Recurrence after the strengthened written gate: add an executable stop
  condition at the production boundary and record the event as N=3.
- Portfolio-wide rule: require cross-domain recurrence and validation evidence
  before promotion; keep project values and one-off diagnostics out of the
  global default.

Every retrospective names the failed Must, exact signal, cause class, smallest
remediation, targeted revalidation, and the proof surfaces that became stale.

## Required Authoring Packet

Every full workflow should produce an authoring packet before writing or visual
production continues.

```yaml
process_lock: cognitive-document-visual-authoring-v1
reader_situation: ""
cognitive_task: ""
desired_action: ""
semantic_fit:
  context: ""
  topic: ""
  purpose: ""
  reader_need: ""
  fit_judgment: pass|fail|blocked
evidence_boundary:
  observed: []
  inferred: []
  uncertain: []
  blocked: []
output_route: document|slide|pptx|report|visualization|mixed
verification_surface: ""
folded_unit: ""
weakness_diagnosis: ""
cta_interview_log:
  - question: ""
    answer_or_inference: ""
    exposed_internal_content: ""
unfolding_trace:
  - from: ""
    to: ""
    reason: ""
seed_sentence: ""
title_sequence: []
knowledge_split:
  declarative: []
  procedural: []
  situational: []
visual_rationale: ""
visual_value_spec:
  design_intent: ""
  reader_path_support: ""
  readability_accessibility:
    readability_target: ""
    audience_distance_or_device: ""
    fit_rationale: ""
    intentionally_unconstrained: []
  native_medium_constraints: []
  chosen_values: {}
  intentionally_unconstrained: []
cognitive_load_risks: []
transfer_artifact: ""
stage_gate_log:
  - stage: R|P|M|W|A
    status: pass|fail|blocked
    evidence: ""
```

## Outline Notes Contract

Outline notes are the required bridge between the authoring packet and any PPTX
implementation. They are not speaker notes alone. They are a production source
that shows why the document or deck is ordered this way and what each slide is
supposed to do.

Minimum fields:

```yaml
outline_notes:
  reader_situation: ""
  deck_or_document_purpose: ""
  section_flow: []
  slide_sequence: []
  title_story_draft: []
  visible_message: []
  spoken_or_facilitation_notes: []
  evidence_links: []
  visual_intent: []
  open_questions: []
```

If these notes are missing, the process returns to writing before storyline
review, visualization, or PPTX build continues.

## Unfolding Repair Loop

Use unfolding when a sentence, slide, chart, section, or whole artifact feels
vague, decorative, over-compressed, or mismatched to the reader's situation.

1. Name the folded unit exactly.
2. Diagnose the weak point: missing situation, missing distinction, missing
   evidence boundary, missing action, missing sequence, or overloaded visual
   surface.
3. Ask narrow cognitive-task-analysis style questions that reveal what the
   author, speaker, or reader was already implying.
4. Write the unfolding trace from hidden content to visible sentence, title,
   diagram, table, or interaction.
5. Replace the weak unit only after the trace explains why the new form supports
   the reader's cognitive task.

The repair adds questions, not decoration. Its purpose is to reveal what was
already inside the weak unit and make it usable.

## Visual Value Contract

Visual design choices are semantic choices when they are selected. A project may
use its own visual conventions, but the authoring packet must explain why each
chosen value exists and which values intentionally remain open.

| Value | Required Rationale |
| --- | --- |
| Design intent | What cognitive job the visual form must support |
| Reader path support | What the reader should notice, read, compare, or decide |
| Readability/accessibility | What readability, contrast, density, alt text, or reading-order constraints are genuinely needed |
| Native medium constraints | What PPTX, screen, room, print, device, or collaboration behavior actually constrains the design |
| Chosen values | Why selected layout, hierarchy, type, color, spacing, image, icon, animation, or chart decisions were chosen |
| Intentionally unconstrained | Which style decisions are not fixed because no reader, evidence, medium, accessibility, or production reason requires them |

Do not turn a predefined style kit, template, layout family, palette, fixed
image-generation method, icon style, motif, animation plan, or typography scale
into a default requirement. Use those only when the authoring packet or staging
brief names the reason.

## Route Mapping

| Route | Next Gate |
| --- | --- |
| Document | Writing flow and document preflight |
| Slide | Writing flow, outline notes, title-only story, assertion-evidence, one-beat, semantic-staging design, design-freedom boundary, and visual value checks |
| PPTX | Outline notes, slide gates, semantic-staging design, design-freedom boundary, native PPTX, and PowerPoint open-check release gates |
| Report | Writing flow, evidence boundary, table/chart rationale, and reader action audit |
| Visualization | Evidence boundary, visual value spec, semantic-staging design, design-freedom boundary, chart/table/diagram semantics, and accessibility audit |

When visualization direction is unsettled or explicitly requested before
HTML/PPTX work, add an image-first packet or contact sheet before implementation.
When VLPP monitoring is used, record the target expression vector, candidate
expression vectors, distance metric, distance-to-target, evidence state, and
non-psychological claim boundary.

## Claim Boundary

This process can support these claims:

- the artifact has a declared reader situation and cognitive task
- semantic fit was checked before wording or design
- weak units were repaired through an unfolding trace
- visual values were chosen intentionally
- visual candidates were compared as symbolic expressions when an image-first
  or VLPP monitor is present
- proxy readability and structure checks have passed

It cannot claim human comprehension, retention, transfer, persuasion, behavior
change, or learner psychology from image previews, proxy checks, or VLPP
expression-distance calculations without separate human outcome evidence.
