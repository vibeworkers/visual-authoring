# Visual Strategy & Expression Select — 콘텐츠 우선 3축 계약 (Phase 3)

Phase 1(저작)·Phase 2(리뷰 게이트) 이후 구현 전에 세 축을 순서대로 정한다.

1. `content_visual_strategy`: 콘텐츠 관계와 독자 과업을 어떻게 보이게 할 것인가.
2. `expression_system`: 그 전략을 어떤 스타일 규칙으로 일관되게 표현할 것인가.
3. `medium_implementation_plan`: 목표 매체에서 어떤 객체·레이어·기능으로 구현할 것인가.

Carbon·Vivid·브랜드·Editorial·Custom은 둘째 축의 **옵션, 선택지, 도구**다. Carbon을 썼다는 사실은 시각화가 아니다. PowerPoint native object, 생성 이미지, SVG/HTML은 셋째 축의 구현 방식이며 Carbon과 같은 디자인 시스템 후보가 아니다. 예를 들어 Carbon을 PowerPoint native objects로 구현하거나, Vivid를 HTML/CSS로 구현하거나, Editorial을 image+native overlay로 구현할 수 있다.

## Content-Fit Quality Hierarchy

아래 우선순위를 뒤집지 않는다.

1. 콘텐츠·독자 과업·원하는 행동 적합성
2. 의미 관계·시각 계층·읽기/발화 흐름
3. 목표 매체의 의도적 구현과 수정 경계
4. 계산 가능한 배치 안정성·접근성·재현성
5. 렌더·패키지·native open 증거
6. 실제 사람의 이해·행동·학습성과 증거

삼성SDI 같은 기준작은 관찰용 레퍼런스가 될 수 있다. 그러나 사용자가 faithful recreation을 명시하지 않았다면 1:1 유사도는 pass gate가 아니다. `improved_variant`는 더 빨리 읽히는가, 콘텐츠 관계가 더 정확히 보이는가, 강의/업무 행동이 더 분명한가, 수정과 발표가 더 쉬운가, 목표 매체에서 안정적인가로 판정한다.

## 선택 절차

1. **지배 과업 판정** — 비교, 순서 이해, 판단, 조작, 기억, 실습, 감정적 전환 중 무엇이 핵심인가.
2. **콘텐츠 전략 탐색** — comparison, process, timeline, data story, scene, workshop board, editorial course, product simulation 등 내용 관계를 가장 잘 드러내는 후보를 비교한다.
3. **표현 시스템 탐색** — 스타일 선택이 결과를 바꾸며 명시적으로 고정되지 않은 경우 최소 3개 후보와 거절 근거를 기록한다.
4. **매체 구현 계획** — PowerPoint/Slides/HTML/SVG/image/hybrid와 native/vector/chart/table/image 경계를 정한다.
5. **검증 계획** — content fit, geometry, render, native, human outcome의 증거 표면을 분리한다.

명확한 브랜드 SoT나 사용자가 정한 시스템이 있으면 표현 시스템 축은 `settled_with_reason`으로 닫을 수 있다. 단, PPTX라는 매체 지정만으로 콘텐츠 전략이나 표현 시스템 검토를 생략하지 않는다. 형식적인 후보 3개를 채우는 대신 실제로 열려 있는 축을 탐색한다.

```yaml
content_visual_strategy: comparison | process | timeline | data_story | scene | workshop_board | editorial_course | product_ui_simulation | operational_dashboard | campaign | custom
strategy_rationale: <content relationship + reader task + desired action>
expression_candidates: [carbon, vivid, brand:<name>, editorial, custom]
selected_expression_system: carbon | vivid | brand:<name> | editorial | custom | none-with-reason:<reason>
expression_selection_state: explored | settled_with_reason
token_or_style_contract: --cds-* | --viv-* | --brand-* | --custom-* | pptx-theme-map:<id> | none-with-reason:<reason>
rejected_candidates:
  - <candidate>: <why not now>
medium_implementation_plan:
  medium_target: powerpoint | google_slides | html | svg | pdf | image | hybrid
  object_strategy: native | image | vector | chart_table | hybrid
  style_materialization: pptx_theme | slides_theme | css_tokens | svg_styles | raster | hybrid
content_fit_evidence: <reader_situation + cognitive_task + relationship + verification_surface>
no_default_assertion: true
```

