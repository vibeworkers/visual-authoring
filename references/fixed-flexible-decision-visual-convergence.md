# Fixed–Flexible–Decision Visual Support Convergence Pattern

## 목적

긴 문서·슬라이드·화면 묶음에서 시각적 지원이 가장 약한 장면을 반복해서 끌어올리되, 모든 장면을 같은 레이아웃으로 평준화하지 않는 범용 개선 패턴이다.

한 문장으로 줄이면 다음과 같다.

> 현재 가장 약한 장면과 의미를 가장 잘 지원한 장면을 찾아, 강한 장면의 겉모양이 아니라 지원 원리를 추출하고, 그 원리를 약한 장면과 다른 장면에 각각 맞게 전이한 뒤, 의도한 구현과 증거를 분리해 검증하는 루프를 최소 다섯 번 수행한다.

이 패턴은 한 번의 수정 기법이 아니라 반복 실수를 줄이는 학습 장치다. 기존 작업에서 효과가 있었던 원리를 다음 장면의 입력으로 바꾸며, 같은 실패가 다시 나타나면 prose 주의사항에서 실행형 stop condition으로 승격한다.

## 적용 조건

다음 중 하나 이상이면 이 패턴을 사용한다.

- 장형·다섹션 덱, 문서, 앱 화면군처럼 장면 간 시각적 지원 편차가 크다.
- "가장 약한 슬라이드를 찾아 계속 개선", "최소 다섯 번", "편차를 줄여", "같은 실수를 반복하지 않게" 같은 요청이 있다.
- 일부 장면은 의미가 잘 드러나지만 다른 장면은 표·문장·카드에 머물러 있다.
- geometry, native object, render proof는 있지만 콘텐츠 관계가 잘 보이는지는 별도 검토가 필요하다.
- 기준작이나 기존 산출물을 넘어서는 개선 원리를 현재 콘텐츠에 맞게 전이하려 한다.

다음 경우에는 전체 패턴을 강제하지 않는다.

- 한 문장, 한 색, 한 객체 위치만 고치는 단발 편집.
- faithful recreation만 목표이며 원리 전이보다 source parity가 우선인 작업.
- 장면이 하나뿐이고 반복 학습이나 장면 간 편차가 존재하지 않는 산출물.

## 층과 순서를 구분한다

`Fixed / Flexible / Decision`은 **무엇을 어디에 둘지 나누는 층**이다. 실제 반복 순서는 다음과 같다.

```text
Decision premise
→ Flexible exploration
→ Fixed realization and audit
→ Decision close
→ learning update
```

즉 Decision은 마지막 판정만이 아니다. 시작할 때 무엇을 약점으로 볼지와 이번 회차의 목표를 고정하고, 끝날 때 결과를 채택·재수정·보류한다.

| 층 | 이 패턴에서 맡는 일 | 맡지 않는 일 |
|---|---|---|
| **Fixed** | source/scene id, 필수 ledger 필드, 최소 5회, 선언된 객체 관계, bbox·간격·겹침·경계·connector·hash·schema·native audit, 증거 freshness | 좋은 디자인, 콘텐츠 적합성, 사람 이해를 자동 판정하지 않음 |
| **Flexible** | 약한/강한 장면 후보, 표현 문법, 실루엣, 레이아웃, 밀도, 색, 이미지/native/SVG/chart 조합, 프로젝트별 tolerance와 예외 | Carbon·Vivid·native 같은 한 도구를 전역 기본값으로 고정하지 않음 |
| **Decision** | 콘텐츠와 독자 과업에 비추어 약한/강한 장면 선택, 전이 원리 채택, `pass_local/revise/blocked/needs_human_choice`, 다음 회차 선택 | fixed 관찰이나 사람 증거 없이 개선을 선언하지 않음 |

Carbon, Vivid, Brand, Editorial, Custom은 Flexible 후보인 표현 시스템이다. PowerPoint native object, image, SVG, chart/table은 별도 매체 구현 선택이다. 둘 다 시각화 자체나 콘텐츠 적합성 판정이 아니다.

## 시각적 지원 단위

장면을 "예쁘다/안 예쁘다"로 정렬하지 않는다. 다음 다섯 지원 축을 `clear / partial / absent / not_applicable`로 관찰한다.

