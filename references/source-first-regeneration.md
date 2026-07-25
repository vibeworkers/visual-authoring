# Source-First Regeneration

원본이 있는 시각 저작은 먼저 그 원본의 **역할**을 분류한다. faithful recreation/transfer를 약속한 baseline은 해체·대조가 필요하다. 참고용 benchmark는 관찰 대상이지 1:1 합격 기준이 아니다. “더 나은 구조·편집성·전달력”은 콘텐츠 적합성으로 판단하며, benchmark 유사도로 대체하지 않는다.

## When To Use

Use this reference when the user provides or points to:

- existing PPTX, PDF, HTML, image, screenshot, manuscript, sketch, or rendered slide deck,
- a request such as “그대로 옮기자”, “네이티브 객체로 바꿔가기”, “원본과 비교”, “업데이트도 다시 생성”, “편집 가능하게”,
- a quality critique where the expected target is defined by an older artifact.

If no original artifact exists, record `source_first: skipped_no_original`.

## Source Decomposition Packet

```yaml
source_first:
  status: required | skipped_no_original | blocked_missing_source
  original_sources:
    - id: src-001
      path_or_handle: ""
      type: pptx | pdf | image | html | doc | sketch | screenshot | other
      source_role: baseline_to_recreate | legacy_to_improve | reference_only | asset_pool | evidence_source
      source_contract: fidelity_baseline | reference_benchmark
      version_or_date: ""
      read_only_boundary: true
      provenance_note: ""
  target:
    artifact_type: pptx | html | pdf | images | markdown | app_ui | other
    audience: ""
    delivery_context: ""
    editability_target: high | medium | low
    parity_target: pixel_close | structure_close | meaning_close | improved_variant | not_applicable_reference
  decomposition:
    scenes:
      - source_scene_id: ""
        intent: ""
        reader_action: ""
        information_units: []
        visual_hierarchy: []
        reading_order: []
        native_features_observed: []
        assets: []
        text_units: []
        risks_or_gaps: []
  decisions:
    preserve: []
    transfer: []
    discard: []
    regenerate: []
  proof_plan:
    render_proof: []
    native_proof: []
    source_parity_table: required_for_fidelity | not_applicable_reference
    content_fit_observation: required
```

## Sequential Action Plan

| Step | Action | Output |
|---:|---|---|
| 0 | Fix scope | target artifact, audience, delivery format, editability target |
| 1 | Acquire source | file paths, screenshots, version, permission/read-only boundary |
| 2 | Inventory source | scenes/pages/slides, assets, text, tables, charts, native features |
| 3 | Decompose source | scene intent, IA, visual hierarchy, reading order, object relationships |
| 4 | Decide treatment | preserve / transfer / discard / regenerate labels with reasons |
| 5 | Restate goal | what must remain same, what should improve, what may change |
| 6 | Author packet | decomposition packet + outline notes + evidence boundary |
| 7 | Lock content source | learner text, speaker notes, evidence table, production source |
| 8 | Map visual structure | slide/page map, IA, object hierarchy, reading order |
| 9 | Select visual strategy/expression | content strategy, optional expression systems, rejection reasons, style contract |
| 10 | Decide medium implementation | editability value + Native Object Intent Plan + image/native/hybrid boundary |
| 11 | Implement | native objects + image base + meaning layer + notes/theme/layout |
| 12 | Verify render | screenshot/PDF/PNG/HTML proof |
| 13 | Verify native | open check, editable objects, notes, accessibility/read order |
| 14 | Verify by source role | fidelity baseline: source parity table; reference benchmark: content-fit observation |
| 15 | Classify feedback | fix_now / defer / reject_with_reason |
| 16 | Regenerate | rebuild from updated packet; previous proof becomes stale |

## Preserve / Transfer / Discard / Regenerate

| Label | Meaning | Examples |
|---|---|---|
| `preserve` | Keep the original content or visual role as-is | title wording, section order, approved brand mark, legally fixed text |
| `transfer` | Recreate in the target medium with the same meaning | table as editable PPTX table, IA diagram as shapes/connectors, labels as text boxes |
| `discard` | Remove intentionally | decorative noise, stale metadata, duplicated files, confusing motif |
| `regenerate` | Rebuild because the original intent is right but execution is weak | weak slide 6 visualization, inconsistent cover/interior tone, poor font scale |

