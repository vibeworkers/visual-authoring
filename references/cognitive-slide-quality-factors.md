# Cognitive Slide Quality Factors

## Purpose

Use this reference when a user asks to compare an existing deck's quality,
derive quality factors, or turn repeated slide-review observations into a
reusable evaluator. The owner is `visual-authoring`; this reference consumes
`vector-language-cognition` evidence states rather than redefining its core
metrics or human-validation boundary.

Run `scripts/analyze_slide_quality_factors.py` against the target PPTX and,
when useful, local reference decks. Inputs are read-only. Put every generated
CSV, JSON, SVG, and review code in the `visual-authoring/evals/` surface or an
explicitly owned evaluation directory, never beside the source PPTX unless the
user asks otherwise.

## Claim Boundary

The evaluator has three deliberately separate layers.

| Layer | Owner and evidence | May say | Must not say |
| --- | --- | --- | --- |
| Package observation | deterministic PPTX parser, exact SHA-256 | text/object/font/geometry distributions and their co-variation | rendered appearance, aesthetic quality, comprehension, native-open success |
| Cognitive declaration | project manifest/outline | intended task, relationship, grammar, visible cue, reading path | that a learner actually made the intended inference |
| Review code | named human or LLM reviewer | a contextual hypothesis about focus, load, relation, transition, rhythm | a universal score or human-outcome result |

Do not sum the three layers into a single quality number. In particular,
alignment, whitespace, object count, image presence, or PCA variance cannot
prove that a slide is good.

## Factor Model

The model is cognitive and instructional before it is stylistic. The factors
are a stable codebook, not a psychometric scale.

| Factor | Reader question | Fixed proxy observations | Flexible review prompt | Typical recovery action |
| --- | --- | --- | --- | --- |
| Focus and hierarchy | What registers first, and is it the intended claim? | declared font tiers, focal-box share, alignment cue ratio | Does the first signal match the inference goal without relying on small copy? | make the focal claim/relationship dominant; suppress competing primary signals |
| Load and segmentation | How many units must the reader integrate at once? | text density, text boxes, paragraphs, object density, declared font floor | Are units chunked by one inference, or merely placed in many cards? | split the inference, reserve height, reduce competing labels, move explanation to notes/sequence |
| Relational encoding | Can the required comparison, process, cause, hierarchy, or decision be seen? | connector/table/picture counts, visual area; declared relationship/grammar/cues | Is the visible grammar carrying the relation, rather than decorative imagery or labels alone? | choose a grammar from the relation; add deterministic arrows, axes, grouping, or state change |
| Guided transition | What does the reader trace, decide, practice, or transfer next? | declared reader task and reading path | Does the slide create a usable next mental or physical action? | expose the path, criterion, decision, or practice surface |
| Deck rhythm | Does repetition stabilize a learning routine or create fatigue? | silhouette frequency and consecutive-run count | Is the role of a pause, recap, comparison, workshop, or closure clear in sequence? | preserve useful routine but change spatial grammar at relation changes |
| Claim and evidence discipline | What does the slide establish, and what is still a hypothesis? | evidence labels, notes, content checks, provenance | Is a structural proxy being falsely presented as human understanding? | separate observation from interpretation and add the missing evidence surface |

## Data-Analysis Protocol

1. **Lock the sample.** Choose the target PPTX and only local reference decks
   that are current enough and presentation-like. Exclude archive, recovery,
   conversion-derived, and hidden diagnostic files from benchmark distributions.
2. **Observe without ranking.** The script outputs slide-level features and a
   correlation/PCA view across the selected files. PCA axes are descriptive
   co-variation of package variables, not latent human factors.
3. **Join the target's cognitive packet.** If the target has a
   `visual-silhouette-manifest.json`, pass it as `--cognitive-manifest` so the
   evaluator can report relationship, grammar, cue, and reading-path coverage.
4. **Review renders separately.** Use the exact-hash render/proxy contact sheet
   to code only those factors that require seeing the slide. Use the code
   template below. A proxy is neither a PowerPoint native-open proof nor a
   learner test.
5. **Decide one source-level action per weak pattern.** Fix the relationship,
   segmentation, or hierarchy in the source/manifest. Do not optimize the
   target merely to improve a percentile or PCA loading.
6. **Refresh evidence.** A source or copy change makes affected geometry,
   render, and native-open proof stale. Rerun the observer and the target's
   own package/native validators.

## Review Code Template

Save an optional JSON file in the evaluation surface. Codes make the flexible
judgment visible; they are not inputs fabricated by the parser.

```json
{
  "schema_version": "1.0",
  "reviewer_type": "llm_proxy_review | human_review",
  "render_boundary": "exact PPTX hash and the rendering/proxy used",
  "slides": [
    {
      "slide_id": "S01",
      "focus_hierarchy": "strong | adequate | conditional",
      "cognitive_load": "low | balanced | pressure",
      "relationship_legibility": "strong | adequate | conditional | not_applicable",
      "transition_affordance": "orient | trace | decide | practice | transfer | close | not_applicable",
      "deck_rhythm_effect": "anchor | explanation | transition | workshop | pause | recap | close",
      "overall_signal": "retain | revise | needs_human_review",
      "observation": "What is visibly present, without a human-outcome claim.",
      "recovery_action": "One source-level correction, if any."
    }
  ]
}
```

## Command

```bash
scripts/visual-authoring-runtime run scripts/analyze_slide_quality_factors.py \
  --target /absolute/path/current.pptx \
  --target-label current \
  --reference /absolute/path/reference-a.pptx \
  --reference /absolute/path/reference-b.pptx \
  --cognitive-manifest /absolute/path/visual-silhouette-manifest.json \
  --review-codes /absolute/path/review-codes.json \
  --output-dir /absolute/path/visual-authoring/evals/example
```

The output contains `analysis.json`, `slide-observations.csv`,
`factor-report.md`, and `target-proxy-profile.svg`.

## Fixed / Flexible / Decisional Ledger

| Layer | In this module |
| --- | --- |
| Fixed | package parsing, SHA-256, CSV fields, correlation/PCA calculation, output schema, read-only input rule |
| Flexible | sample choice, declared cognitive manifest, exact render selected for review, review observations, relation-specific recovery options |
| Decisional | `retain`, `revise`, `needs_human_review`; a decision cites an observed metric and a review/manifest path, then names one rerun surface |

## Runtime and Package Notes

- Runtime compatibility: `shared-core only / no-delta`.
- Dependencies: Python 3 standard library only; no network, model credential,
  external conversion renderer, native-app automation, or PowerPoint automation.
  Visual evidence is supplied separately through image/PDF render artifacts;
  native PowerPoint behavior remains a distinct manual release check.
- Permissions: reads the supplied PPTX/JSON paths; writes only to
  `--output-dir`.
- Source/license: this is a local `visual-authoring` diagnostic module. It
  implements no external scoring model and makes no proprietary benchmark
  claim.