1. `relationship_support`: 비교·과정·인과·계층·판단 등 핵심 관계가 보이는가.
2. `priority_support`: 무엇이 먼저이고 무엇이 중요한지 계층이 보이는가.
3. `inference_or_action_support`: 독자가 무엇을 추론하거나 다음에 무엇을 해야 하는지 보이는가.
4. `evidence_or_completion_support`: 근거, 확인 지점, 완료 조건, 재시도 조건이 보이는가.
5. `medium_support`: 목표 매체에서 읽고 설명하고 수정하는 행동을 의도한 객체·노트·상태가 지원하는가.

이 라벨은 reviewer의 bounded judgment다. 코드는 장면별 라벨 분포와 `absent` 개수, 반복 family 집중도, 선언 대비 실제 geometry를 집계할 수 있지만 라벨을 생성하거나 미적 점수로 승격하지 않는다.

`support_floor`는 현재 장면군에서 가장 취약한 지원 상태다. 편차를 줄인다는 말은 평균적인 모양을 같게 만드는 것이 아니라, 이 낮은 꼬리를 끌어올리면서 관계에 필요한 실루엣 차이는 보존한다는 뜻이다.

## 약한 장면과 강한 장면을 고르는 법

### 약한 장면

다음 우선순위로 고른다.

1. 독자 과업에 필수인 지원 축이 `absent`인 장면.
2. 핵심 관계가 문장·표·카드 안에 접혀 있는 장면.
3. 행동·완료·근거 cue가 없어 강사의 구두 설명에만 의존하는 장면.
4. 같은 generic silhouette가 반복되어 콘텐츠 차이를 지우는 장면.
5. fixed audit는 통과하지만 시각적 의미 지원이 약한 장면.

### 강한 장면

다음 조건을 충족한 장면을 고른다.

- 관계, 우선순위, 행동 또는 증거가 실제 visible cue로 드러난다.
- 읽기 경로와 발표/조작 행동이 장면 구조에 연결된다.
- 표현 시스템이 아니라 콘텐츠 관계가 성공 이유를 설명한다.
- 다른 장면에 그대로 복제하지 않고도 원리로 추출할 수 있다.

강한 장면은 가장 화려하거나 기준작과 가장 닮은 장면이 아니다.

## 표면이 아니라 원리를 전이한다

강한 장면에서 다음 4항을 추출한다.

```text
source_relation
→ visible_cue
→ reader_inference_or_action
→ transfer_condition
```

예를 들어 `과정 → 경로와 체크포인트 → 다음 단계와 완료 근거를 읽음 → 순서와 검증이 모두 필요한 장면에 사용`은 원리다. 반면 "왼쪽에 파란 원 세 개"는 표면 복제다.

전이는 두 곳에서 검증한다.

1. 현재 가장 약한 장면에 적용한다.
2. 관계가 다른 두 번째 장면에 원리를 변형 적용한다.

두 장면이 같은 레이아웃 복사본이 되면 원리 전이에 실패한 것이다. 두 번째 적용은 원리가 특정 슬라이드의 장식이 아니라 재사용 가능한 지원 규칙인지 확인하는 테스트다.

## 최소 5회 수렴 루프

이 패턴이 활성화되면 5회는 Fixed 최소값이다. 5회가 최대값은 아니다.

각 회차는 다음 순서로 닫는다.

1. 전체 장면의 현재 `support_floor`와 반복 실패를 다시 본다.
2. **현재** 가장 약한 장면 하나와 비교에 쓸 강한 장면 하나를 고른다.
3. 강한 장면에서 전이 가능한 지원 원리를 한 문장으로 추출한다.
4. 약한 장면을 다시 저작한다. 정보 정리, 관계 외현화, 행동·근거 cue, 읽기 경로를 먼저 고치고 스타일은 그다음 정한다.
5. 같은 원리를 다른 장면 하나에 변형 적용한다.
6. 필요한 부분만 source에서 다시 빌드하고 렌더한다.
7. Fixed audit로 의도한 객체 관계, bounds, overlap, spacing, connector, native coverage, hash/freshness를 확인한다.
8. Decision이 `pass_local / revise / blocked / needs_human_choice` 중 하나로 닫고, 다음 회차의 가장 약한 장면을 다시 고른다.

5회 뒤에도 다음 중 하나가 남으면 계속한다.

