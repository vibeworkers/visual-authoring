# Slide Quality Factor Observation

## Judgment Boundary

This is a cognitive-quality **diagnostic**, not a single quality score or a proof of aesthetic quality, comprehension, learning transfer, accessibility, or Microsoft PowerPoint native-open success. Package observations, declared cognitive structure, and optional human/LLM review codes remain separate.

## Dataset

- Target: `prompt-engineering-whole-work.fresh-v15` — 23 slides, SHA-256 `46f706c93dc8046f27563a64a166ca829d61d9a1157de36c93158d190179f0c5`.
- Local structural reference decks: 10 deck(s), 202 slides.
- Reference decks establish descriptive proxy distributions only; their topic, audience, and visual strategy are not normalized.

## Target Median in the Local Structural Sample

The percentile below is a location in the heterogeneous local sample, not a better/worse direction.

| Package proxy | Target median | Reference median | Target-median location in reference slides |
| --- | ---: | ---: | ---: |
| text_density_chars_per_1000pt2 | 1.445 | 1.014 | 87.1% |
| paragraph_count | 13.000 | 17.000 | 34.1% |
| object_density_per_million_pt2 | 32.793 | 28.935 | 59.5% |
| occupied_area_ratio | 0.546 | 0.732 | 9.5% |
| picture_count | 0.000 | 0.000 | 49.5% |
| focal_box_ratio | 0.165 | 0.176 | 42.3% |
| alignment_cue_ratio | 0.618 | 0.681 | 43.8% |
| title_to_median_font_ratio | 1.846 | 2.286 | 21.9% |

## Cognitive Factor Model

| Factor | Fixed observations | Flexible cognitive judgment | Do not infer |
| --- | --- | --- | --- |
| Focus & hierarchy | declared font tiers, focal-box share, alignment cues | what should register first and whether it is visually dominant | aesthetic quality or comprehension |
| Load & segmentation | text density, paragraph/object count, minimum declared font | whether the reader must integrate too many units at once | actual readability or learning burden |
| Relational encoding | pictures/connectors/tables plus declared relation, grammar, cues | whether the visual grammar makes the required inference available | that an image or connector is explanatory |
| Guided transition | declared reader task and reading path | whether explanation changes into a decision, practice, or transfer action | learner transfer |
| Deck rhythm | silhouette family frequency and manual rhythm code | whether repetition is a stabilizing pattern or fatigue | engagement or pacing success |

## Target Deck Observations

| Slide | Focus proxy | Load headroom proxy | Relation declaration | Manual review signal |
| --- | --- | --- | --- |
| S01 | middle within deck | more headroom within deck | 4/4 | retain |
| S02 | middle within deck | middle within deck | 4/4 | needs_human_render_review |
| S03 | higher within deck | more headroom within deck | 4/4 | retain |
| S04 | middle within deck | middle within deck | 4/4 | retain |
| S05 | middle within deck | less headroom within deck | 4/4 | retain |
| S06 | lower within deck | middle within deck | 4/4 | retain |
| S07 | middle within deck | middle within deck | 4/4 | retain |
| S08 | higher within deck | middle within deck | 4/4 | retain |
| S09 | lower within deck | middle within deck | 4/4 | revise_source |
| S10 | middle within deck | middle within deck | 4/4 | retain |
| S11 | middle within deck | less headroom within deck | 4/4 | retain |
| S12 | higher within deck | middle within deck | 4/4 | revise_source |
| S13 | middle within deck | middle within deck | 4/4 | revise_source |
| S14 | middle within deck | less headroom within deck | 4/4 | retain |
| S15 | higher within deck | less headroom within deck | 4/4 | needs_human_render_review |
| S16 | higher within deck | middle within deck | 4/4 | revise_source |
| S17 | middle within deck | less headroom within deck | 4/4 | needs_human_render_review |
| S18 | middle within deck | less headroom within deck | 4/4 | retain |
| S19 | middle within deck | middle within deck | 4/4 | retain |
| S20 | lower within deck | middle within deck | 4/4 | retain |
| S21 | lower within deck | more headroom within deck | 4/4 | retain |
| S22 | middle within deck | more headroom within deck | 4/4 | revise_source |
| S23 | lower within deck | more headroom within deck | 4/4 | retain |

## Descriptive PCA

- Status: `observed_descriptive_pca`.
- The PCA is an exploratory co-variation view of package proxies. It does not validate the conceptual factors above.
- Axis 1: 46.0% variance; strongest loadings: alignment_cue_ratio (+0.898), object_density_per_million_pt2 (+0.859), paragraph_count (+0.778).
- Axis 2: 17.3% variance; strongest loadings: occupied_area_ratio (-0.792), picture_count (+0.619), focal_box_ratio (-0.449).
- Axis 3: 9.7% variance; strongest loadings: picture_count (+0.724), focal_box_ratio (+0.407), occupied_area_ratio (+0.325).

## Evidence States

- structural_package: observed computation for the exact PPTX hashes listed above.
- reading/cognitive: declared packet plus optional reviewer coding; it is a hypothesis about cognitive support, not an outcome measure.
- viewing_render: not produced by this script; any referenced slide proxy must be reviewed separately.
- native_runtime: not produced by this script.

## Next Action

Use lower-headroom or conditional-review slides as candidates for slide-scoped render review. Repair source structure or visual grammar, then rerun this observer; do not tune the deck merely to raise these proxy values.
