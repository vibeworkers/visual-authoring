# Rubric Design

## Must (결과물)
1. 필수 산출물 5종 존재
- Evidence: 파일 존재 검사 명령

2. 5단계 게이트 명시
- Evidence: Step/진입/탈출 키워드 검색

3. Code/LLM 경계 명시
- Evidence: 섹션 문자열 검색

4. preflight 로그 존재
- Evidence: 실행 명령 + 출력 요약

5. 이미지 base layer와 SVG semantic layer 분리
- Evidence: 산출물 또는 검증 로그에 `image base`, `SVG 의미 레이어`, `Carbon token` 역할 구분

6. 시각 의미 단위표와 라벨 가림 판독 기준 존재
- Evidence: 산출물 또는 검증 로그에 `meaning_unit`, `visible_cue`, `masked_read_criterion`, `라벨 가림` 기록

7. 생성 이미지 prompt ledger 존재
- Evidence: 생성 이미지를 쓴 경우 `model`, `prompt`, `output_path`, `integration_path`, `verification` 기록

## Should (과정)
1. 레거시 alias 전략 명시
2. 모바일/데스크톱 동시 검증
3. 다음 액션 1개로 종료
4. 텍스트 가림 또는 contact sheet 판독 검증
5. 라벨이 아니라 visible cue를 고치는 recovery action 기록
