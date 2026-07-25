# Universal Visual VLC Review Packet

Use this packet before visual production, visual QA, or release-level visual claims.

```yaml
visual_vlc_review_packet:
  source:
  artifact_type:
  surface_role:
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

All-route scene packet and image-route manifest:

```yaml
scene_first_judgement_packet:
  unit_id:
  source_sentence:
  artifact_role:
  one_scene_statement:
  scene_mode: concrete_world | operational_state | abstract_relationship
  concrete_entities: []
  action_or_state_change:
  core_read_3s:
  reader_inference_or_action:
  visible_cue: []
  semantic_boundary:
  deterministic_meaning_items: []
  design_system_lock_ref:
  materiality_candidate_space: open_set
  open_materiality_candidates: []
  selected_materiality_reason:
  route_status: SVG_ALLOWED | ROUTED_IMAGE_REQUIRED | INTEGRATED_HYBRID | SVG_PROXY_ONLY | BLOCKED_IMAGEGEN
  semantic_variable_ledger:
  pattern_class:
  visual_vocabulary_budget:
  localization_state: not_applicable | source_copy | translated_pending_reflow | concretized_pending_reflow | reflow_verified
  recovery_action:

image_production_manifest:
  route_status: CLASSIFICATION_PENDING | SVG_ALLOWED | ROUTED_IMAGE_REQUIRED | IMAGE_ASSET_PRESENT | INTEGRATED_HYBRID | SVG_PROXY_ONLY | BLOCKED_IMAGEGEN
  product_anchor:
  model_or_source:
  output_form_slug:
  prompt_or_source_ledger:
  image_output_path:
  integration_path:
  verification_path:
  deterministic_semantic_layer:
    owner:
    controls:
      - exact Korean labels
      - arrows and attention path
      - evidence callouts
      - accessibility/contrast/readability
  read_tests:
    three_second_read:
    five_second_proxy:
    label_hidden_thumbnail:
  human_outcome_validation:
```

Translation/concretization materialization packet (when visible or accessible copy changed):

```yaml
localization_reflow_packet:
  unit_id:
  language_owner: korean | source_author | other:<owner>
  source_phrase:
  rendered_phrase:
  preserved_facts: []
  affected_surfaces: []
  geometry_risks: []
  stale_proofs: []
  reflow_evidence:
    - surface:
      proof_type: render | geometry | native_open | accessibility | format
      path:
      fresh_after_copy_change: true
  localization_state: translated_pending_reflow | concretized_pending_reflow | reflow_verified
  recovery_action:
```

`translated_pending_reflow` and `concretized_pending_reflow` are blocking states. A wording change invalidates affected text-fit, geometry, render, PDF, native-open, and accessibility proof until fresh target-medium evidence closes `reflow_verified`.

Decision labels:

- `usable`: proxy gate ran with sufficient source/context/goal inputs and no blocking unsupported claim.
- `candidate`: proxy evidence is useful but external gates or human outcome evidence remain incomplete.
- `blocked`: required source, goal, runtime, format, or claim-boundary evidence is missing.
- `hypothesis only`: the request is too early or too abstract for a release-oriented judgment.

Required closeout:

```yaml
visual_vlc_review_result:
  decision:
  route_status:
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
