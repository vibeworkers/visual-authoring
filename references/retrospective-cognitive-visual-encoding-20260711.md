# Retrospective — Cognitive Visual Encoding (2026-07-11)

## Goal

장형 강의 덱에서 시각적 다양성이 단순한 레이아웃 교체가 되지 않도록, 콘텐츠 관계와 독자 추론 목표가 시각 문법 선택을 이끌게 한다.

## Exact failure signal

- 기존 게이트는 실루엣 가족 수·반복·지배 비율을 검사했지만, 선택한 실루엣이 실제 관계와 추론에 적합한지는 기록하지 않았다.
- `차분함`을 낮은 표현 강도로 해석하는 규칙은 생겼으나, 어떤 cue를 보여주고 억제했는지와 읽기 경로가 한 패킷으로 남지 않았다.
- 계산 가능한 proxy와 실제 사람의 이해·몰입·학습성과 사이 경계가 제작 manifest에 직접 연결되지 않았다.

## Learning

다양성은 필요조건이지 의미 적합성의 증거가 아니다. 시각 판단은 다음 순서를 보존해야 한다.

1. source claim과 reader task
2. relationship type과 inference goal
3. materially different candidate visual grammars
4. selected grammar와 selection reason
5. visible/suppressed cues와 reading path
6. evidence state, claim boundary, human-validation boundary

`vector-language-cognition`은 evidence state와 인지 proxy/사람 검증 경계를 소유한다. `visual-authoring`은 이를 소비하며, 새로운 metric이나 enum을 임의로 만들지 않는다.

## Implemented gate

- 신규/전면 재구성 장형 덱: `visual-silhouette-manifest.json` schema v2 필수
- legacy schema v1: 과거 감사만 허용, 새 전체 확장 승인에는 사용 금지
- validator: 선택 문법이 후보 안에 있는지, 필수 cue/경로/근거가 있는지, 사람 outcome pass가 실제 `human_outcome` evidence와 일치하는지 검사
- 사람 실측 전: 이해·몰입·학습성과는 inferred/calibrated proxy로만 보고

## Routing examples

- `차분한 120장 강의 덱`: 표현 강도는 낮추되 comparison/process/decision/practice 관계별 문법 후보를 유지하고 schema v2를 요구한다.
- `한 화면 운영 대시보드`: 실제 관계가 상태 비교와 이상 탐지에 집중되어 있다면 많은 실루엣 가족을 억지로 만들지 않는다. 대신 선택 문법과 cue의 관계 적합성, evidence boundary를 기록한다.

## Evidence status

이 패치는 규칙·schema·검증기 수준의 구현 증거다. 실제 학습자의 이해·기억·행동 개선은 아직 사람 검증 전이며 `human_outcome`으로 주장하지 않는다.
