# PowerPoint Native Object Intent / Geometry / Semantic Coverage Contract

PowerPoint native는 “편집 가능한 도형이 몇 개 있는가”가 아니다. 슬라이드의 의미 단위를 PowerPoint가 제공하는 객체·구조·발표 기능으로 **왜, 어떻게, 어디까지** 구현할지를 빌드 전에 선언하고, 빌드 후 실제 PresentationML 객체와 대응시켜 검증하는 계약이다.

## 역할

- 표현 시스템(Carbon/Vivid/Brand/Editorial/Custom)과 직교한다. 어떤 표현 시스템도 PowerPoint native object로 구현할 수 있다.
- 모든 것을 도형으로 만드는 규칙이 아니다. 사진적 장면·복잡한 일러스트·질감은 image layer가 더 적합할 수 있다.
- 의미·수정 가치·발표 행동이 큰 요소는 native가 우선이다. 표, 차트, IA, 과정, 타임라인, 라벨, 콜아웃, 연결선, 제목, 노트, 반복 구조가 대표적이다.
- native object count나 shape ratio만으로 quality pass를 선언하지 않는다.

## 빌드 전 산출물: `native-object-intent-plan.json`

```json
{
  "contract_version": "1.0",
  "target_medium": "powerpoint",
  "style_materialization": "pptx_theme",
  "threshold_profile": {
    "profile_id": "project-v1",
    "safe_margin_pt": 0,
    "alignment_tolerance_pt": 1.5,
    "spacing_tolerance_ratio": 0.15,
    "spacing_tolerance_pt_when_zero": 1.5,
    "overlap_epsilon_ratio": 0.01,
    "unplanned_text_overlap_epsilon_ratio": 0.01,
    "connector_endpoint_tolerance_pt": 3,
    "minimum_native_unit_coverage": 0,
    "minimum_required_relation_coverage": 1
  },
  "slides": [
    {
      "slide_number": 1,
      "units": [
        {
          "unit_id": "claim-title",
          "slide_number": 1,
          "semantic_role": "assertion",
          "criticality": "critical",
          "native_requirement": "required",
          "expected_native_type": "text",
          "planned_object_names": ["claim-title"],
          "edit_boundary": "text_and_position",
          "group_name": null,
          "z_order": 3,
          "reading_order": 1,
          "presentation_behavior": "always_visible",
          "raster_exception_reason": null,
          "required_relations": [
            {"type": "inside_safe_area"},
            {"type": "align_left", "with": "evidence-panel"},
            {"type": "vertical_gap", "with": "evidence-panel", "target_pt": 18},
            {"type": "separate", "with": "evidence-panel"}
          ]
        }
      ]
    }
  ],
  "overlap_exceptions": [],
  "waivers": []
}
```

### 의미 단위 필수 필드

| 필드 | 의미 |
|---|---|
| `unit_id`, `slide_number`, `semantic_role` | 의미 단위 식별과 슬라이드 역할 |
| `criticality` | `critical`, `high_change`, `supporting` |
| `native_requirement` | `required`, `preferred`, `raster_allowed`, `not_applicable` |
| `expected_native_type` | `text`, `shape`, `table`, `chart`, `connector`, `group`, `picture`, `any_native` |
| `planned_object_names` | PowerPoint Selection Pane/XML `cNvPr@name`과 연결되는 이름 |
| `edit_boundary` | 사람이 바꿀 수 있어야 하는 범위 |
| `group_name`, `z_order`, `reading_order` | 그룹·앞뒤·접근성/발표 읽기 순서 |
| `required_relations` | `inside_safe_area`, `separate`, `contain`, `overlay`, `align_*`, `horizontal_gap`, `vertical_gap`, `connect` |
| `presentation_behavior` | 항상 표시, 단계 공개, 발표자 설명과 동기화 등 |
| `raster_exception_reason` | image/hybrid 예외의 의미·편집성 손실 이유 |

객체 이름은 사람이 PowerPoint Selection Pane에서 이해할 수 있는 semantic name을 사용한다. 자동 생성된 `Rectangle 17` 같은 이름만으로 intent coverage를 닫지 않는다.

### 선언하지 않은 텍스트 겹침 차단

선언된 `separate` 관계만 검사하면, 서로 다른 카드·라벨이 intent plan에 직접 연결되지 않았을 때 겹침을 놓칠 수 있다. 감사기는 같은 슬라이드의 서로 다른 native text object를 모두 비교하고, 교차 면적이 더 작은 bbox의 `unplanned_text_overlap_epsilon_ratio`를 넘으면 `unplanned_text_overlap`으로 차단한다.

