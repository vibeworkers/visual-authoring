---
name: geo-carbon-visual-integrator
description: >
  GEO 홍보 페이지와 시각 문서에 의도된 시각 시스템을 일관되게 적용하기 위한 통합 스킬.
  Carbon 토큰 매핑, 시각 의미 단위표, 장면 심상 벤치마크, 생성 이미지 통합, SVG 의미 레이어,
  label-masked evidence-first 시각 검증을 하나의 루프로 실행한다.
  "카본 토큰으로 정리", "시각 시스템 통합", "의도된 비주얼로 리팩터링", "이미지 생성과 SVG 통합" 요청에서 사용한다.
---

# geo-carbon-visual-integrator

GEO 홍보용 HTML/CSS와 시각 문서를 Carbon 토큰 중심 체계로 정규화하고,
시각 판단을 취향이 아닌 증거를 보고 닫는 통합 스킬.
이미지 생성 모델은 장면 base layer, SVG/HTML은 의미 layer, Carbon token은 시스템 layer로 분리한다.

## External SoT

The visual semantic encoding gate is defined in `references/visual-semantic-encoding.md`.
Global skill routing is defined in `../generate-skill/references/global-skill-management.md`.
This skill body is a process snapshot as of 2026-05-05; project protocols may set stricter local criteria.

## Goal

하드코딩 스타일을 Carbon 의미론 토큰으로 통합하고,
장면 기반 키비주얼과 SVG 의미 레이어가 분리된 상태로 첫 화면 의도 전달력과 시각 일관성을 PASS 가능하게 만든다.

## 적용 대상 (Trigger)

- "의도된 시각 시스템"을 만들거나 정리해야 할 때
- 기존 CSS가 변수 일부만 쓰고 있어 체계가 무너질 때
- Carbon 디자인 언어(토큰, grid, tile)를 기존 랜딩에 반영할 때
- 시각 품질을 근거 기반(PASS/CONDITIONAL/FAIL)으로 검증해야 할 때
- 생성 이미지가 배경/키비주얼을 맡고 SVG/HTML이 의미 구조를 얹어야 할 때
- 슬라이드/페이지가 3초 안에 무엇으로 읽히는지 흔들릴 때

## Inputs

- 대상 파일 경로(HTML/CSS)
- 페이지 목적(예: 강의 전환, 신청 유도, 신뢰 형성)
- 우선 디바이스(Desktop 우선/모바일 동등)
- 브랜드 제약(색상, 폰트, 금지 요소)
- 핵심 메시지와 3초 판독 문장
- 시각 의미 단위표(meaning unit, visible cue, masked read criterion, risk, recovery action)
- 이미지 생성 프롬프트 또는 생성 이미지 경로(있는 경우)
- prompt ledger(model, prompt, output path, integration path, 3초 판독 검증 경로)

## 수행 흐름 (5단계, 게이트 포함)

### Step 1) 문제 포착 & 이론 앵커
- 진입 조건: 대상 파일 + 페이지 목적이 명시됨.
- 작업:
  - 현재 스타일의 병목을 문장 1개로 고정한다.
  - 이론 앵커 2개로 설명한다.
  - Carbon 토큰화 근거와 시각 루브릭 근거를 연결한다.
  - 이미지 생성이 필요한 경우, 생성 모델이 맡을 장면 물성과 SVG/Carbon이 맡을 의미 구조를 먼저 분리한다.
- 탈출 조건:
  - 막힘 문장 1개 + 이론 근거 2개 + 사례 1개가 문서화됨.

### Step 2) 용어 사전 & 컨셉맵
- 진입 조건: Step 1 산출물 존재.
- 작업:
  - 용어 5개 이상을 스킬 맥락 정의로 확정한다.
  - 문제→토큰→레이아웃→검증 흐름을 경로로 맵핑한다.
  - 키비주얼 작업이면 `시각 의미 단위표 -> 3초 판독 -> 심상 벤치마크 -> 장면 문법 -> 이미지 생성 -> SVG 의미 레이어 -> Carbon 통합` 경로를 추가한다.
  - `references/visual-semantic-encoding.md` 기준으로 meaning unit, visible cue, masked read criterion, risk, recovery action을 채운다.
- 탈출 조건:
  - `references/glossary.md`, `references/concept-map.md` 생성 완료.

