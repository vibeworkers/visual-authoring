# Slide Authoring Methods

Use this reference when a deck needs evidence-backed judgment about slide titles,
story flow, assertion-evidence fit, cognitive load, and learner-facing visual
clarity before native PPTX implementation.

This reference runs after `references/cognitive-authoring-process.md`. The
cognitive authoring packet supplies the reader situation, cognitive task,
desired action, semantic fit, seed sentence, title sequence, knowledge split, and
visual value spec that this slide-specific gate reviews.

## Evidence Layers

| Layer | Sources | Use |
| --- | --- | --- |
| Direct slide evidence | Garner & Alley, `How the Design of Presentation Slides Affects Audience Comprehension` ([PDF](https://www.ijee.ie/articles/Vol29-6/23_ijee2791ns.pdf)); Alley et al., `How the Design of Headlines in Presentation Slides Affects Audience Retention` ([PDF](https://www.writing.engr.psu.edu/ae_headlines.pdf)); Assertion-Evidence tutorial ([site](https://www.assertion-evidence.org/tutorial.html)) | Treat slide titles as message claims and slide bodies as evidence, comparison, procedure, example, or action. |
| Learning and cognitive-load evidence | Mayer, `Multimedia Learning` ([PDF](https://www.jsu.edu/online/faculty/MULTIMEDIA%20LEARNING%20by%20Richard%20E.%20Mayer.pdf)); Castro-Alonso et al., `Five Strategies for Optimizing Instructional Materials` ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7940870/)) | Reduce redundant text, split attention, decorative load, and unclear signaling. |
| Structure and organizer evidence | Bryce & Blown, `Ausubel's meaningful learning re-visited` ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10130311/)); Bogaerds-Hazenberg et al., `A Meta-Analysis on the Effects of Text Structure Instruction` ([Wiley](https://ila.onlinelibrary.wiley.com/doi/full/10.1002/rrq.311)) | Use agenda, headings, and title sequence as structure cues, not only labels. |
| Practitioner structure | think-cell, `Pyramid Principle for PowerPoint presentations` ([site](https://www.think-cell.com/en/resources/content-hub/using-the-pyramid-principle-to-build-better-powerpoint-presentations)) | Use conclusion-first titles and subordinate slides that support the conclusion. Treat this as practical guidance, not peer-reviewed proof. |

## Gate Tests

| Test | Pass condition | Failure signal |
| --- | --- | --- |
| Authoring Packet Fit Test | Reader situation, cognitive task, desired action, semantic fit, evidence boundary, unfolding trace, and visual value spec are present before slide writing is judged. | Titles or layouts are being judged without knowing what reader problem they serve. |
| Title-Only Story Test | The slide titles alone show the problem, development, practice reason, judgment standard, response, and close, and they inherit the packet's seed sentence and desired action. | Titles are mostly noun labels, and slide order can change without changing meaning. |
| Assertion-Evidence Test | Each title states one claim or action, and the body directly supports it with visual evidence, comparison, procedure, example, or action. | Title and body are parallel summaries that do not depend on each other. |
| One Beat Test | One slide does one learner-facing job. | Definition, example, warning, source inventory, and practice instructions compete on one slide. |
| 5-Second Scan Test | A learner can identify the slide's main action or judgment within about five seconds. | Version labels, decorative rails, dense citations, or secondary metadata are visually louder than the point. |
| Cognitive Load Test | Coherence, signaling, contiguity, and redundancy risks are reduced. | The same sentence appears in title, body, and spoken script, or related text and visual evidence are far apart. |
| Evidence Boundary Test | Source IDs, evidence states, and uncertainty are visible enough to audit but do not dominate learner-facing slides. | Long URLs or verification tables overwhelm the learning surface. |

## Claim Boundary

- `technical_editability_proxy`: native object, notes, table, chart, hyperlink, and package checks.
- `semantic_structure_proxy`: title-only story, assertion-evidence map, one-beat review, source/evidence boundary.
- `cognitive_readability_proxy`: 5-second scan, grouping, proximity, signaling, redundancy, and split-attention review.
- `human_outcome_validation`: learner comprehension, retention, transfer, or behavior evidence.

Do not report learner comprehension, retention, transfer, or performance as
passed from proxy checks alone. Without human evidence, close as `candidate`,
`conditional`, `hypothesis only`, or `not_run`.

## Application Rules

1. Put the storyline/readability gate after writing and before visualization.
2. Require the cognitive authoring packet before judging slide titles or visual layout.
3. Rewrite topic labels into short sentence claims when the slide is meant to teach a judgment.
4. Keep speaker explanation, source tables, and verification inventories outside learner-facing slide bodies unless they are the learner's task.
5. Make prompt-practice slides show request, rationale, and checking criteria in adjacent structure.
6. Convert visual choices into semantic variables and visual value specs only after the slide's story beat is stable.
7. Treat text readability as part of the slide's visual value spec when the learner-facing surface requires sustained reading.
8. Keep practitioner methods such as action titles and pyramid structure separate from peer-reviewed evidence claims.
