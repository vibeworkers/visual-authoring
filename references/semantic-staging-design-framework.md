# Semantic Staging And Design Freedom Framework

Use this reference when a deck, report, visualization, or PPTX needs stronger
visual staging: attention entry, curiosity, guided reading, spoken flow,
evidence reveal, action exit, and explicit design freedom.

## Boundary

This framework owns semantic staging, not visual style. It decides what cognitive
job a visual form must perform and which constraints are real. It does not make
any predefined style kit, template, layout family, palette, fixed
image-generation method, icon style, motif, animation plan, or recurring visual
language mandatory.

Expression stays open unless the target project supplies a real constraint:
brand, accessibility, device or room condition, native PPTX behavior, data
structure, licensing, production capacity, or a deliberate staging choice.

## Artifact-Level Lock And Open-Set Materiality

Once an artifact starts production, lock the design-system grammar: token/style
namespace, typography hierarchy, spacing/density, component grammar, status
semantics, and accessibility/contrast. The values remain project-specific, but
the active artifact does not drift silently. Changing the lock creates a new
lock id and makes affected style/render evidence stale.

The lock is not a page template. Scene structure, viewpoint, spatial relation,
reading path, silhouette, and visual material remain open to the semantic job.
All visual expressions an LLM can currently or later render are candidates, not
a finite whitelist. Close candidates only for real source, brand, license,
safety, accessibility, medium, or production constraints. This open candidate
space does not force image generation; deterministic SVG/native structure may
be the strongest materiality for an abstract relationship.

## Evidence Basis

This framework reuses the local evidence bundle in
`references/slide-authoring-methods.md`:

- assertion-evidence slide research: titles as claims and slide bodies as
  evidence, procedure, comparison, example, or action
- multimedia learning and cognitive-load research: coherence, signaling,
  contiguity, redundancy, and split-attention control
- text-structure and organizer research: headings and sequence as meaning cues
- practitioner presentation structure: conclusion-first and support hierarchy,
  treated as practice guidance rather than peer-reviewed proof

## Core Principle

Design is not decoration and design freedom is not arbitrariness. A visual
choice earns its place only when it changes the reader's cognitive path:

1. What do they notice first?
2. What question or tension makes the next part worth reading?
3. What should they read on the slide, and what should they hear from the
   speaker?
4. What evidence, example, comparison, or procedure makes the message credible?
5. What action or judgment should remain after the slide changes?
6. Which style choices are genuinely constrained, and which should remain open?

## Staging Packet

Before open visualization planning or PPTX build, create
`staging-design-brief.json` or an equivalent section in the production source:

```yaml
staging_design_brief:
  design_system_lock_ref: ""
  scene_beat: ""
  scene_mode: "concrete_world | operational_state | abstract_relationship"
  attention_entry: ""
  curiosity_gap: ""
  reading_path: []
  listening_cue: ""
  evidence_reveal: []
  semantic_variables: []
  accessibility_and_load: ""
  design_freedom_boundary: ""
  open_expression_options: []
  open_materiality_candidate_space: "open_set"
  selected_materiality_rationale: ""
  selected_expression_rationale: ""
  avoid_unnecessary_constraints: []
```

## Staging Moves