### Step 3) 프로토타입 & 실패 포착
- 진입 조건: Step 2 통과.
- 작업:
  - 최소 변경으로 토큰 치환 프로토타입을 만든다.
  - 키비주얼이 필요하면 이미지 생성 전에 시각 의미 단위표를 먼저 만들고, 라벨을 가린 상태에서 무엇이 보여야 하는지 고정한다.
  - 키비주얼이 필요하면 생성 이미지는 사람/공간/사물/빛/흔적을 담당하고, SVG는 관계/경로/주의/라벨만 담당하도록 분리한다.
  - ChatGPT Images 2.0 계열을 쓰는 경우 prompt ledger에 product anchor, API/CLI model, prompt, output path, integration path, verification을 기록한다.
  - 반복 실패 패턴을 2개 이상 수집한다.
- 탈출 조건:
  - 실패 패턴 2개 이상과 대응안이 기록됨.

### Step 4) 경계 설계 (Code/LLM + 게이트)
- 진입 조건: Step 3 통과.
- 작업:
  - Code 강제 항목과 LLM 판단 항목을 분리한다.
  - 각 원칙에 "하지 않는다" + "대체한다"를 함께 적는다.
- 탈출 조건:
  - 경계 규칙 표가 존재하고 예외가 명시됨.

### Step 5) 스킬 추출 & 루브릭
- 진입 조건: Step 4 통과.
- 작업:
  - 최종 `SKILL.md`와 references를 정리한다.
  - Must/Should 루브릭 + Evidence 방법을 포함한다.
  - 1회 preflight 테스트 명령 결과를 남긴다.
- 탈출 조건:
  - 필수 산출물 5개 + 검증 로그 1개 존재.

## 실행 프로토콜 (R->P->M->W->A)

- `R` Research: 기존 CSS 변수/하드코딩 분포 조사 (`rg ':root|var\(|#|px'`).
- `P` Plan: 섹션별 치환 우선순위와 영향 범위 확정. 키비주얼은 핵심 메시지, 시각 의미 단위표, 3초 판독, 일반 심상, 장면 문법, SVG 의미 레이어를 먼저 고정한다.
- `M` Make: 최소 변경 단위로 토큰 치환 + 레거시 alias 유지. 필요한 경우 `imagegen` 스킬로 생성 이미지를 만들고 HTML/SVG/Carbon에 통합한다.
- `W` Verify: 스크린샷/DOM/CSS 근거, label-masked 3초 판독, contact sheet 기준으로 PASS/CONDITIONAL/FAIL 판정.
- `A` Archive: 적용 결과와 실패 패턴을 기록하고 다음 액션 1개 닫기.

## Code / LLM Boundary (Code / LLM 경계)

### Code가 강제하는 것 (예외 없음)
- 하드코딩 색상/간격/반경 신규 추가 금지.
- 토큰은 `--cds-*` 우선, 기존 변수는 alias로만 유지.
- 이미지/SVG 혼합 작업에서 심리·인지 해석은 관찰 지표와 분리해 `hypothesis`, `interpretation`, `caution` 등으로 표시.
- 이미지 생성 결과에 의미 경로/추상 라벨/조건 게이트를 맡기지 않는다. 해당 요소는 SVG/HTML layer에서 제어한다.
- 라벨을 가린 상태에서 핵심 의미 단위가 읽히지 않으면 완료 선언 금지. 더 많은 라벨을 추가하지 말고 visible cue 또는 장면 배치를 고친다.
- ChatGPT Images 2.0 / `gpt-image-2` 또는 snapshot을 쓴 경우 prompt ledger를 남기고, 투명 배경이 필요한 경우 모델 지원 여부를 별도 확인한다.
- Must 항목 미충족이면 완료 선언 금지.

### LLM이 판단하는 것 (유연)
- 어떤 색/간격 토큰을 어떤 컴포넌트에 매핑할지
- 시각 계층(히어로/본문/보조) 우선순위
- 어떤 장면 심상이 3초 판독에 가장 강한지
- 이미지 생성 모델을 쓸지, 고밀도 SVG만으로 충분한지
- Conditional 판정의 보완 우선순위

## 금지 패턴 -> 대체 규칙

- 하지 않는다: 섹션마다 임의 색상 추가
- 대체한다: `--cds-background-*`, `--cds-text-*`에서 선택

