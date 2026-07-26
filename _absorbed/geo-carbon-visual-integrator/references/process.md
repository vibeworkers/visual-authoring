# Process Log

## Step 1 — 문제 & 이론 앵커
- 막힘 문장: 페이지에 변수는 있지만 체계적 토큰 언어가 없어 섹션별 스타일이 분산된다.
- 이론 앵커 1: Carbon 의미론 토큰(색/간격/레이어)으로 스타일 의도를 고정한다.
- 이론 앵커 2: Evidence-first 시각 루브릭으로 미감 논쟁 대신 검증 가능한 판정을 사용한다.
- 확장 앵커: 생성 이미지는 물성/사람/공간/빛/흔적을 만들고, SVG/Carbon 레이어는 관계/경로/주의/라벨을 설명한다.
- 모델 앵커: ChatGPT Images 2.0은 키비주얼의 제품/능력 기준이며, API/CLI 실행에서는 `gpt-image-2`를 장면 base layer 기본값으로 사용한다. 의미 경로/추상 라벨/조건 게이트는 SVG/HTML에서 제어한다.
- 판독 앵커: 라벨을 숨긴 상태에서 의미 단위가 읽히지 않으면 시각화가 아니라 설명문 의존이다. 먼저 visible cue와 공간 배치를 고친다.
- 사례: GEO 강의 상세 페이지에서 `:root`는 있으나 spacing/typography/motion 계층이 약함.

## Step 2 — 용어 사전 & 컨셉맵
- glossary, concept-map 작성 완료.

## Step 3 — 프로토타입 & 실패 포착
- 실패 패턴 1: 새 섹션 추가 시 하드코딩 hex가 다시 유입됨.
- 실패 패턴 2: 데스크톱 기준만 맞고 모바일 위계가 흔들림.
- 실패 패턴 3: SVG 도식이 의미를 모두 설명하려 하면서 관객이 장면을 먼저 읽지 못함.
- 실패 패턴 4: 생성 이미지를 먼저 만들면 예쁘지만 핵심 메시지와 3초 판독이 흔들림.
- 실패 패턴 5: 이미지 prompt에 화살표와 개념 라벨까지 넣으면 편집 가능한 의미 layer가 사라지고 수정 비용이 커짐.
- 실패 패턴 6: 사물, 증거, 반복, 자기 확인을 라벨로만 구분하면 관객은 장면을 읽지 못하고 제작자의 해석문을 읽게 됨.
- 실패 대응: 신규 값은 `--cds-*`만 허용 + 모바일 캡처를 Must 검증에 포함.
- 실패 대응: `핵심 메시지 -> 시각 의미 단위표 -> 3초 판독 -> 심상 벤치마크 -> 장면 문법 -> 이미지 프롬프트 -> SVG 의미 레이어 -> label-masked/contact sheet 검증` 순서를 고정.
- 실패 대응: prompt ledger(model, prompt, output path, integration path, verification)를 남기고, 이미지 base와 SVG semantic layer를 별도 파일/레이어로 관리.
- 실패 대응: 라벨 가림 상태에서 key unit 3개 이상이 보이지 않으면 라벨 추가가 아니라 base scene visible cue를 재설계.

## Step 4 — 경계 설계
- Code: 규칙 위반 차단(하드코딩 신규 금지).
- LLM: 토큰 매핑 우선순위와 시각 계층 판단.

## Step 5 — 추출 & 루브릭
- SKILL.md + references 5종 구성.
- visual-semantic-encoding reference 추가.
- preflight 명령으로 구조 검증 예정.