Do not use `discard` as a shortcut for content that is merely hard to implement. Record the reason and the expected reader impact.

## Editability Value

Native editability is valuable when the object carries meaning or must be changed by a human later. Use this test before converting images into shapes:

| Signal | Native object favored | Image layer favored |
|---|---|---|
| Meaning density | process, IA, table, chart, timeline, label, relation | mood, texture, photograph, cinematic scene |
| Fit to slide job | central claim or workshop action | background atmosphere |
| Expected edits | likely to revise text, order, data, arrows | unlikely to revise exact form |
| Native support | PowerPoint can express it cleanly | requires complex illustration/fidelity |
| Fidelity risk | simple geometry/text | high risk if recreated as primitives |

Rule: editability follows meaning and fit, not technical possibility. A shape is not worth native conversion just because it can be drawn.

## Reference Benchmark Boundary

`reference_only`, `asset_pool`, `evidence_source`는 `reference_benchmark` 계약이다. 이 경로에서는 기준작을 대표 슬라이드와 1:1로 나란히 놓는 것을 pass 조건으로 만들지 않는다. 다음만 관찰한다.

- 정보 밀도와 화면당 한 가지 핵심 일의 처리 방식
- 제목·본문·도표·장면의 계층
- 반복되는 리듬, 여백, 이미지/도형/표의 역할
- PowerPoint native 기능을 어디에 의도적으로 썼는지
- 현재 콘텐츠·독자·강의 행동에 전이할 가치가 있는 원리와 버릴 원리

`improved_variant` 판정은 Content-Fit Quality Hierarchy에 따른다. benchmark와 더 닮았다는 이유만으로 improved가 되지 않고, 다르게 생겼다는 이유만으로 fail이 되지 않는다.

## Source Parity Table

Use one row per source scene/page/slide or per meaningful object group.

| source_id | target_id | parity_target | status | matched | changed | missing | intentional_gap | proof |
|---|---|---|---|---|---|---|---|---|
| src-01 | slide-01 | meaning_close | matched | title, section role | font scale | none | visual system updated | screenshot + open check |

Status values:

- `matched`: source intent and required content are present.
- `changed`: different from source, with explicit improvement or medium reason.
- `missing`: required source element absent; cannot close release.
- `intentional_gap`: omitted by decision, with reason and owner acceptance.

## PPTX Native Transfer Rules

- Use slide master/layout/theme/placeholders for repeated structure, not duplicated floating shapes.
- Use title placeholders or explicit title objects for every slide.
- Use speaker notes for facilitation content; do not hide facilitation logic in small slide text.
- Use editable tables/charts/shapes/connectors for high-editability meaning units.
- Use image base layers for complex generated scenes, screenshots, photographic content, or fidelity-sensitive illustrations.
- Put Korean labels, arrows, callouts, read order, and alt text in native/meaning layers when they carry instructional meaning.
- Run fresh manual PowerPoint open proof after every rebuild. A previous open proof is stale.
- Create `native-object-intent-plan.json` before build and map source semantic units to target semantic object names, expected native types, edit boundaries, reading/z-order, and required geometry relations.
- Run a fresh native-object audit after build. Object existence alone does not close coverage; type and required relations must also match.

## 3-Layer Ledger

| Layer | Fixed | Flexible | Decisional |
|---|---|---|---|
| Source-first regeneration | action order, source-role enum, parity status labels, rebuild-stale rule | actual source files, slide count, screenshots, brand/font values, parity/content-fit evidence paths | preserve/transfer/discard/regenerate choices, source contract, parity target, native-vs-image judgment |

Do not turn flexible project evidence into global defaults. Do not treat a decisional native-vs-image choice as proof without render/native/source-parity evidence.

## Failure Patterns

- Building from memory of the artifact instead of the artifact itself.
- Converting every visual shape into PowerPoint primitives even when fidelity matters more than editability.
- Keeping everything as a full-slide image when text, IA, tables, and notes are the actual editable meaning.
- Forcing new-vs-original parity when the source is only a reference benchmark.
- Calling a deck improved because it looks more like the benchmark while fitting the current content worse.
- Calling an update “done” after a patch when the source packet changed; source-first update means regenerate from the revised packet.
