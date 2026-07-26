# Course Flow To Design System Sequence

This reference fixes the order for lecture-slide authoring when the project must
avoid choosing a visual style before the instructional meaning is known.

## Fixed Sequence

1. `course-flow-map.md`
   - Defines the whole course before slide design starts.
   - Required fields: `program_goal`, `audience_context`, `fixed_schedule`,
     `module_sequence`, `session_timing`, `learning_arc`, `output_chain`,
     `constraints_and_non_goals`.
2. `slide-planning-map.json`
   - Defines what each slide is doing for the learner.
   - Required fields per slide: `source_module`, `slide_goal`,
     `visual_situation`, `cognitive_operation`, `learner_action`,
     `output_artifact`, `timing_budget`, `evidence_boundary`, `reuse_policy`.
3. `symbol-inventory.json`
   - Collects the symbols that can carry the planned meanings.
   - Required fields per symbol: `symbol_id`, `semantic_role`,
     `source_context`, `target_expression_vector`, `possible_confusions`,
     `visual_candidates`, `selection_reason`, `learner_facing_boundary`.
4. `semantic-design-system.json`
   - Converts the planned course meaning and symbol set into a design system.
   - Required fields: `design_principles`, `symbol_mapping`, `layout_families`,
     `typography_rules`, `color_logic`, `image_style_rules`,
     `pptx_element_use`, `layout_element_calculations`,
     `accessibility_and_density`, `calculated_values`,
     `implementation_trace`.

## Design Start Boundary

Do not choose a template, palette, motif, image style, icon family, or recurring
layout family before the first three files exist. A design system is allowed
only after the workflow can show how the visual choices follow from:

- the whole lecture flow
- the slide-level learner action
- the symbols needed to carry the meaning
- the actual medium and accessibility constraints

## Layout Element Calculations

Every element that reaches a slide layout must have a calculation record. The
Korean labels below clarify the intent:

- `element_tradeoff` (`거래`): what attention cost and space cost are paid for
  the semantic gain.
- `placement` (`배치`): where the element sits relative to the learner's scan
  path, safe area, grouping, and action exit.
- `front_back_order` (`앞뒤 순서`): what should visually come forward or recede
  before native PPTX object order is finalized.

Required fields per layout element:

- `element_id`
- `semantic_role`
- `element_tradeoff`
- `attention_cost`
- `space_cost`
- `semantic_gain`
- `placement`
- `front_back_order`
- `reading_order`
- `native_object_order`
- `overlap_risk`

## Reuse Rule

The same layout family can be reused only when these four values are the same:

- `visual_situation`
- `cognitive_operation`
- `learner_action`
- `output_artifact`

If any value differs, the layout family must either change or record a concrete
reuse reason. Reuse without a reason is a design-system failure, not a visual
preference difference.