의도적으로 글자를 겹쳐 연출해야 할 때만 다음처럼 두 semantic object name과 이유를 함께 선언한다. 일반 `waiver`로 계산 결과를 숨기지 않는다.

```json
"overlap_exceptions": [
  {
    "slide_number": 4,
    "object_names": ["Title: S04", "Typography Accent: S04"],
    "reason": "두 텍스트는 같은 문장을 겹쳐 보이는 의도적 타이포그래피 레이어다."
  }
]
```

이 예외는 **정확히 두 개의 이름**과 비어 있지 않은 이유를 요구한다. 이름이 없거나 중복된 예외는 intent schema에서 막는다. bbox 겹침 검사는 실제 glyph·줄바꿈·폰트 fallback을 볼 수 없으므로, 이 통과도 render/PowerPoint visual review를 대신하지 않는다.

## 의도적으로 다룰 PowerPoint 기능

- slide master, layout, theme, placeholders로 반복 구조와 style을 소유한다.
- title placeholder 또는 명시적 title object를 모든 슬라이드에 둔다.
- 표·차트는 데이터와 구조를 수정할 필요가 있으면 native table/chart를 사용한다.
- process/IA/relation은 shape와 실제 연결 대상이 있는 connector로 만든다.
- 의미 그룹은 group과 semantic object name으로 선택·이동 가능하게 한다.
- z-order와 reading order를 우연한 생성 순서에 맡기지 않는다.
- 강의 진행 정보는 speaker notes에 두고 작은 본문에 숨기지 않는다.
- alt text와 reading order는 주요 그림·차트·도형의 접근성 계약이다.
- animation/transition은 교육적 순차 공개나 발표 행동이 있을 때만 쓰며, 없으면 사용하지 않는 것이 정상이다.
- PowerPoint 전체 기능을 무조건 켜지 않는다. `references/pptx-native-conformance-and-self-remediation.md`의 core capability catalog에서 각 기능을 `used`, `intentionally_not_used`, `not_applicable`로 분류하고 그 이유를 남긴다.

## PowerPoint Convention Companion Contract

이 intent plan은 **의미 단위와 geometry**를 소유한다. 다음 PowerPoint 관례는 별도 `pptx-native-conformance-contract.json`에서 소유하고, `scripts/validate_pptx_native_conformance.py`가 exact PPTX와 대조한다.

- master/layout/theme과 Pretendard major/minor Latin·East Asian font
- native title placeholder, native section list, TOC native text, ordered title story
- automatic slide-number placeholder/field
- 기본 도형 text의 가로 가운데(`a:pPr@algn=ctr`)·세로 가운데(`a:bodyPr@anchor=ctr`)와 named exception
- picture/image typography의 raster exception, semantic reason, equivalent text
- recovery incident를 source로 거절하고 report/repair plan만 쓰는 source-level self-remediation

두 계약은 대체하지 않는다. conformance가 pass여도 critical semantic unit의 native type·connector·geometry relation을 보장하지 않으며, native-object audit가 pass여도 automatic number나 theme font·title story를 보장하지 않는다.

## Fixed 계산

객체 bbox를 슬라이드 좌표와 point 단위로 읽고, intent plan의 관계와 tolerance에 대해 계산한다. 모든 간격을 같게 만드는 것이 아니라 **그룹별로 선언한 목표 관계와의 오차**를 계산한다.

- `out_of_bounds_non_bleed_count`: `inside_safe_area` 객체가 safe area를 벗어난 수.
- `unintended_overlap_count`: `separate` 관계의 두 객체 교차 면적이 허용치를 넘은 수.
- `unplanned_text_overlap_count`: 선언된 예외가 없는 서로 다른 native text object의 bbox 교차가 허용치를 넘은 수.
- `overlap_ratio = intersection_area / min(area_a, area_b)`.
- `max_alignment_error_pt`: 선언한 alignment edge/center 사이 거리의 최대값.
- `max_spacing_deviation_ratio = |actual_gap - target_gap| / target_gap`. 목표가 0이면 절대 오차를 쓴다.
- `detached_required_connector_count`: `connect` 관계의 connector가 대상 object id에 결속되지 않은 수.
- `object_density`: 객체 수 / 슬라이드 면적. 경고용 관찰값이며 미적 점수가 아니다.
- `read_order_mismatch_count`: critical unit의 선언 reading order와 실제 top-level XML/object order가 다른 수.
- `geometry_constraint_coverage`: 감사된 required relation / 선언된 required relation.
- `native_unit_coverage`: 객체 존재·유형 일치·필수 관계 구현을 모두 만족한 eligible unit / eligible unit.
- `critical_native_coverage`: 같은 조건을 만족한 critical unit / critical unit.
- `required_relation_coverage`: 통과한 required relation / required relation.
- `raster_exception_rate`: 승인된 raster unit / native eligible unit.