- 하지 않는다: 카드별 임의 border-radius 혼용
- 대체한다: `--cds-radius-02/03/04` 중 목적별 고정

- 하지 않는다: 시각 평가는 감상 위주 코멘트로 종료
- 대체한다: 캡처 경로/DOM 근거 포함 PASS/CONDITIONAL/FAIL로 종료

- 하지 않는다: 생성 이미지가 스토리와 해석을 임의로 대신 만들게 둔다
- 대체한다: 핵심 메시지와 3초 판독을 먼저 고정하고, 이미지는 물성/장면, SVG는 관계/경로/주의를 담당하게 한다

- 하지 않는다: 이미지 생성 prompt에 화살표, 조건 게이트, 추상 설명 라벨까지 넣어 의미를 모델 출력에 고정한다
- 대체한다: 이미지에는 보이는 사물과 장면만 요청하고, 의미 경로는 SVG/HTML에서 편집 가능하게 얹는다

- 하지 않는다: 식별되지 않는 사물이나 자기 확인 지점을 라벨만으로 보정한다
- 대체한다: 라벨을 숨겨도 보이는 visible cue, 공간 배치, 반사/프로필/손짓 같은 자기 지시 단서를 먼저 강화한다

## Rubric (Must/Should)

### Must
- 필수 산출물 5개가 모두 존재한다.
  - Evidence: `test -f`로 파일 존재 검증.
- Step 1~5 게이트 조건이 SKILL 문서에 명시된다.
  - Evidence: `rg 'Step 1|Step 2|Step 3|Step 4|Step 5|진입 조건|탈출 조건'`.
- Code/LLM 경계와 금지->대체 규칙이 포함된다.
  - Evidence: 해당 섹션 문자열 검색.
- preflight 검증 1회 결과가 기록된다.
  - Evidence: 명령/출력 요약 로그.
- 키비주얼/슬라이드 요청에서 장면 심상과 SVG 의미 레이어 역할이 분리된다.
  - Evidence: `핵심 메시지|3초 판독|심상 벤치마크|장면 문법|SVG 의미 레이어` 항목이 산출물 또는 검증 로그에 존재한다.
- 키비주얼/슬라이드 요청에서 시각 의미 단위표와 label-masked 판독 기준이 존재한다.
  - Evidence: `시각 의미 단위표|meaning_unit|visible_cue|masked_read_criterion|라벨 가림` 항목이 산출물 또는 검증 로그에 존재한다.
- 생성 이미지를 쓴 경우 prompt ledger가 남는다.
  - Evidence: `model|prompt|output_path|integration_path|verification` 항목이 산출물 또는 검증 로그에 존재한다.

### Should
- 토큰 alias 정책이 레거시 호환성까지 설명된다.
- 모바일/데스크톱 둘 다 판정 근거가 남는다.
- 다음 액션이 한 줄로 명확히 닫힌다.
- 생성 이미지를 쓴 경우 원본 프롬프트, 모델, 출력 경로, 통합 경로가 남는다.
- 생성 이미지/SVG 통합 산출물은 라벨 가림 상태에서 key unit 3개 이상이 식별된다.

## Preflight 체크

```bash
# 1) 필수 파일 존재
ls -la skills/geo-carbon-visual-integrator
ls -la skills/geo-carbon-visual-integrator/references

# 2) 게이트/루브릭 구조 검증
rg -n "Step 1|Step 2|Step 3|Step 4|Step 5|Rubric|Must|Should|Code / LLM 경계" skills/geo-carbon-visual-integrator/SKILL.md

# 3) 참고 문서 연결 확인
rg -n "glossary|concept-map|process|rubric-design|gate-conditions" skills/geo-carbon-visual-integrator/SKILL.md skills/geo-carbon-visual-integrator/references/*.md
```

## References

- `references/process.md`
- `references/glossary.md`
- `references/concept-map.md`
- `references/gate-conditions.md`
- `references/rubric-design.md`
- `references/visual-semantic-encoding.md`

## AGENTS.md Alignment

- Goal-First: 목표는 검증 가능한 완료 조건으로 고정한다.
- Rubric-Driven: Must 100% 전까지 종료하지 않는다.
- Completion Rule: 차단 시 원인/우회안을 함께 남긴다.