- 핵심 지원 축이 `absent`인 장면이 남아 있다.
- 같은 실패가 이미 만든 guard를 통과해 다시 나타났다.
- critical fixed blocker가 남아 있다.
- 원리 전이가 표면 복제에 머물렀다.

정지할 때는 "다섯 번 했음"이 아니라, `support_floor` 변화, 남은 blocker, 전이된 원리, 증거 표면을 함께 기록한다.

## 구현과 거리 계산의 역할

객체 간 거리·정렬·겹침 계산은 **의도를 정확한 위치에 구현하고 재현하는 수단**이다.

순서는 고정한다.

1. 사람/LLM이 의미 그룹, 필요한 분리·정렬·포함·연결 관계와 목표 간격을 선언한다.
2. 구현 코드가 PowerPoint native object 또는 다른 목표 매체 객체로 물질화한다.
3. 감사 코드가 실제 bbox와 관계를 선언값에 대조한다.
4. Decision이 render와 content-fit evidence를 함께 보고 다음 행동을 고른다.

모든 간격을 같게 만들거나, overlap 0을 좋은 디자인으로 간주하거나, geometry score를 improved-variant 판정으로 쓰지 않는다. 거리 계산이 발견한 실패는 source-level repair 대상으로 되돌리고, 재빌드 뒤 이전 render/native/open 증거는 stale 처리한다.

PowerPoint에서는 수정 가치가 큰 제목, 라벨, 표, 차트, 프로세스, 연결선, 콜아웃, notes, 읽기 순서를 의도적으로 native object로 만든다. 사진적 장면·복잡한 일러스트·질감은 image layer로 유지할 수 있으며, 그 위 의미 라벨과 행동 cue를 native layer로 올린다.

## 기준작의 역할

먼저 `source_role`을 고정한다.

- `fidelity_baseline`: faithful recreation이 목표이므로 source parity가 별도 Fixed gate다.
- `reference_benchmark`: 성공 원리와 약점을 관찰하는 Flexible evidence다. 1:1 유사도는 개선 gate가 아니다.

`reference_benchmark`에서 더 잘 만든다는 뜻은 현재 콘텐츠가 더 빨리 읽히고, 관계·행동·근거가 더 잘 보이며, 목표 매체에서 더 잘 설명·수정되고, 고장 없이 작동하는 것이다.

## 반복 실수 방지

각 회차에서 채택한 원리는 `pattern_guard`로 남긴다.

- 첫 발생: local hypothesis와 가장 작은 source repair를 기록한다.
- 비교 가능한 두 번째 발생: owner reference 또는 checklist를 강화하고 두 맥락에서 재검증한다.
- 강화된 written gate 뒤에도 재발: 생산 경계의 executable stop condition이나 validator fixture로 승격한다.

수정했다는 사실만 남기고 guard를 만들지 않으면, 다음 작업은 같은 실수를 새 문제처럼 다시 발견하게 된다.

## 회차 ledger

프로젝트는 다음 구조를 유지한다. 실제 장면 id, support 상태, threshold, 현재 수치는 프로젝트 SoT나 run log에 둔다.

```yaml
pattern: fixed-flexible-decision-visual-convergence
pattern_state: adaptive
minimum_cycles: 5
source_role: fidelity_baseline | reference_benchmark | no_original
cycles:
  - cycle_id: 1
    weak_scene_id: ""
    weak_support:
      relationship_support: clear | partial | absent | not_applicable
      priority_support: clear | partial | absent | not_applicable
      inference_or_action_support: clear | partial | absent | not_applicable
      evidence_or_completion_support: clear | partial | absent | not_applicable
      medium_support: clear | partial | absent | not_applicable
    strong_scene_id: ""
    transferable_principle:
      source_relation: ""
      visible_cue: ""
      reader_inference_or_action: ""
      transfer_condition: ""
    primary_transfer_scene: ""
    secondary_transfer_scene: ""
    flexible_choices:
      candidate_grammars: []
      selected_grammar: ""
      expression_system: ""
      medium_implementation: ""
    fixed_checks:
      source_rebuilt: false
      geometry_audit: not_run | pass | fail | not_applicable
      native_audit: not_run | pass | fail | not_applicable
      render_freshness: fresh | stale | not_applicable
      manual_open: not_run | pass | fail | not_applicable
    decision:
      status: pass_local | revise | blocked | needs_human_choice
      fixed_rule_applied: ""
      flexible_evidence_path: ""
      content_fit_reason: ""
      human_outcome_validation: not_run | pass | fail | blocked_by_human_input
      next_weak_scene_or_stop_reason: ""
    pattern_guard: ""
```

