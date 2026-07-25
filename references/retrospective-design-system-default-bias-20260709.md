# Retrospective — Design-System Default Bias / Scene Specificity / Native PPTX

## Context

LinkageLab 운영팀 스터디 교재·슬라이드 제작 중 다음 피드백이 반복됐다:

- 디자인이 별로이고 자유도가 사라짐.
- 시각화가 획일적이고 장면을 정확히 전달하지 못함.
- PPTX가 제공하는 정식 기능을 쓰지 않고 이미지/렌더 중심으로 닫히는 느낌.
- 생성 이미지를 그대로 옮기되, PPTX의 편집 가능한 기능도 같이 써야 함.

## Root Cause

1. Phase 3가 Carbon/Vivid를 사실상 기본 선택축으로 다뤘다.
2. 생성 이미지가 필요한 장면에서 구체 인물·공간·사물·행동을 잠그는 게이트가 약했다.
3. PPTX를 최종 렌더 증거 중심으로 확인하고, master/layout/notes/editable object 같은 네이티브 기능 점검이 늦었다.
4. 회고 신호가 다음 산출물 게이트로 다시 들어가는 규칙이 약했다.

## Remediation

- `SKILL.md`: Phase 3를 `Visual Strategy & System Select`로 바꾸고, Carbon/Vivid를 후보로만 둔다.
- `references/design-systems.md`: 기본값 표를 제거하고, 후보 3개 이상 탐색·선택/거절 근거·no-default 기록을 요구한다.
- `references/review-gate.md`: `Scene Specificity Gate`를 추가해 generic image background를 차단한다.
- `references/slide-authoring.md`: `Native Medium Capability Scan`을 추가해 PPTX 편집성·발표성·협업성을 별도 증거로 본다.
- `references/checklist.md`: `Design Exploration Gate`, `Scene Specificity Gate`, `Retrospective Signal Gate`, Mode S native checks를 출고 항목으로 추가한다.

## Carry-Forward Rule

다음 `visual-authoring` 실행부터는 아래 4개가 없으면 완료로 닫지 않는다:

1. `visual_strategy` + 후보 3개 이상 + 선택/거절 근거.
2. 이미지 경로면 `Scene Specificity Gate` packet.
3. PPTX 경로면 `Native Medium Capability Scan` packet.
4. 반복 피드백 신호의 분류(`default_bias`, `scene_generic`, `native_feature_gap`, `readability_gap`, `other`)와 다음 수정 게이트 연결.
