# Session Feedback And Surface Gates

This reference distills repeated document and slide review feedback into reusable
agent-system gates. It does not copy one project's deck content. It keeps the
review pattern, the artifact-surface boundary, and the routing experiment shape.

## Feedback Pattern Gate

Use this gate after storyline/readability review and before more visual
production. A repeated comment should become a reusable check when it affects the
reader's story, meaning, evidence, legal boundary, prompt action, or handoff.

| Check | Question | Failure Signal | Expected Repair |
| --- | --- | --- | --- |
| `title_story_naturalness` | Do the visible titles create a natural story? | Titles look like imported framework labels or isolated topics. | Rewrite the title sequence so each title advances the reader's situation, question, judgment, or action. |
| `decorative_load` | Does each visual element reduce attention cost or clarify meaning? | Rails, ornaments, icons, or effects compete with the message. | Remove or simplify elements that do not guide scan path, grouping, contrast, or meaning. |
| `internal_metadata_relevance` | Does the reader need this process/version/source label? | Internal labels appear because the production team needed them. | Move production metadata to notes, source files, or handoff surfaces. |
| `legal_or_regulated_ai_boundary` | Is AI use framed by task risk and verification need? | The slide implies AI can decide regulated matters alone. | Separate AI-supported reading, drafting, comparison, and question generation from expert or official verification. |
| `citation_link_integrity` | Are cited sources traceable with labels and links? | Source labels exist without URLs, or citations appear only in hidden files. | Keep citations in the correct learner, note, evidence, or handoff surface with stable links. |
| `table_or_slide_body_fit` | Would a table reveal structure better than prose? | Dense criteria or comparisons are buried in paragraphs. | Use a table when rows/columns make the decision, comparison, or evidence easier to inspect. |
| `prompt_structure_knowledge_split` | Does the prompt show what the reader must know and do? | Prompt examples mix task facts, procedures, and situational constraints without structure. | Split declarative, procedural, and situational knowledge when it improves action. |

## Artifact Surface Separation Gate

Use this gate before closeout. The goal is not to create every surface every
time. The goal is to prevent one completion label from hiding unfinished or
misplaced surfaces.

| Surface | Reader-Facing Role | Typical Evidence |
| --- | --- | --- |
| `learner_facing` | What the end reader sees and uses. | PPTX, PDF, report, dashboard, webpage, or handout. |
| `instructor_facilitator` | What the speaker, facilitator, or reviewer needs to run the session. | Speaker notes, facilitator guide, talking points, timing notes. |
| `production_source` | The editable inputs that regenerate the artifact. | Markdown, outline notes, scripts, templates, JSON, CSV, image sources. |
| `evidence_fact_table` | The source trail and verification boundary. | Citation table, fact-check table, uncertainty log, source map. |
| `render_native_proof` | Proof that the artifact renders and remains native-editable where required. | Screenshot, PDF, native feature audit, PowerPoint open result. |
| `delivery_handoff` | The final package or route for a client, collaborator, or course team. | ZIP, folder index, delivery note, upload path, handoff checklist. |

## Routing Experiments

Use routing experiments after changing this reusable skill or its generated
agent system.

| Case Type | Example | Expected Behavior |
| --- | --- | --- |
| `should_trigger` | "Create a reusable agent system for course slide writing, evidence tables, PPTX build, and handoff." | Use this skill and scaffold/check the portable system. |
| `should_trigger` | "Before creating the PPTX, write overview notes that show the story, spoken flow, evidence, and visual intent." | Use the outline-notes gate before storyline, visualization, or PPTX build. |
| `should_trigger` | "The deck keeps defaulting to a template or motif before the slide's attention path and reader question are clear." | Use the semantic-staging design and design-freedom boundary gate before open visualization planning or PPTX build. |
| `should_trigger` | "Separate the student deck, instructor guide, source files, evidence table, and native proof." | Use the artifact surface separation gate. |
| `should_trigger` | "Repeated slide review comments show title story and decorative-load issues; make them part of the workflow." | Use the session feedback pattern gate. |
| `should_trigger` | "Include the npm system run, PPTX build, PresentationML/native checks, recovery comparison, manual PowerPoint open check, and release check in the slide authoring process." | Use the compatible npm authoring process gate and keep rebuild invalidation explicit. |
| `should_not_trigger` | "Rewrite this one slide title naturally." | Use a copy-editing skill or answer directly. |
| `should_not_trigger` | "Suggest a Canva color palette." | Use a design or Canva-specific flow, not this native PPTX agent system. |
| `near_miss` | "Make a simple PPTX from five bullet points." | Ask whether a reusable workflow or native release gate is required; otherwise keep it simple. |

## Closeout Language

Report these states separately:

- structural readiness
- cognitive/storyline proxy readiness
- session-feedback pattern coverage
- semantic-staging design coverage
- artifact-surface readiness
- compatible npm route status
- native/render proof status
- manual PowerPoint release status

Do not say `done` for all surfaces when only one of these states passed.
