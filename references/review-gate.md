# Review Gate — Phase 2 상세

시각 관련 요청을 제작 전에 잡는 리뷰 게이트. (원형: `universal-visual-vlc` — 전문 스냅샷 `../_absorbed/universal-visual-vlc/`)

## 로드 맵

| 필요한 것 | 파일 |
|---|---|
| review packet 필드 정의(언어 단위, 목표, 맥락, scene-first packet, target profile, human-outcome boundary), 결정 라벨 4종 | `review-packet.md` |
| route_status 판정 절차(image-required route gate), SVG↔이미지 경계 기준 | `image-required-route-gate.md` |

## 핵심 계약 (요약)

### claim 3분리
- `observable_proxy` — 이 게이트가 직접 측정한 것 (구조, 카운트, 판독 등)
- `inferred_risk` — 측정에서 추론한 위험
- `human_outcome_claim` — 사람 이해·설득·몰입·전이·학습성과. **이 게이트만으로 통과 불가, 별도 실측 필요**

### route_status enum
| 값 | 의미 | 종료 가능? |
|---|---|---|
| `SVG_ALLOWED` | 구조·추상·데이터 우선 → 결정적 SVG/HTML/토큰이 주 비주얼 | 정상 진행 |
| `ROUTED_IMAGE_REQUIRED` | 구체 장면·사진·일러스트 base 필요 → 이미지 생성 라우팅 | 정상 진행 |
| `INTEGRATED_HYBRID` | 이미지 base가 장면 기억을 소유하고, 결정적 의미 레이어가 정확한 라벨·관계·순서를 소유 | 정상 진행 |
| `SVG_PROXY_ONLY` | 이미지가 필요한데 SVG 대용만 있음 | **실패 종료 — `Done`/`*_pass` 금지** |
| `BLOCKED_IMAGEGEN` | 이미지 경로 차단됨 | **실패 종료 — `Done`/`*_pass` 금지** |

### 결정 라벨
`usable` / `candidate` / `blocked` / `hypothesis only`.
외부 증거 없이 `human_pass`, `high_quality_slide_pass`, `cinematic_pass` 보고 금지.

## 실행 라우팅 (owner 경계)

| 대상 | Owner |
|---|---|
| 이미지 생성 | `imagegen` |
| 슬라이드/PPTX 파일 빌드 | `slides` / `hybrid-slide-pipeline` / `hybrid-deck-factory` |
| 문서/PDF/HTML 포맷 변환 | `carbon-doc` / `doc-converter` / `pdf` |
| 핵심 VLP metric/schema/validator | `vector-language-cognition` |

본 스킬은 이들을 조율만 하고 소유하지 않는다.

## Scene-Centered Meaning Gate (모든 경로)

`SVG_ALLOWED`를 포함한 모든 정상 경로는 구현 전에 `review-packet.md`의 확장된 `scene_first_judgement_packet`을 닫는다. 장면은 사진적 공간만 뜻하지 않는다.

- `concrete_world`: 사람·공간·사물과 실제 행동
- `operational_state`: 현재 상태, 판단, 조치, 완료 근거의 변화
- `abstract_relationship`: 비교·과정·인과·계층·클러스터·판단 관계

각 주요 의미 단위는 한 장면·한 독자 추론/행동을 우선하고, 인식 가능한 entity/anchor, action 또는 state change, 3초 core read, non-label visible cue, semantic boundary, 정확 문구·수치의 deterministic owner, artifact-level design-system lock 참조, 열린 materiality 후보와 선택 이유를 기록한다. scene-centered는 반복 레이아웃을 뜻하지 않으며, open materiality는 이미지를 강제하지 않는다.

라벨을 가릴 때 검사하는 것은 관계·상태 변화·행동이다. 정확한 한국어, 수치, 조건, 근거 라벨은 deterministic meaning layer에서 읽혀야 하며 이미지에 추측을 맡기지 않는다.

## Scene Specificity Gate

`ROUTED_IMAGE_REQUIRED` 또는 `INTEGRATED_HYBRID`가 나오면 이미지 생성 전 아래를 통과해야 한다.
추상 배경·그라디언트·일반 분위기 이미지만으로는 통과하지 않는다.

| 필드 | 닫는 것 |
|---|---|
| `scene_subject` | 누가/무엇이 중심인지. 프로젝트와 무관한 generic object 금지 |
| `place` | 어디인지. 사무실/카페/워크샵룸/운영센터처럼 구체 공간 |
| `objects` | 반드시 보여야 할 도구·문서·화면·물건 |
| `action` | 그 장면에서 일어나는 동작. 정지된 무드가 아니라 변화의 순간 |
| `viewpoint` | 카메라/독자 관점. 왜 이 각도에서 이해되는지 |
| `text_policy` | 이미지 안 텍스트·로고·세부 UI는 맡기지 않음. 의미 레이어가 소유 |
| `negative_prompt` | 읽기 어려운 텍스트, 가짜 로고, 손상된 UI, 과도한 blur/crop 방지 |
| `could_apply_to_any_project` | `false`여야 함. true면 scene brief를 다시 작성 |
| `integration_plan` | 이미지 base와 SVG/HTML/PPTX 의미 레이어의 역할 분리 |
| `proof_surface` | thumbnail/render path 또는 생성 차단 사유 |

`INTEGRATED_HYBRID`는 "이미지를 깔고 그 위에 글자를 올린다"가 아니다. 이미지 base는 기억할 수 있는 장면을,
의미 레이어는 정확한 라벨·관계·순서·검증 가능한 문장을 소유해야 한다.

## 선택형 VLC 어댑터 (있을 때만)

프로젝트가 `surface_vlc_gate` 또는 `run_surface_delivery_gate` 호환 CLI를 제공하면, project config에 상대 경로나 명령을 기록해 연결한다. 이 패키지는 특정 컴퓨터나 workspace의 절대 경로를 호출하지 않는다.

CLI가 없거나 실패하면 **점수를 날조하지 않는다** — 구조화 packet(위 필드)을 수기로 반환하고 게이트 상태를 `blocked`로 남긴다.

## Phase 2 탈출 게이트 (요약)

1. route_status 결정됨 (enum 5값 중 하나)
2. claim 3분리 명시 (`observable_proxy` / `inferred_risk` / `human_outcome_claim`)
3. 결정 라벨 부여 (`usable`/`candidate`/`blocked`/`hypothesis only`)
4. 실패 종료 상태(`SVG_PROXY_ONLY`/`BLOCKED_IMAGEGEN`)면 다음 Phase 진입 금지
5. 모든 정상 경로에서 Scene-Centered Meaning Gate와 artifact-level design-system lock 참조 통과 또는 `blocked`
6. 이미지 경로(`ROUTED_IMAGE_REQUIRED`/`INTEGRATED_HYBRID`)면 추가로 Scene Specificity Gate 통과 또는 `blocked`