## 증거 표면과 완료 계약

다음 표면을 섞지 않는다.

- `content_fit_review`: 관계·우선순위·행동·근거가 잘 지원되는가.
- `fixed_implementation_audit`: source, schema, geometry, native, hash가 선언과 맞는가.
- `render_proof`: 실제로 보이는 결과가 깨지지 않았는가.
- `native_open_proof`: 목표 PowerPoint/Slides에서 복구 없이 열리고 의도한 객체가 편집되는가.
- `human_outcome_validation`: 실제 독자·학습자·협업자가 더 잘 이해·수행·수정했는가.

사람 검증 전에는 `content_fit candidate` 또는 `pass_local`까지만 닫는다. `human_outcome`으로 승격하지 않는다.

완료 보고는 최소 다음을 포함한다.

1. 수행 회차 수와 각 회차의 weak/strong scene.
2. 추출·전이한 원리와 secondary transfer 결과.
3. Fixed audit 결과와 stale proof 재검증 여부.
4. support floor의 변화와 남은 취약 장면.
5. human outcome 상태.
6. 새로 만든 pattern guard 또는 executable stop condition.

## 사용 맥락 실험

### 맥락 A — 교육용 슬라이드 덱

- 약한 장면: 개념과 실습 행동이 본문/표 안에 접혀 있음.
- 강한 장면: 과정과 체크포인트, 결과 근거가 경로로 보임.
- 전이 원리: `단계 + 행동 + 확인 근거`를 한 읽기 경로에 묶음.
- 구현: 제목·단계·체크포인트·연결선·노트는 PowerPoint native, 복잡한 현장 장면은 image base 가능.
- 판정: 학습성과가 아니라 semantic structure와 editability의 `pass_local`.

### 맥락 B — 운영 대시보드 또는 시각 문서

- 약한 장면: 상태 카드가 많지만 무엇을 판단하고 다음에 무엇을 해야 하는지 불분명함.
- 강한 장면: 이상 신호→판단 기준→조치→완료 증거가 한 흐름에 연결됨.
- 전이 원리: `상태 표시`를 `판단과 다음 행동을 닫는 경로`로 전환.
- 구현: 앱에서는 상태·필터·행동·오류를 semantic component로, 문서에서는 flow/table/callout로 구현.
- 판정: 운영 성과가 아니라 action path와 implementation consistency의 `pass_local`.

## 안티패턴

- 기준작과 1:1로 나란히 놓지 않았다는 이유만으로 improved 판정을 금지.
- Carbon 적용, native object 수, geometry pass를 시각화 개선으로 보고.
- 강한 장면의 색·카드·도형 배치를 그대로 복사.
- 가장 약한 한 장만 고친 뒤 다른 장면에 원리를 전이하지 않음.
- 다섯 회차를 같은 수정의 미세 조정으로 채움.
- 평균 실루엣을 맞추면서 의미 관계의 차이를 제거.
- 고친 실패를 pattern guard에 남기지 않아 다음 작업에서 반복.
- 렌더, native, content-fit, human outcome을 하나의 `done`으로 합침.

## Patternization Three-Layer Ledger

- **Fixed**: 이 reference의 적용 조건, 최소 5회, 회차 ledger 필드, 증거 표면 분리, geometry/quality 비승격, Rubric Must lock.
- **Flexible**: 대상 프로젝트 SoT, 장면 id, 약한/강한 장면, 지원 라벨, 시각 문법·표현 시스템·매체 구현, project tolerance, 실제 검증 로그.
- **Decision**: 기존 `visual-authoring`를 재사용하고 이 패턴을 `distill + validate`로 추가한다. Fixed 규칙은 `generate-skill`의 reuse-before-create와 three-layer ledger이며, Flexible evidence는 사용자 제공 작업 맥락과 현재 `visual-authoring` references다. 첫 cross-artifact 패턴화이므로 `adaptive`로 두고 다음 비교 가능한 맥락에서 재검증한다.