| Move | Question | Freedom-preserving output |
| --- | --- | --- |
| `scene_beat` | What one scene or learner-facing job does this slide perform? | A one-job statement before any style choice. |
| `attention_entry` | What should the reader see within the first few seconds? | A focal intent, not a forced focal technique. |
| `curiosity_gap` | What useful question makes the next part worth reading or hearing? | The tension or missing piece that justifies attention. |
| `reading_path` | What order should the eye follow? | The required sequence; layout remains open unless constrained. |
| `listening_cue` | What does the speaker add that should not be duplicated as slide text? | Visible/spoken split. |
| `evidence_reveal` | What proof, example, procedure, or source boundary supports the claim? | Evidence timing and level of detail. |
| `semantic_variables` | Which visual choices carry meaning? | Named variables such as contrast, position, grouping, object type, label, scale, or reveal timing when actually used. |
| `accessibility_and_load` | What reduces cognitive and perceptual burden? | Readability, contrast, density, alt text, and reading order constraints that are actually needed. |
| `design_freedom_boundary` | Which design decisions are fixed, flexible, or intentionally open? | A constraint map that prevents false defaults. |
| `open_expression_options` | What different visual expressions could serve the same meaning? | Multiple viable options before selection. |
| `selected_expression_rationale` | Why choose this expression now? | A reason tied to reader task, evidence, medium, or production limits. |
| `avoid_unnecessary_constraints` | What must not be frozen too early? | Explicit removal of premature style, method, or production assumptions. |

## Image-First And VLPP Expression-Distance Extension

Use image-first visual staging when the team needs to see the design direction
before committing to HTML, PPTX, template, palette, motif, or animation details.
The image is a decision surface, not a final delivery claim.

Minimum packet:

```yaml
image_first_visualization_packet:
  image_first_visualization_surface: ""
  visual_candidate_set: []
  candidate_semantic_role: []
  target_expression_vector: {}
  expression_vector_dimensions: []
  candidate_expression_vectors: []
  distance_metric: "cosine_distance"
  distance_to_target: []
  candidate_strength_formula: ""
  selected_candidate: ""
  monitoring_rules: []
  evidence_state: "observed_computation"
  claim_boundary: "symbol/expression distance only"
  learner_facing_boundary: ""
```

Rules:

- Calculate visual values from semantic role, reader situation, schedule or
  session constraint, medium constraint, safe area, readable size, density, scan
  path, and action exit.
- Use VLPP only as computed distance observation between target symbolic
  expression and candidate rendered expression.
- Do not use VLPP to infer comprehension, motivation, persuasion, retention, or
  behavior change.
- Prefer the shortest distance to the target-expression vector unless a recorded
  accessibility, brand, human-review, or production constraint overrides it.

## Gate Tests

| Test | Pass condition | Failure signal |
| --- | --- | --- |
| `scene_one_job` | The slide has one main staging job. | A definition, warning, example, source table, and task instruction compete. |
| `attention_to_question` | The focal point leads to a real question, tension, or next reading action. | A decorative element attracts attention but does not explain why it matters. |
| `read_speak_split` | Slide text and spoken explanation complement each other. | The slide repeats the full script, or the speaker must explain what the slide should already show. |
| `evidence_reveal_fit` | Evidence appears at the moment and level needed for the reader's judgment. | Source proof is hidden when needed, or URLs dominate the learner-facing surface. |
| `design_freedom_preserved` | Predefined style kits, templates, motifs, palettes, icons, images, and animation plans remain optional unless justified. | A default style or production method decides the slide before the cognitive job is clear. |
| `constraint_truthfulness` | Constraints are named only when they come from audience, medium, data, accessibility, brand, license, production, or native PPTX requirements. | A preference is recorded as a requirement. |
| `load_and_accessibility` | Signaling, proximity, readable size, contrast, and density are intentional when used. | Visual polish increases split attention, crowding, or reading effort. |
| `image_first_surface` | A visual candidate or contact sheet exists before build when requested or when direction is unsettled. | PPTX/HTML is built before the team can inspect visual direction. |
| `vlpp_claim_boundary` | VLPP monitor states distance metric, evidence state, and non-psychological claim boundary. | A computed distance is reported as learner psychology or outcome proof. |

## Output Boundary

`staging-design-brief.json` supports a semantic-staging and design-freedom
readiness claim. Image-first packets and VLPP monitors support visual-direction
and expression-distance readiness claims. They do not prove that the audience
understood, remembered, or acted. Human outcome validation still requires
learner response, comprehension answers, transfer tasks, or equivalent evidence.
