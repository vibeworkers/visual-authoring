# Retrospective — Calmness Is Not Silhouette Repetition

## Context

2026-07-10 디지털 마케팅 3일 과정의 120장 PowerPoint는 시간표 충실도, native 편집성, 발표자 노트, 렌더, overflow, 실제 PowerPoint open, PDF 페이지 검증을 통과했다. 그러나 사용자 검토에서 시각화 종류가 제한적이라는 문제가 확인됐다.

## Observation

- 차분한 편집형 워크숍이라는 표현 방향은 유지됐다.
- 외부 이미지와 근거 없는 데이터를 넣지 않는 경계도 유지됐다.
- 그러나 제목+넓은 여백, 2단 구성, 표·목록, 색상 면이 붙은 실습 지시가 과도하게 반복됐다.
- 색상은 세션별로 달랐지만 공간 관계와 읽기 경로는 충분히 달라지지 않았다.

## Root Cause

`차분함`, `편집 가능성`, `일관성`을 잘못 결합해 표현 강도뿐 아니라 의미 구조의 다양성까지 축소했다. 외부 이미지가 없다는 조건을 비교·과정·클러스터·지도·해부·스토리보드 같은 native 의미 시각화까지 줄이는 근거로 사용했다. 렌더와 네이티브 검증은 통과했지만, 이 검증들은 실루엣 다양성을 측정하지 않았다.

## Learning

- 차분함은 낮은 채도·절제된 질감·모션·장식을 뜻한다. 관계 구조의 획일화를 뜻하지 않는다.
- 시각 다양성은 색·아이콘·shape 수가 아니라 읽기 경로와 공간 관계의 차이로 판정한다.
- 편집 가능성이 높은 native object는 의미 기반 다이어그램을 피하는 이유가 아니라 구현 수단이다.
- 긴 덱은 전체 확장 전에 관계 유형과 실루엣 가족의 분포를 선언하고 검사해야 한다.

## Carry-Forward Rule

장형/다섹션 시각 산출물은 `visual-silhouette-manifest.json`을 작성하고, 프로젝트가 선언한 가족 수·연속 반복·지배 비율·의미 시각화 목표를 validator로 확인한다. 표현군 prototype은 실제 실루엣 가족을 대표해야 한다. rebuild 후 이전 분포·렌더·native-open 증거는 stale이다.

## Pattern Repetition Counter

이름: `calmness_to_silhouette_collapse`

현재 반복 수: `N=1`

판정: 현재는 한 프로젝트에서 명시적으로 포착된 가설이다. 따라서 전역 고정 수치를 만들지 않고, 프로젝트별 policy를 선언하게 하는 실행형 게이트만 추가한다. 다른 독립 프로젝트에서 같은 실패가 반복되면 N=2 격상 신호로 재검토한다.

## Three-Layer Ledger

| Layer | Record |
|---|---|
| Fixed | relationship/silhouette 분리, manifest 필수 필드, 선언값 validator, 색·장식 변형을 별도 가족으로 세지 않음 |
| Flexible | 프로젝트별 가족 수, 연속 허용치, 지배 비율, 의미 시각화 목표, 워크시트 예외 |
| Decisional | 어떤 관계를 어떤 실루엣으로 바꿀지, 반복이 학습상 유익한지, 수정 우선순위 |