분모가 없으면 full coverage로 보고하지 않고 `not_applicable`로 기록한다. 텍스트 잘림은 package geometry만으로 확정하지 않는다. 코드의 `text_fit_risk_count`는 기술적 proxy일 뿐이며, `confirmed_text_clipping_count`는 PowerPoint/렌더 proof에서 별도로 기록한다.

## Fixed / Flexible / Decisional

| 층 | 소유 | 예 |
|---|---|---|
| Fixed | schema, 계산식, parser/validator, evidence state, status enum | bbox·overlap·alignment·spacing·connector·coverage 계산, hash, stale 규칙 |
| Flexible | 프로젝트 intent plan과 시각 후보 | 의미 단위, criticality, 목표 간격, tolerance 근거, safe area, native/image/hybrid 구성 |
| Decisional | fixed 결과 + content fit + 사람/렌더 증거 | `pass_local`, `revise`, `blocked`, `needs_human_choice`, waiver 수용 여부 |

문서에 계산 항목을 적는 것만으로 Fixed가 되지 않는다. `scripts/audit_pptx_native_objects.py`처럼 동일 입력에서 동일 출력을 내는 실행 가능한 검증기가 있어야 한다.

## 판정 계약

다음은 critical/exact-zero blocker다.

- `out_of_bounds_non_bleed_count = 0`
- `unintended_overlap_count = 0`
- `unplanned_text_overlap_count = 0`
- `detached_required_connector_count = 0`
- `critical_native_missing_count = 0`
- `critical_object_type_mismatch_count = 0`
- `critical_required_relation_missing_count = 0`
- `critical_read_order_mismatch_count = 0`
- `critical_native_coverage = 1.0` 또는 critical unit이 없으면 `not_applicable`
- `required_relation_coverage = 1.0` 또는 relation이 없으면 `not_applicable`

Noncritical coverage 목표와 tolerance는 프로젝트가 빌드 전에 `minimum_native_unit_coverage`로 선언한다. 모든 required relation은 기본적으로 `minimum_required_relation_coverage = 1.0`을 요구한다. intent plan이 없으면 native semantic quality의 `status`는 `blocked`, `decision_code`는 `blocked_missing_intent_plan`이다. geometry 감사만 통과하면 `pass_local` 후보가 될 뿐, 콘텐츠 적합성·좋은 디자인·학습자 이해를 증명하지 않는다.

## Waiver

Waiver는 측정값을 지우거나 pass로 바꾸지 않는다. 의도적인 text-on-text 연출은 위 `overlap_exceptions`에서 이름 두 개와 이유로만 다룬다. 일반 waiver는 다음 필드가 필요하다.

```yaml
slide_number: 4
unit_or_object_id: scene-base
finding_id: geometry-004
reason: photographic scene intentionally bleeds beyond slide bounds
owner: <name-or-role>
review_condition: revisit when base image changes
expires_or_review_date: <date-or-event>
```

## 빌드 후 증거

`native-object-audit.json`은 최소 다음을 포함한다.

- PPTX 절대 경로와 SHA-256
- intent plan 경로와 SHA-256
- slide size, slide/object inventory
- threshold profile id와 실제 값
- slide/object/relation별 finding
- 계산 metrics와 evidence state `observed_computation`
- `pass_local | revise | blocked | needs_human_choice`
- 계산기의 미지원 범위

PPTX 재빌드 시 geometry/native/render/manual-open 증거는 전부 stale이다. fresh hash로 다시 감사한다.

## 증거 경계

- package/XML audit: 객체 존재·유형·ID·bbox·group·connector·master/layout·notes·object order를 증명한다.
- geometry audit: 선언한 제약과 실제 좌표의 편차를 증명한다.
- semantic ledger: 계획 대비 구현 coverage를 증명한다.
- render proof: 해당 렌더러에서 보이는 외형·잘림을 증명한다.
- fresh PowerPoint open: 복구 경고 없이 열리는지 증명한다.
- 실제 selection/edit test: 사람이 객체를 선택·수정할 수 있는지 증명한다.
- learner test: 이해·기억·전이·행동을 증명한다.

어느 하나도 나머지를 대신하지 않는다.