## Artifact-Level System Lock, Scene-Level Freedom

디자인 시스템의 실제 값은 프로젝트마다 Flexible이지만, 한 산출물 안에서는 `design_system_lock`으로 고정한다. 잠금 대상은 `token_style_namespace`, `typography_hierarchy`, `spacing_density`, `component_grammar`, `status_semantics`, `accessibility_contrast`다. 잠금 뒤 바꾸려면 새 `lock_id`와 변경 이유를 남기고 기존 style/render proof를 stale 처리한다.

이 잠금은 레이아웃 템플릿이 아니다. 동일한 색·타입·간격·상태 문법을 쓰면서도 비교, 흐름, 작업 상태, 장면, 지도, 해부, 판단, 실습은 서로 다른 공간 구조·시점·실루엣을 가져야 한다. 같은 카드나 2단 구성을 반복하는 것은 시스템 일관성 증거가 아니다.

```yaml
design_system_lock:
  state: locked | not_applicable
  lock_id: <stable artifact id>
  reason: <required only when not_applicable>
  token_style_namespace: <single namespace or reason>
  typography_hierarchy: <role/scale policy>
  spacing_density: <rhythm/density policy>
  component_grammar: <shape/border/elevation/container rules>
  status_semantics: <accent/status meaning>
  accessibility_contrast: <contrast/readability/motion/reading-order policy>
scene_variation_policy:
  invariant: [<system grammar kept across scenes>, ...]
  intentionally_open: [<layout, camera, material, reading path, silhouette>, ...]
open_visual_materiality:
  candidate_space: open_set
  candidates: [<materially distinct scene or rendering approach>, ...]
  selected: <candidate or deterministic no-image route>
  selection_reason: <semantic/reader-task/medium fit>
  real_constraints: [<source, brand, license, safety, accessibility, medium, production>, ...]
```

`open_set`은 현재 나열할 수 있는 스타일 목록으로 제한하지 않는다. LLM이 이미지로 만들 수 있는 모든 표현은 실제 제약에 걸리지 않는 한 후보가 될 수 있다. 다만 후보 개방은 이미지 강제가 아니며, 구조·추상 관계가 더 정확하면 `SVG_ALLOWED`가 정답일 수 있다. 선택은 장면의 의미와 읽기 과업으로 하고, 유행·모델 기본 미감·도구 가용성만으로 닫지 않는다.

## 표현 시스템 후보 표

| 후보 | 잘 맞는 상황 | 반대 신호 | 필수 증거 |
|---|---|---|---|
| Carbon (`--cds-*`) | 운영·관리·데이터 판단·폼·신뢰 우선 표면 | 장면 기억, 캠페인 전환, 표지 임팩트가 핵심이면 약함 | 지배 과업이 판단/조작이라는 근거, 정보 밀도, 접근성·토큰 검증 |
| Vivid (`--viv-*`) | 캠페인·런칭·모집·키비주얼·감정/전환 유도 | 반복 업무, 수치 판단, 긴 본문 학습에서는 과자극 위험 | 감정/전환 과업, 대비/판독, reduced-motion, 5초 proxy |
| Brand (`--brand-*`) | 실제 브랜드 가이드·로고·서체·색·금지 규정이 우선 | 브랜드 자료가 말로만 있고 문서/자산이 없을 때 | brand SoT path, 사용·금지 경계 |
| Editorial/Course (`--custom-*`) | 교재·강의·워크숍의 개념 대비·순서·반복 학습 | 첫 화면 전환율이나 캠페인 임팩트가 주 목표 | learning sequence, section/slide job, repetition/contrast plan |
| Custom (`--custom-*`) | 위 시스템이 콘텐츠 구조나 브랜드 요구를 제대로 담지 못할 때 | 관례적 스타일 혼합만 있고 규칙이 없을 때 | 선택 이유, semantic variables, surface boundary, 검증 계획 |

Generated scene, Product UI Simulation, chart/table, diagram은 표현 시스템이 아니라 콘텐츠 전략 또는 구현 수단이다. 필요하면 어떤 표현 시스템과도 조합한다.

## 발화 신호의 해석

- “믿음직하게”, “차분하게”, “업무용”은 Carbon을 후보에 추가하지만 자동 선택하지 않는다.
- “몰입”, “임팩트”, “영화처럼”은 Vivid 또는 scene 전략을 후보에 추가하지만 자동 선택하지 않는다.
- “PPTX가 제공하는 기능”, “정석대로 편집 가능”은 표현 후보 점수가 아니라 `medium_implementation_plan.medium_target=powerpoint`와 `Native Object Intent Plan`을 활성화한다.
- “앱을 만든다”, “전체 동작 스케치”는 product UI simulation 전략을 추가한다. Carbon 사용 여부는 별도 판단이다.

## Vivid 강도 결정

Vivid 선택 시에만 Full(Stage D), Stage L, Restrained 중 강도를 고른다. Restrained는 Carbon 혼용이 아니라 Vivid 내부 강도 조절이다. 상세는 `tokens-vivid.md`.

## 혼합 산출물

표면별로 표현 시스템을 다르게 쓸 수 있지만 경계를 기록한다.

```yaml
surfaces:
  cover:
    content_visual_strategy: scene
    expression_system: vivid
    medium_implementation: image_plus_native_overlay
  worksheet:
    content_visual_strategy: workshop_board
    expression_system: editorial
    medium_implementation: powerpoint_native
  operations_console:
    content_visual_strategy: operational_dashboard
    expression_system: carbon
    medium_implementation: html_css
```

같은 화면에서 CSS token namespace를 즉흥 혼용하지 않는다. PowerPoint native object는 모든 표현 시스템과 병행 가능하므로 namespace 혼용 검사 대상이 아니다. PPTX에서는 선택한 style contract가 theme/master/layout/object style map으로 일관되게 물질화됐는지 검사한다.

## Cognitive Visual Encoding

시각 문법은 장식 유형이 아니라 독자가 관계를 읽고 추론하는 방식이다. 먼저 `inference_goal`을 쓰고, 관계에 맞는 후보를 비교한 뒤 `selected_grammar`와 거절 이유를 기록한다.

| 관계 | 우선 검토할 시각 문법 후보 |
|---|---|
| comparison | aligned contrast, matrix, paired scale |
| sequence / process | path, flow, staged progression |
| causality | cause-effect chain, feedback loop |
| hierarchy | tree, nesting, layered stack |
| cluster / map | spatial grouping, topology map |
| decision | branch, criteria matrix |
| anatomy | layered decomposition, annotated cutaway |
| timeline | temporal axis, before-after states |
| practice / workshop | workspace canvas, checkpoint loop |

이 표는 자동 스타일 매핑이 아니다. 같은 `comparison`도 독자가 차이를 찾는지, 우선순위를 고르는지, 격차 크기를 읽는지에 따라 문법이 달라진다. 표현 시스템은 선택된 문법을 일관되게 보이게 하고, 매체 계획은 이를 어떤 객체로 구현할지 정한다.

새 장형·다섹션 덱의 manifest는 schema v2로 판단과 증거 경계를 함께 보존한다. `evidence_state`는 `vector-language-cognition`의 enum을 그대로 소비하고, 사람 검증 전에는 human outcome을 주장하지 않는다.

## Semantic Silhouette Diversity

표현 시스템의 일관성과 장면 실루엣의 다양성을 분리한다. `Editorial`을 선택했다고 모든 슬라이드를 제목+2단 본문으로 만들지 않고, `차분함`을 선택했다고 의미 관계를 텍스트와 표로만 환원하지 않는다. 차분함은 채도·질감·모션·장식 강도를 낮추는 결정이며, 비교·순서·순환·계층·클러스터·지도·해부·스토리보드·의사결정 같은 관계 구조는 계속 달라야 한다.

장형 또는 다섹션 덱은 구현 전에 `visual-silhouette-manifest.json`을 작성한다.

```json
{
  "schema_version": 2,
  "policy": {
    "minimum_families": 0,
    "max_consecutive_same": 0,
    "dominant_family_cap": 0.0,
    "semantic_visualization_target": 0.0,
    "excluded_roles": []
  },
  "policy_rationale": "프로젝트 콘텐츠 관계와 반복 학습 행동에서 산정",
  "slides": [
    {
      "slide": 1,
      "unit_id": "S01-U01",
      "source_claim": "오늘의 학습 경로를 파악한다",
      "reader_task": "locate",
      "role": "session_open",
      "relationship_type": "orientation",
      "inference_goal": "세 세션의 순서와 도착점을 한 번에 파악한다",
      "candidate_grammars": ["path", "staged_progression"],
      "selected_grammar": "path",
      "selection_reason": "순서와 도착점을 동시에 보여준다",
      "visible_cues": ["directional_line", "three_checkpoints", "end_state"],
      "suppressed_cues": ["decorative_icons"],
      "reading_path": "left_to_right",
      "evidence_state": "inferred_proxy",
      "claim_boundary": "observable_proxy",
      "validation_boundary": {
        "technical_editability_proxy": "pass",
        "semantic_structure_proxy": "pass",
        "cognitive_readability_proxy": "not_run",
        "human_outcome_validation": "not_run"
      },
      "recovery_action": "순서 cue와 도착점 대비를 source에서 재설계",
      "silhouette_family": "asymmetric_editorial_open",
      "semantic_visual": true,
      "semantic_visual_eligible": true,
      "diversity_exception": null
    }
  ]
}
```

`minimum_families`, `max_consecutive_same`, `dominant_family_cap`, `semantic_visualization_target`은 프로젝트 Flexible 값이다. 실제 분포와 선언값의 일치 여부만 코드가 검사한다. 가족을 나눌 때는 색·모서리·장식이 아니라 읽기 경로와 공간 관계가 실제로 달라지는지를 본다.

다양성 예외가 가능한 경우:

- 동일한 작업지를 반복해 학습자가 작성 위치를 즉시 알아야 함
- 연속된 단계가 동일 화면의 상태 변화를 보여줌
- 의도적인 리듬 반복 뒤 강한 전환을 만들기 위한 짧은 구간

각 예외는 `diversity_exception`에 이유를 적는다. “일관성을 위해”만으로는 충분하지 않다.

## 안티패턴

- `신호 없음 -> Carbon`, `운영 장표 -> 무조건 Carbon`, `vivid 요청 -> 무조건 Vivid`.
- Carbon 적용을 시각화 완료로 보고.
- PowerPoint native 구현을 Carbon/Vivid와 같은 표현 시스템 후보로 취급.
- PPTX를 PNG/PDF 렌더 또는 shape 개수만 보고 native 품질까지 통과했다고 보고.
- 기준작과 닮았다는 이유만으로 improved variant를 선언.
- 선택 근거만 있고 실제로 열려 있던 후보의 거절 근거가 없음.
- artifact-level system lock을 같은 카드·같은 2단 레이아웃 반복으로 해석하거나, 장면 자유도를 token/style drift의 허가로 해석.
- LLM 이미지 표현의 후보 공간을 미리 정한 몇 가지 스타일 whitelist로 축소하거나, 반대로 open materiality를 이유로 source·brand·license·safety·accessibility·medium 제약을 무시.
- 생성 이미지를 장면 근거 없이 추상 배경으로 쓰고 “몰입”이라고 보고.
- 차분함을 실루엣 축소로, 일관성을 반복 레이아웃으로 해석.
- 색상·아이콘·장식 위치만 바꾼 동일 공간 구조를 서로 다른 실루엣으로 계산.
- 관계 시각화를 회피한 뒤 편집 가능성을 이유로 제시.
