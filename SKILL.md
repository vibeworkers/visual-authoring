---
name: visual-authoring
description: >
  시각 저작(Visual Authoring) 통합 정본 스킬. 인지적 문서/슬라이드 저작, 외부 자산 흡수 집필(GGACA),
  원본 기반 재생성/이관, 원본 해체→보존/전이/폐기→source parity 대조, 제작 전 시각 리뷰 게이트,
  콘텐츠 적합성을 우선하는 시각 전략, 산출물 단위로 고정한 디자인 시스템과 장면별 열린 시각 재료,
  선택형 표현 시스템(Carbon/Vivid/Brand/Custom 등), 정확 문구·수치의 결정적 의미 레이어,
  번역·구체화 뒤 재배치와 증거 갱신,
  매체 구현을 분리한 랜딩/앱UI/슬라이드/시각문서·교재·워크북·배포 PDF 제작, scene-base/meaning/system/materialization
  레이어 분리, 계산 가능한 배치 검증, 의도적인 PowerPoint native object 및 릴리즈 게이트를 하나의
  6단계 파이프라인으로 실행한다. 복구 이력이 있는 PPTX를 생성 기반으로 쓰지 않고, Fixed 패턴 컴파일러와
  Flexible LLM 저작, 분리된 구조·읽기·보기·native-runtime 증거 장부로 새 후보 계열을 만든다.
  트리거 — "시각화", "장표/슬라이드/PPTX", "랜딩/홍보/marketing page", "대시보드/앱UI/폼/모달",
  "카본 토큰으로 정리", "vivid하게/시네마틱", "의도된 시각 시스템", "여러 저자 자산을 한 권으로 흡수",
  "이미지 생성과 SVG 통합", "디자인 시스템은 고정하되 장면마다 자유롭게", "장면 중심으로 의미를 강화",
  "LLM이 이미지로 만들 수 있는 모든 표현을 후보로", "한눈에 이해되는가", "고품질 slide인가".
  document-slide-authoring-agent-system
  + ggaca-authoring + universal-visual-vlc + visual-implementation + geo-carbon-visual-integrator를
  하나로 병합한 정본이며, 이 5개 이름은 본 스킬로 라우팅한다.
metadata:
  display-name: Visual Authoring
  short-description: Fixed-system, scene-centered visuals with proof-safe reflow
  cogarch-role: visual-authoring-canonical
  runtime-compatibility: runtime-delta implemented
  source-kind: merged canonical skill
---

# visual-authoring

**한 문장 정의**: 무엇을 왜 보여줄지 고정하고(Author), 제작 전에 콘텐츠·독자·행동에 맞는 시각 표현인지 판정하고(Review Gate), 시각 전략과 선택형 표현 시스템을 매체 구현과 분리해 정한 뒤(Visual Strategy & Expression Select), 계산 가능한 구조와 의도적인 native object로 만들고(Implement), 콘텐츠 적합성·렌더·네이티브·사람 증거를 분리해 닫는(Verify/Release) 단일 시각 저작 파이프라인.

이 스킬은 5개 스킬을 흡수한 정본이다:

| 흡수 소스 | 파이프라인 위치 |
|---|---|
| `ggaca-authoring` | Phase 0 — Absorb (외부 자산 다수 흡수 집필) |
| `document-slide-authoring-agent-system` | Phase 1 — Author (인지적 저작·순서·PPTX 게이트) |
| `universal-visual-vlc` | Phase 2 — Review Gate (제작 전 시각 판정) |
| (신규 요구) | Phase 3 — Visual Strategy & Expression Select (콘텐츠 전략 우선, Carbon/Vivid/Brand/Custom은 선택형 도구) |
| `visual-implementation` + `geo-carbon-visual-integrator` | Phase 4 — Implement (토큰·레이어 빌드) |
| (5개 공통) | Phase 5 — Verify & Release (근거·5초·PPTX open) |

---

## Trigger Contract

### should-trigger
- "시각화", "visualization", "인포그래픽", "다이어그램", "키비주얼", "visual storytelling"
- "장표", "slide", "PPTX", "PDF 장표", "슬라이드 만들어", "교육 자료/제안서 시각화"
- "랜딩", "홍보", "marketing page", "promo", "강의 상세", "모집/제품 상세", "영화처럼 몰입", "시네마틱"
- "대시보드", "앱 UI", "admin/운영 도구", "폼", "모달", "인스펙터", "데이터 테이블 화면"
- "카본 토큰으로 정리", "의도된 시각 시스템", "vivid하게", "생성 이미지와 SVG 통합"
- "디자인 시스템은 고정하되 장면마다 자유롭게", "장면 중심으로 의미를 강화", "LLM이 이미지로 만들 수 있는 모든 표현을 후보로"
- 기존 시각 산출물의 문구를 번역·자연화·구체화하고 레이아웃·렌더·접근성·배포 증거까지 다시 검증해야 할 때
- "교과서", "워크북", "전자책", "독자용 표지", "배포 PDF", "목차에서 해당 위치로 이동", "공개 자료에서 내부 제작/검증 문구를 숨겨줘"
- "여러 저자/논문/코퍼스를 한 권으로 묶어 집필", "외부 자산을 내 어휘로 흡수"
- "특정 작가의 기존 글 호흡이나 에세이 문법을 읽고 웹·문서의 읽기 흐름으로 옮겨줘", "해경 브런치 글의 문법을 디자인에 반영해줘"
- "원본을 기준으로 다시 생성", "기존 PPTX/이미지/HTML을 그대로 구현", "네이티브 객체로 바꿔가기", "원본 대조", "source parity"
- "한눈에 이해되는가", "상징이 불명확", "고품질 slide인가", "3초 안에 읽히는가"
- 기존 시각 산출물을 릴리즈·반복 전에 검토해야 할 때

### should-not-trigger (다른 owner로 라우팅)
- 문서 파일 내보내기(PPTX/DOCX/HWPX 자체 포맷 생성·변환만) → `carbon-doc`, `doc-converter`, `slides`, `pdf`
- 순수 이미지 생성만, 품질·이해·릴리즈 주장 없음 → `imagegen` (본 스킬은 lightweight preflight만)
- 핵심 VLP metric/schema/validator 변경 → `vector-language-cognition`
- 한국어 문장 자연화만 → `korean`
- 컨셉맵 단독 제작 → `concept-map-creator` (병합 제외 대상)
- 단일 저자 단일 짧은 글 신규 집필(흡수 없음) → 일반 응답 또는 writer 계열
- 브런치 플랫폼의 화면·편집기·로고를 그대로 복제해줘 → 플랫폼 UI 재현 요청으로 분리한다. 이 스킬의 코퍼스 문법 모듈은 글의 흐름을 관찰해 대상 매체에 이식하며, 브런치 UI fidelity를 약속하지 않는다.

### near-miss 경계
- "이 슬라이드 문구만 한 줄 고쳐줘" → 본 스킬 아님(단발 편집).
- "이 문장만 한국어로 번역해줘" → `korean`; 단, 번역문을 기존 시각 산출물에 반영하고 재배치·재렌더해야 하면 본 스킬과 함께 사용.
- "PPTX 파일로 저장만" → 포맷 owner로 route, 저작·시각판단 없음.
- "이미지 1장만 뽑아줘" → `imagegen`, 단 "슬라이드에 쓸 이해되는 키비주얼"이면 본 스킬 Review Gate 통과.

---

## Working Source of Truth and Clarification Intake

저작·시각 계획·구현 전에 현재 working source of truth를 고정한다. 사용자가 노트·파일·경로·URL을 줬다면 그것을 정본으로 잠그고 generic 가정으로 다시 시작하지 않는다. 다음을 명명한다:

- `goal`
- `scope` / `excluded_surfaces`
- `working_source_of_truth`
- `success_condition`
- `evidence_target`
- `runtime_target` (선택)
- `provider_provenance` (선택)
- `output_brand` (선택)
- `original_source_inventory` (원본 artifact가 있을 때 필수)
- `source_decomposition` (원본 장면·정보·시각·네이티브 기능 해체)
- `preserve_transfer_discard_decisions` (보존/전이/폐기 판단)
- `source_role` (`fidelity_baseline`인지 `reference_benchmark`인지 명시)
- `source_parity_evidence` (faithful recreation/transfer가 목표일 때만 필수)
- `audience_surface_policy` (독자 공개 / 진행자·편집자 / 제작·검증 표면의 언어·노출 경계)
- `artifact_role_map` (예: 본권, 워크북, 부록이 맡는 지식·행동·증거의 역할)
- `format_standard_profile` (배포 포맷별 적용 기능, 검증 방법, 인증 주장 상태)

빠진 항목은 generic 추정으로 메우지 말고 `TODO / question / uncertain / blocked`로 표시한 뒤, 검증된 범위 안에서만 진행한다. 한 번의 묶음 질문으로 닫을 수 있으면 짧게 묻는다. 하위 Phase는 이 clarification packet을 상속하며 임의로 재개봉하지 않는다.

## User Decision, Comparative Preview, and Progress Gate

이 스킬은 사용자가 결정해야 하는 내용을 추측으로 닫지 않는다. 모든 응답은 현재 위치를 **Step by Step**으로 보이며, 각 단계가 끝날 때 다음 단계와 필요한 사용자 결정만 한 묶음으로 제시한다.

```text
진행 상황  [████░░░░░░] 2/6
현재 단계  Step 2/6 — Review Gate
이번에 확인한 것  <관찰·근거>
사용자 결정  <선택 필요 / 없음>
다음 단계  Step 3/6 — 전략·표현·매체 선택
```

`0=Absorb`, `1=Author`, `2=Review Gate`, `3=Visual Strategy`, `4=Implement`, `5=Verify & Release`를 공통 진행 단위로 사용한다. 건너뛴 단계는 `skipped + 이유`를 표시하고, 진행바는 실제로 닫은 단계만 채운다. 진행바가 품질·사람 이해·릴리즈 통과를 뜻하지는 않는다.

### 명시적으로 받아야 하는 사용자 결정

1. **목적 확인**: `goal`, 청중, 산출물, 성공 조건이 명시적으로 확인되기 전에는 저작·시각 전략을 시작하지 않는다.
2. **원본/이전 작업 처리**: 원본 또는 이전 산출물이 있으면 `continue_improve`(이어서 개선)와 `fresh_start`(새로 시작) 중 하나를 반드시 확인한다. 원본이 없을 때만 `not_applicable_no_existing_work`로 기록한다.
3. **전략 선택**: 열려 있는 전략 축마다 최소 두 개의 후보를 만든다. 각 후보는 `imagegen`으로 만든 시각 콘셉트 이미지와, 목표 매체 전체를 대표하는 실제 렌더 화면을 함께 제시한다. 사용자는 후보를 비교해 선택하거나 재탐색을 요청한다. 이미지 생성이나 전체 렌더를 만들 수 없으면 선택을 가장하지 않고 `blocked_preview_generation`으로 멈춘다.
4. **색상 선택**: 팔레트 이름이나 색상칩만 보여 주지 않는다. 같은 콘텐츠·같은 정보량으로 만든 **완전한 UI/슬라이드/문서 화면**을 후보별로 보여 준다. 필요한 모든 표면(기본, 상태/오류, 데이터·읽기·행동 표면 등)은 `required_surface_ids`로 먼저 정하고, 각 후보가 모두 덮는지 비교한다. HCI 기준인 대비·가독성·주의 계층·상태 의미·색각 다양성·감정적 톤을 평이한 질문으로 안내한 뒤 사용자 선택을 받는다.
5. **릴리즈 저자 표기**: 릴리즈 직전 `include_author_credit`, `omit_author_credit`, `custom_credit` 중 하나를 확인한다. 저자명·역할·표기 위치가 주어지지 않으면 임의로 넣거나 빼지 않는다.
6. **향후 사람 피드백**: 현재 `human_feedback_mode: off`를 유지한다. 다만 나중에 사용자가 켜면 쓸 수 있도록 7점 리커트 문항과 자유응답 문항을 `references/user-decision-and-feedback.md`에서 제공한다. 이 문항은 피드백을 수집하기 위한 도구이지, 사람 이해·행동 변화를 이미 입증하는 증거가 아니다.
7. **도구·기능 구현**: 필요한 기능을 프롬프트 지시로만 남기지 않는다. image concept은 `imagegen`, 목표 매체 렌더는 코드 renderer, 웹 UI의 전체 표면 확인은 portable browser adapter의 URL·screenshot·DOM/상태 증거로 실행한다. Python이 없으면 `scripts/visual-authoring-runtime`이 OS 패키지 관리자로 설치를 시도한 뒤 실행한다. browser 또는 image converter가 없으면 runtime은 알려진 OS 패키지 관리자만 사용해 `설치 계획 → 설치 시도 → 재탐색 → 원래 작업 재시도` 순서로 처리한다. 설치를 끄거나 권한·네트워크·패키지 관리자가 없을 때는 `dependency_installation_*` JSON에 실행 가능한 명령·이유를 남긴다. 발견된 browser가 capture를 끝내지 못하면 안전한 profile·발견 후보를 제한적으로 재시도하고, 모두 실패하면 `browser_runtime_failed`와 실행 기록을 남긴다. host browser의 URL 정책이 막은 경우에는 우회하지 않고 `blocked_tool_runtime`으로 닫는다. 기능이나 증거를 가정해서 통과시키지 않는다.

`references/user-decision-and-feedback.md`는 질문 문구, 비교 화면의 최소 범위, HCI 설명, 피드백 문항과 사용 경계를 소유한다. `references/tool-runtime-implementation.md`는 도구·코드·인앱 브라우저 어댑터와 실행 증거를 소유한다. `scripts/validate_visual_authoring_decision_packet.py`는 목적 확인, 원본 선택, preview coverage, 색상 비교, 도구 구현, 릴리즈 저자 표기, 사람 피드백 OFF/ON 상태를 구조적으로 검사한다.

---

## Source-First Sequential Action Plan

원본 artifact(PPTX, PDF, PNG/JPG, HTML, 문서, 스케치, 기존 슬라이드 렌더)가 제공되면 먼저 역할을 분류한다. `baseline_to_recreate`/`legacy_to_improve`처럼 fidelity를 약속한 원본은 Source-First parity 게이트를 닫는다. `reference_only`/`asset_pool`/`evidence_source`는 관찰·영감·근거용이며 1:1 대조를 강제하지 않는다. 원본이 없으면 `source_first: skipped_no_original`을 기록한다.

**순서의존 행동 계획** — 중간 단계를 건너뛰면 다음 단계의 판단 근거가 사라진다. 상세 템플릿은 `references/source-first-regeneration.md`.

| 순서 | 행동 | 닫는 증거 |
|---:|---|---|
| 0 | 작업 범위 고정 | target artifact, audience, delivery format, editability target |
| 1 | 원본 확보 | original files/paths/screenshots/version, 권한·수정 금지 경계 |
| 2 | 원본 인벤토리화 | slide/page/scene id, asset list, text/table/chart/image/native feature 목록 |
| 3 | 원본 해체 | 정보 구조, 장면 의도, 시각 계층, 읽기 순서, 상호작용/발표 기능 |
| 4 | 보존/전이/폐기 판단 | `preserve`, `transfer`, `discard`, `regenerate` 라벨과 이유 |
| 5 | 오늘의 목표 재정의 | 원본 대비 무엇을 같게/다르게 만들지 |
| 6 | 저작 기준서 작성 | Source Decomposition Packet + Outline Notes |
| 7 | 통합교재/본문 원본 확정 | learner-facing text, instructor notes, evidence table 분리 |
| 8 | 장표/시각 구조 설계 | scene/page map, IA, object hierarchy, reading order |
| 9 | 시각 방식 선택 | Design Exploration Gate 후보/선택/거절 |
| 10 | 편집 가능성 판단 | 의미·fit가 큰 객체만 native화, 복잡한 장면은 이미지 layer 유지 |
| 11 | 구현 | native object + image base + meaning layer + notes/theme/layout |
| 12 | 렌더 검증 | screenshot/PDF/PNG/HTML render proof |
| 13 | 네이티브 검증 | PowerPoint/Slides open, editable object, speaker notes, read order |
| 14 | 역할별 검증 | fidelity baseline은 source parity, reference benchmark는 content-fit observation |
| 15 | 피드백 수집 | gap을 `fix_now` / `defer` / `reject_with_reason`으로 분류 |
| 16 | 다시 생성 | 부분 땜질이 아니라 업데이트된 packet으로 재빌드, 이전 증거는 stale |

**편집 가능성 판단 원칙**: 생성된 것이 단순 도형·텍스트·표·차트·화살표·IA·프로세스처럼 의미 단위와 편집 가치가 크면 네이티브 객체로 전이한다. 사진적 장면, 복잡한 일러스트, 분위기, 질감, 사람/공간 묘사처럼 형태 보존 가치가 편집 가치보다 크면 이미지로 유지하고 의미 라벨·화살표·콜아웃만 native/HTML/SVG layer로 올린다.

---

## The Pipeline (Phase 0 → 5)

순서 의존. 각 Phase는 진입/탈출 게이트를 가진다. 원본 artifact가 있으면 `Source-First Sequential Action Plan`을 먼저 실행하거나 Phase 1 앞에 명시적으로 결합한다. 모든 요청이 6단계를 전부 밟는 것은 아니다 — 규모에 맞게 Phase를 건너뛰되(예: 단일 소스면 Phase 0 skip), **건너뛴 Phase는 명시**한다.

```
[Phase 0] Absorb        (외부 자산 다수 → 정본 어휘 흡수; GGACA R1~R6/M0~M8)
   ↓  게이트: 외부 자산 4조건 충족 시만 진입. 아니면 skip 명시.
[Phase 1] Author        (인지적 저작 패킷 → course-flow → slide-plan → symbol → design 준비)
   ↓  게이트: reader_situation/cognitive_task/desired_action/evidence_boundary와 공개 독자 표면 경계 고정. outline notes 존재.
[Phase 2] Review Gate   (제작 전 판정: route_status + claim 경계 + image-required)
   ↓  게이트: route_status 결정됨. observable_proxy vs human_outcome_claim 분리됨.
[Phase 3] Visual Strategy & Expression Select (콘텐츠 전략 → 선택형 표현 시스템 → 매체 구현 계획의 3축)
   ↓  게이트: content-fit hierarchy + 후보별 imagegen concept preview + 전체 표면 render preview + 사용자 전략/색상 선택 + 선택/거절 근거 + artifact-level design-system lock + scene-centered packet. 시스템은 잠그되 장면 재료는 open set.
[Phase 4] Implement     (랜딩/앱UI/슬라이드/시각문서; scene-base·SVG-meaning·system-token 레이어 분리)
   ↓  게이트: 웹/CSS는 hardcoded hex/px 0건. PPTX는 theme/style materialization + Native Object Intent Plan + 계산형 배치 감사. 번역·구체화 시 reflow + proof refresh.
[Phase 5] Verify & Release (근거 기반 PASS/CONDITIONAL/FAIL, 5초 테스트, PPTX open check, surface 분리)
       게이트: proxy/human/format 증거 분리 보고. 공개 표면·산출물 역할·포맷 표준 기능을 확인하고, 사람 실측 전 human-outcome 확정 금지.
```

전체 요청 규모에 따라:
- **가벼운 시각화 리뷰**: Phase 2만(리뷰 게이트) + Phase 5 근거.
- **랜딩/앱 UI 빌드**: Phase 1(축약) → 3 → 4 → 5.
- **강의 슬라이드/PPTX**: Phase 1(전체) → 2 → 3 → 4 → 5.
- **교재/논문 흡수 집필**: Phase 0 → 1 → (필요시 4는 시각 산출물 한정) → 5.

---

## Phase 0 — Absorb (GGACA: 외부 자산 흡수 집필)

**언제**: 아래 4조건이 **모두** 참일 때만. 하나라도 아니면 Phase 0 skip을 명시하고 Phase 1로.
1. 외부 자산이 여러 개(다른 저자 책·논문·코퍼스·도구 어휘)를 단일 deliverable로 묶는다.
2. 원본을 손대지 않는다(read-only, 인용·요약이 아니라 흡수).
3. 저자 정본 어휘가 따로 있어 외부 내부 어휘를 본문에 노출하지 않는다.
4. 사이클로 닫는다(한 번에 끝내지 않고 게이트+인계 1문장).

**6개 잠금 규칙 (R1~R6)** — 매 사이클 상속. 새 사용자 결정은 충돌 카드 5줄로 R7·R8 추가 또는 R1~R6 갱신.

| 규칙 | 정의 |
|---|---|
| R1 | 외부 어휘 본문 노출 0 (Reference 줄에서만 출처 표기) |
| R2 | 비유 어휘 본문 노출 0 (정본 어휘로 교체) |
| R3 | 정본 핵심 문서 무수정 (사이클 종료까지 line/byte 0건) |
| R4 | 외부 원본 무수정 (read-only, 0건) |
| R5 | baseline 정정은 백업 필수 (`*.bak_<DATE>` + 사유) |
| R6 | 새 개념 도입 0 (외부 어휘는 정본 어휘로 번역해 흡수) |

**9단계 게이트 (M0→M8)** — 순서 의존. 상세는 `references/absorption-cycle.md`.

| 게이트 | 닫는 것 |
|---|---|
| M0 | 흡수 골격 확장 (외부 자산 → deliverable 구조에 1줄 배정) |
| M1/M2 | 본문 전/후반부 (필요 시 unfolding 해석 호출) |
| M3 | 충돌 해소 (충돌 카드 5줄, 본문 라인 번호로 닫음) |
| M4 | 매니페스트·빌드 (forbidden_terms / required_canonical_terms 잠금) |
| M5 | 렌더링 (단일 본문 조립 + 최종 형식) |
| M6 | 검증 (5개 카운트: V-Forbidden=0, V-Required≥N, V-TheoryFoundation, V-NewAbsorption, V-FrontHero=3/3) |
| M7 | 5초 테스트 (첫 화면 약속 3요소 + 사람 5인 실측) |
| M8 | 릴리즈 (원본 보존 증명 + 게이트 상태 동기화; 리스크는 Addendum) |

**탈출 게이트**: forbidden 어휘 본문 0, 정본·외부 원본 무수정 증명, 충돌 로그 닫힘, 다음 사이클 인계 1문장.

---

## Phase 1 — Author (인지적 문서/슬라이드 저작)

디자인 시스템·템플릿·팔레트를 **먼저 고르지 않는다.** 순서는 고정:

```
course-flow-map.md  →  slide-planning-map.json  →  symbol-inventory.json  →  semantic-design-system.json
(전체 흐름)            (슬라이드별 목적·인지작업)      (의미 담을 상징)            (앞 3개에서 파생)
```

**Original Source Decomposition Gate** — 원본 artifact가 있을 때는 저작 패킷보다 먼저 또는 저작 패킷과 함께 작성한다. 없으면 `skipped_no_original`.

```
source_role: reference_only | baseline_to_recreate | legacy_to_improve | asset_pool | evidence_source
original_source_inventory: <file/page/slide/scene id + asset list + native feature list>
source_scene_map: <각 원본 장면의 의도·정보 구조·읽기 순서·시각 계층>
source_text_map: <표지/본문/노트/라벨/표/차트/콜아웃 텍스트>
preserve_transfer_discard_decisions:
  preserve: <그대로 유지할 것>
  transfer: <목표 매체의 native/text/vector/object로 다시 만들 것>
  discard: <버릴 것 + 이유>
  regenerate: <개선 목표로 다시 만들 것 + 기준>
editability_value: high | medium | low, with reason
source_contract: fidelity_baseline | reference_benchmark, with reason
source_parity_target: pixel-close | structure-close | meaning-close | improved-variant | not_applicable_reference, with reason
```

PPTX/HTML/이미지 원본을 “그대로” 옮기는 작업은 이 packet 없이 빌드하지 않는다.

## 코퍼스 기반 에세이 문법 모듈

특정 작가의 공개 글, 또는 접근 가능한 대화·로컬 기록을 읽고 관찰된 호흡을 웹·문서·시각 시스템에 옮길 때 사용한다. 이 모듈에서 `브런치 문법`은 브런치 플랫폼의 공식 기능이나 보편적 글쓰기 규칙이 아니다. **저자 코퍼스나 명시적으로 경계를 둔 대화 코퍼스에서 관찰한 흐름을 임시로 부르는 이름**이며, 결과물에서는 출처 역할과 관찰 범위를 함께 적는다.

### 적용 순서

1. `source_role: author_corpus_reference` 또는 `conversation_corpus_reference`로 잠그고, 원문·대화 기록은 read-only로 둔다. 여러 외부 저자를 한 산출물에 흡수하는 일이 아니면 Phase 0은 `skipped_author_owned_corpus`로 기록한다. 대화 코퍼스는 접근 가능한 표면, 사용할 수 없는 표면, 변환 방식, 출처 경계를 별도로 기록한다.
2. 대화 코퍼스에는 언어학·상담심리학·코칭·행동변화·상징 체계·인지과학 렌즈를 각각 `관찰 / 제한된 해석 / 주장하지 않는 것`으로 적는다. 이 기록은 이론의 경험적 검증이나 사람의 진단·성과 판정이 아니다.
3. 같은 저자의 글에서 최소 세 편을 고르거나, 대화 코퍼스에서 최소 세 표본을 골라 각 표본의 `entry_tension`, `exploration_question`, `context_bridge`, `thought_shift`, `open_end`를 관찰한다. 모든 표본에 다섯 요소가 똑같이 있을 필요는 없지만, 코퍼스 전체에는 시작의 긴장·맥락 연결·열린 끝이 확인되어야 한다.
4. 관찰한 문장, 코퍼스 해석, 대상 매체의 적응안을 분리한다. 글·대화에 없는 저자 의도·독자 반응·플랫폼 효과는 추정으로 채우지 않는다.
5. 대상 매체에 옮길 때는 `긴장/장면 → 질문 → 맥락 → 관점 이동 → 열린 끝`의 읽기 흐름을 우선 검토한다. 제목 아래의 짧은 불편함이나 장면, 본문 중간의 근거·사례, 마지막의 열어 둔 질문이나 다음 생각을 사용할 수 있다.
6. 플랫폼 chrome, 고정 CTA, 저자 권위를 가장하는 인용, 실제 독자 공감/전환 주장은 이식 대상에서 제외한다. CTA가 필요하면 글의 끝과 분리된 기능 요소로 두고, 열린 끝을 CTA로 바꾸지 않는다.

### 시각 적응 규칙

- 첫 화면은 결론을 판정하기보다 읽고 싶은 긴장과 질문을 만든다. 과장된 문제 해결 약속이나 심판자 말투는 피한다.
- 본문은 넉넉한 읽기 폭, 장면과 맥락의 교대, 한 번에 하나의 관점 이동을 지원한다. 색·폰트·컴포넌트 값은 프로젝트 디자인 시스템에서 결정한다.
- 사례·인용·이미지는 글의 장면이나 맥락을 명확히 할 때만 쓴다. 정확한 출처와 조건은 meaning layer가 보유한다.
- 끝은 “정답”보다 독자가 자신의 상황으로 되돌아갈 여지를 남긴다. 이는 사람 반응을 보장하는 장치가 아니라 저작 가설이다.

### Fixed / Flexible / Decisional

| 층 | 이 모듈에서 고정하거나 맡기는 것 |
|---|---|
| Fixed | `essay-grammar-packet` 스키마, 상대 경로 원문 참조, 최소 세 표본, 관찰 역할 enum, 플랫폼 공식 문법·사람 성과 주장 금지, validator |
| Flexible | 선택할 글, 실제 문장·장면, 대상 매체, 디자인 토큰, 어떤 질문과 열린 끝을 보존할지 |
| Decisional | 코퍼스에서 관찰한 흐름이 현재 글·독자 상황에 맞는지, 보존/전이/폐기할 요소, CTA와 열린 끝의 분리 방식 |

`references/author-corpus-essay-grammar.md`가 packet 필드, 해경 코퍼스 예시, 출처·라이선스·검증 경계를 소유한다. Fixed 형식은 `scripts/validate_essay_grammar_packet.py`가 검사한다. LLM은 관찰·이식 이유만 제안하고, 코드가 schema admission과 주장 경계를 소유한다.

**인지적 저작 패킷** (`R→P→M→W→A`: Research/Person/Message/Writing/Audit) 필수 필드 — 상세 `references/slide-authoring.md`:
- `reader_situation`, `cognitive_task`, `desired_action`, `semantic_fit`, `evidence_boundary`, `output_route`, `verification_surface`
- 약하거나 접힌 내용은 unfolding 해석(folded_unit → weakness_diagnosis → CTA 질문 → unfolding_trace → 재작성)으로 편다.

**Outline Notes 게이트** — storyline/시각화/PPTX 빌드 전, 흐름을 검사 가능하게: `reader_situation`, `deck_purpose`, `section_flow`, `slide_sequence`, `title_story_draft`, `visible_message`, `spoken_notes`, `evidence_links`, `visual_intent`, `open_questions`. 없으면 시각화로 넘어가지 않고 writing으로 돌아간다.

**Storyline/Readability 게이트** (시각화 직전 6검사, proxy 판정이지 human outcome 아님):
Title-Only Story / Assertion-Evidence / One-Beat / 5-Second Scan / Cognitive-Load / Evidence-Boundary.

**전체 덱 품질 비교/요인 추출**: 기존 슬라이드의 품질을 비교하거나 반복 검토 신호를 요인으로 기능화할 때는 `references/cognitive-slide-quality-factors.md`와 `scripts/analyze_slide_quality_factors.py`를 사용한다. 원본 PPTX는 read-only로 읽고, package 관찰·인지 패킷·렌더 기반 검토 코드를 분리한다. 로컬 비교 덱은 구조적 분포를 제공할 뿐 범용 품질 순위가 아니며, PCA/상관·geometry·객체 수를 콘텐츠 적합성, 사람 이해, 학습성과 판정으로 승격하지 않는다.

**레이아웃 요소 계산** — PPTX 배치 전 각 요소: `element_tradeoff`(주의비용·공간비용 vs 의미이득), `placement`, `front_back_order`, `reading_order`, `native_object_order`, `overlap_risk`. 코드 감사는 선언된 `geometry_constraints`를 기준으로 `alignment_error`, `spacing_deviation`, `overlap_violation_count`, `out_of_bounds_count`, `connector_detachment_count`, `object_density`를 계산한다. 모든 간격을 같게 만드는 것이 아니라 의미 그룹별 의도값과의 편차를 잰다.

**Session-feedback 게이트**: 반복 리뷰 코멘트를 재사용 검사로(제목 자연스러움, 장식 부하, 내부 메타데이터 노출, 법/규제 AI 경계, 인용 링크, 표/본문 적합, 프롬프트 지식구조).

---

## Phase 2 — Review Gate (제작 전 시각 판정)

시각 관련 요청은 **일단 리뷰 게이트로 잡는다.** 이미지 생성/SVG/PPTX/HTML로 직행하지 않는다(리뷰가 명시적 out-of-scope가 아닌 한). 상세 `references/review-gate.md`.

**claim 경계 분리 (핵심)**: `observable_proxy` / `inferred_risk` / `human_outcome_claim`. 사람 이해·설득·몰입·전이·학습성과는 이 게이트만으로 통과 불가.

**route_status 결정** (이미지 필요 여부):
- `SVG_ALLOWED`: 구조·추상·데이터/다이어그램 우선 → 결정적 SVG/HTML/토큰이 주 비주얼.
- `ROUTED_IMAGE_REQUIRED`: 구체 장면·사진·일러스트 base가 필요 → 이미지 생성 라우팅.
- `SVG_PROXY_ONLY` / `BLOCKED_IMAGEGEN`: 실패 종료 상태. `Done`/`cinematic_pass`/`human_pass`로 닫을 수 없음.
- `INTEGRATED_HYBRID`: 이미지 base + 결정적 의미 레이어 결합.

**결정 라벨**: `usable` / `candidate` / `blocked` / `hypothesis only`. 외부 증거 없이 `human_pass`, `high_quality_slide_pass`, `cinematic_pass` 보고 금지.

**실행 라우팅**: 이미지 → `imagegen`; 슬라이드/PPTX 빌드 owner → `slides`/`hybrid-slide-pipeline`/`hybrid-deck-factory`; 문서/PDF/HTML → `carbon-doc`/`doc-converter`/`pdf`; 핵심 VLP metric → `vector-language-cognition`. (이들은 별도 owner이며 본 스킬이 조율만.)

**선택형 VLC 어댑터(있을 때)**: 프로젝트가 제공한 `surface_vlc_gate` / `run_surface_delivery_gate`를 project config의 상대 경로 또는 명령으로 연결한다. 이 패키지는 특정 workspace CLI를 전제하지 않는다. 어댑터가 없으면 점수 날조 금지 — 구조화 packet을 반환하고 게이트를 `blocked`로 남긴다.

---

## Phase 3 — Visual Strategy & Expression Select (콘텐츠 우선, 매체와 직교)

여기서 선택하는 것은 하나가 아니라 세 축이다. 첫째 `content_visual_strategy`는 콘텐츠 관계와 독자 과업에 맞는 표현 구조다. 둘째 `expression_system`은 그 구조를 꾸리고 일관되게 만드는 선택형 도구다. Carbon·Vivid·브랜드·커스텀은 이 둘째 축의 옵션일 뿐 “시각화” 자체가 아니다. 셋째 `medium_implementation_plan`은 PowerPoint native, SVG/HTML, image, chart/table, hybrid 같은 구현 방식이며 표현 시스템과 직교한다. 상세는 `references/design-systems.md`.

**Content-Fit Quality Hierarchy** — 아래 순서를 뒤집지 않는다:

1. 콘텐츠·독자 과업·원하는 행동 적합성
2. 의미 관계·시각 계층·읽기/발화 흐름
3. 목표 매체의 의도적 구현과 수정 경계(PPTX라면 native object intent)
4. 계산 가능한 배치 안정성·접근성·재현성
5. 렌더·패키지·native open 증거
6. 실제 사람의 이해·행동·학습성과 증거

레퍼런스 유사도는 진단 보조다. 사용자가 faithful recreation을 명시한 경우에만 parity gate가 되며, 그 외에는 `improved_variant` 판정을 결정하지 않는다. “더 잘 만든다”는 더 닮게 만드는 것이 아니라 콘텐츠가 더 빨리 읽히고, 더 잘 가르치고/행동시키며, 사람이 더 쉽게 수정하고, PowerPoint에서 안정적으로 작동하게 만드는 것이다.

**Design Exploration Gate**:
- 먼저 비교·과정·타임라인·데이터·장면·워크숍·편집/강의 등 콘텐츠 전략 후보를 만든다.
- 표현 시스템/브랜드 스타일이 명시적으로 고정되지 않았고 선택이 결과를 바꾼다면 최소 3개 표현 후보와 거절 근거를 기록한다. 매체가 PPTX라는 사실만으로 탐색을 생략하지 않는다.
- `신호 없음 -> Carbon`, `운영 장표 -> 무조건 Carbon`, `vivid 요청 -> 무조건 Vivid` 같은 단축 선택을 금지한다.
- 이미 답이 명확한 축에 형식적인 3개 후보를 만들지 않는다. 그 경우 `settled_with_reason`으로 닫고 콘텐츠 전략의 대안을 검토한다.
- 사용자가 선택해야 하는 열린 축은 후보 설명만으로 닫지 않는다. 후보마다 imagegen 시각 콘셉트와 동일 정보 범위를 가진 target-surface render를 만들고, 비교 화면을 본 뒤 `user_selected` 또는 `reexplore_requested`로 기록한다. 부분 카드·색상칩·무관한 moodboard는 전체 표면 비교 증거가 아니다.
- 색상은 대비, 가독성, 주의 계층, 상태 의미, 색각 다양성, 톤을 설명한 뒤 실제 전체 화면으로 비교한다. 필요한 화면 범위가 정의되지 않았거나 후보가 그 범위를 덮지 못하면 palette 선택을 진행하지 않는다.

### Cognitive Visual Encoding Gate

시각화 종류를 먼저 고르지 않는다. 각 의미 단위에서 `독자가 무엇을 추론해야 하는가`를 먼저 정하고, 콘텐츠 관계에 맞는 시각 문법 후보를 비교한 뒤 하나를 선택한다. 비교는 정렬된 대비·행렬, 과정은 경로·흐름, 인과는 원인-결과 사슬·피드백 루프, 계층은 트리·중첩, 판단은 분기·기준 행렬처럼 **관계가 후보군을 제한**하지만 자동으로 스타일을 결정하지는 않는다.

새로 만들거나 전면 재구성하는 장형·다섹션 덱은 `visual-silhouette-manifest.json`의 `schema_version: 2`를 사용하며 각 슬라이드에 다음 판단 패킷을 남긴다.

```yaml
unit_id: <stable semantic unit id>
source_claim: <reader-facing claim or task>
reader_task: <compare | trace | decide | locate | practice | explain | other>
relationship_type: <content relationship>
inference_goal: <what the reader should infer>
candidate_grammars: [<materially distinct visual grammar>, ...]
selected_grammar: <one candidate>
selection_reason: <relationship + reader task fit>
visible_cues: [<cue the reader can actually see>, ...]
suppressed_cues: [<intentionally omitted cue>, ...]
reading_path: <intended scan or reveal order>
evidence_state: observed_computation | inferred_proxy | calibrated_proxy | human_outcome | blocked_external
claim_boundary: observable_proxy | inferred_risk | human_outcome_claim
validation_boundary:
  technical_editability_proxy: pass | fail | not_run | not_applicable
  semantic_structure_proxy: pass | fail | not_run | not_applicable
  cognitive_readability_proxy: pass | fail | not_run | not_applicable
  human_outcome_validation: pass | fail | not_run | blocked_by_human_input
recovery_action: <source-level correction when a gate fails>
```

`vector-language-cognition`이 `evidence_state`의 정의와 인지 proxy/사람 검증 경계를 소유한다. 이 스킬은 그 값을 소비하는 caller adapter이며 core metric·enum·schema를 임의로 추가하거나 이름을 바꾸지 않는다. `evidence_state`와 Phase 2의 시각 주장 분류(`observable_proxy`/`inferred_risk`/`human_outcome_claim`)도 서로 대체하지 않는다. 전자는 증거 상태, 후자는 현재 시각 판단의 주장 강도다. 실제 사람 검증 전에는 이해·몰입·학습성과를 확정하지 않는다.

기존 `schema_version` 없음/1 manifest는 과거 산출물 감사용으로만 허용한다. `--require-cognitive-encoding` 없이 기존 다양성 검사를 재현할 수 있지만, 이를 새 장형 덱의 전체 확장·릴리즈 승인으로 재사용하지 않는다.

## Fixed Design System / Open Visual Materiality / Scene-Centered Meaning Contract

프로젝트마다 디자인 시스템의 실제 값은 Flexible이지만, 한 산출물의 제작이 시작되면 artifact 단위 계약으로 잠근다. 잠그는 것은 스타일 문법이지 화면 템플릿이 아니다.

```yaml
design_system_lock:
  state: locked | not_applicable
  lock_id: <artifact-level stable id>
  reason: <required only when not_applicable>
  token_style_namespace: <single namespace or explicit no-token reason>
  typography_hierarchy: <roles and scale policy>
  spacing_density: <spacing rhythm and density policy>
  component_grammar: <shape, border, elevation, container rules>
  status_semantics: <meaning of accent/status colors and marks>
  accessibility_contrast: <contrast, readable size, motion, alt/reading-order policy>
```

이 잠금은 장면마다 같은 카드, 2단 레이아웃, 카메라, 아이콘, 실루엣을 반복하라는 뜻이 아니다. 토큰·서체 계층·간격 리듬·컴포넌트 문법·상태 의미·접근성은 일관되게 유지하되, 장면의 공간 구조·시점·이미지/도형 재료·읽기 경로는 콘텐츠 관계에 맞춰 달라질 수 있다. 잠금 뒤 값이 바뀌면 새 `lock_id`로 갱신하고 기존 style/render proof를 stale 처리한다.

**Open Visual Materiality**는 허용 목록이 아니라 열린 후보 공간이다. 사진적 장면, 일러스트, 콜라주, 3D, 종이·오브젝트 연출, 지도·해부·스토리보드, UI 시뮬레이션, 데이터 형태, 타이포그래피 구성, SVG/native diagram 등 현재 또는 이후 LLM이 이미지로 만들 수 있는 모든 표현을 후보로 둘 수 있다. 이 열거는 whitelist가 아니다. source fidelity, brand, license, safety, accessibility, target medium, production capacity가 실제 제약일 때만 후보를 닫는다. 열린 후보 공간은 이미지를 강제하지 않으며 `SVG_ALLOWED`, `ROUTED_IMAGE_REQUIRED`, `INTEGRATED_HYBRID` 경로는 그대로 유지한다.

**Scene-Centered Meaning**은 이미지 경로에만 적용하지 않는다. 장면은 `concrete_world`(사람·공간·사물), `operational_state`(업무 상태·행동·완료 근거), `abstract_relationship`(비교·과정·인과·계층·판단 관계) 중 하나로 정의할 수 있다. 한 장면은 하나의 독자 추론 또는 행동을 우선하지만, 하나의 장면이 하나의 반복 레이아웃을 뜻하지는 않는다. 모든 주요 의미 단위는 구현 전에 아래 packet을 남긴다.

```yaml
scene_first_judgement_packet:
  unit_id: <stable id>
  source_sentence: <source claim or task>
  artifact_role: <cover | section | explanation | evidence | practice | action | other>
  one_scene_statement: <one scene and one job>
  scene_mode: concrete_world | operational_state | abstract_relationship
  concrete_entities: [<recognizable people, objects, states, nodes, or anchors>, ...]
  action_or_state_change: <what happens or changes>
  core_read_3s: <what should register first>
  reader_inference_or_action: <what the reader should infer or do>
  visible_cue: [<non-label cue>, ...]
  semantic_boundary: <what the visual must not imply>
  deterministic_meaning_items: [<exact Korean, number, condition, evidence label, accessibility text>, ...]
  design_system_lock_ref: <lock_id>
  materiality_candidate_space: open_set
  open_materiality_candidates: [<materially distinct candidate>, ...]
  selected_materiality_reason: <scene/relationship/reader-task/medium fit>
  route_status: SVG_ALLOWED | ROUTED_IMAGE_REQUIRED | INTEGRATED_HYBRID | SVG_PROXY_ONLY | BLOCKED_IMAGEGEN
  semantic_variable_ledger: <meaning role + cue + removal criterion>
  pattern_class: <spatial/reading-path class>
  visual_vocabulary_budget: <repeated vocabulary and exception budget>
  localization_state: not_applicable | source_copy | translated_pending_reflow | concretized_pending_reflow | reflow_verified
  recovery_action: <source-level correction>
```

정확한 한국어, 수치, 조건, 표의 값, 근거 라벨, 접근성 텍스트는 결정적 meaning/native/HTML/SVG layer가 소유한다. 생성 이미지에 맡기지 않는다. label-masked 검사는 관계·상태 변화·행동이 보이는지를 검사하며, 정확한 값 자체를 라벨 없이 추측하게 만드는 시험이 아니다. packet의 결정적 필드와 pending 상태는 `scripts/validate_scene_materiality_reflow_contract.py`로 검사한다.

### Semantic Silhouette Diversity Gate

`차분함`, `일관성`, `편집 가능성`은 표현 강도와 구현 경계를 제어하는 말이지, 모든 관계를 같은 2단·표·목록 실루엣으로 바꾸는 허가가 아니다. 외부 이미지가 없더라도 비교·순서·순환·계층·클러스터·지도·해부·스토리보드·의사결정·워크숍 관계는 서로 다른 의미 기반 구조로 보여야 한다.

긴 덱이나 여러 섹션이 있는 덱은 전체 구현 전에 `visual-silhouette-manifest.json`을 만든다. 각 슬라이드는 최소한 `relationship_type`, `silhouette_family`, `semantic_visual`, `semantic_visual_eligible`, 반복 예외가 있으면 `diversity_exception`을 기록한다. 프로젝트는 다음 Flexible 값을 근거와 함께 먼저 잠근다.

- `minimum_families`: 실제 콘텐츠 관계를 커버하는 최소 실루엣 가족 수
- `max_consecutive_same`: 같은 실루엣의 연속 허용 수
- `dominant_family_cap`: 한 실루엣이 비예외 슬라이드에서 차지할 수 있는 최대 비율
- `semantic_visualization_target`: 시각 구조로 전환할 가치가 있는 슬라이드 중 의미 기반 시각화를 갖춰야 하는 비율
- `excluded_roles`: 반복 자체가 학습 행동을 안정시키는 워크시트·개별 작업·피드백 등 예외 역할

수치 자체는 프로젝트 Flexible 값이며 전역 미적 점수가 아니다. 그러나 선언한 값과 실제 분포의 일치 여부는 `scripts/validate_visual_silhouette_budget.py`가 Fixed로 검사한다. 색만 바꾼 동일 구조, 장식 위치만 바꾼 동일 구조, 표를 카드로 감싼 구조는 다른 실루엣으로 세지 않는다. 예외는 `diversity_exception`에 학습 또는 발표 이유를 적을 때만 허용한다.

**Prototype 연결**: 표현군 prototype은 색·서체 후보만 보여주는 표본이 아니다. 실제 덱에서 쓰일 materially different silhouette family를 최소 한 번씩 포함해야 하며, prototype 승인 뒤 새 가족을 추가하면 승인과 format 증거를 stale 처리한다.

```yaml
content_visual_strategy: comparison | process | timeline | data_story | scene | workshop_board | editorial_course | product_ui_simulation | operational_dashboard | campaign | custom
strategy_rationale: <content relationship + reader task + desired action>
expression_candidates: [carbon, vivid, brand:<name>, editorial, custom]
selected_expression_system: carbon | vivid | brand:<name> | editorial | custom | none-with-reason:<reason>
token_or_style_contract: --cds-* | --viv-* | --brand-* | --custom-* | pptx-theme-map:<id> | none-with-reason:<reason>
rejected_candidates: <선택이 열려 있었던 축의 후보별 거절 근거>
medium_implementation_plan:
  medium_target: powerpoint | google_slides | html | svg | pdf | image | hybrid
  object_strategy: native | image | vector | chart_table | hybrid
  style_materialization: pptx_theme | slides_theme | css_tokens | svg_styles | raster | hybrid
content_fit_evidence: <reader_situation + cognitive_task + relationship + verification_surface>
```

**금지**: Carbon·Vivid·native·생성 이미지를 같은 종류의 후보로 비교. PowerPoint native를 token namespace로 취급. 레퍼런스와 닮았다는 이유만으로 개선 판정. 생성 이미지를 장면 근거 없이 추상 배경으로만 쓰고 “몰입”이라고 보고. `차분함=실루엣 축소`, `일관성=반복 레이아웃`, `외부 이미지 없음=의미 시각화 없음`으로 해석. 시각화 다양성을 색상 수·shape 수·장식 수로 대체.

---

## Phase 4 — Implement (토큰·레이어 빌드)

빌드 전 **3가지 선행**: Visual Thesis(한 문장 분위기) / Content Plan(모드별 시퀀스) / Token Plan(사용·확장 변수, 선택한 token namespace 또는 no-token 사유).

**레이어 분리 (필요한 모드에서 조합)**:
- **scene base layer**: 사람·공간·사물·빛·질감·재인성 → 생성 이미지 또는 실사(`imagegen` 경유). 라벨·의미 경로를 여기 고정하지 않는다.
- **meaning layer**: 정확한 한국어 라벨·화살표·주의 경로·근거 콜아웃·순서 → SVG/HTML.
- **system/style layer**: 색·간격·타이포·상태 의미 → 선택한 표현 시스템의 token/style contract.
- **medium materialization layer**: CSS/SVG/PPTX theme/master/layout/native object로 style과 의미를 목표 매체에 실현. native 여부는 표현 시스템이 아니다.

위 레이어 이름은 **제작·검증을 위한 내부 어휘**다. 독자용 표지, hero, 목차, 행동 지시, 배포 상태 문구에 그대로 복사하지 않는다. 독자에게 보여 주는 문장은 해당 교재·문서의 주제, 이해해야 할 관계, 다음 행동으로 다시 쓴다. 다만 어떤 개념이 실제 학습 목표라면 본문에서 독자 언어의 정의와 사례를 갖춰 가르칠 수 있으며, 이것은 제작 상태를 노출하는 것과 다르다.

## Publication Surface Contract

교재·워크북·전자책·배포 PDF·공개 HTML처럼 독자가 직접 읽는 산출물이 있으면, 구현 전에 아래 세 표면을 분리한다.

| 표면 | 목적 | 허용 언어 |
|---|---|---|
| `reader_public` | 표지, 목차, 본문, 독자 행동 | 주제·독자 상황·이해할 관계·다음 행동 |
| `facilitator_editor` | 강의 진행, 편집, 운영 인계 | 진행 지침, 편집 메모, 교육 설계 |
| `production_evidence` | 프롬프트, 검증, 상태, 근거 | 레이어 이름, 검증 키, 파일 상태, 실험·승인 기록 |

**공개 표면 규칙**:
- 제작 레이어 이름, prompt ID, 검증 key, 내부 claim status, `draft`/출간 전 상태 배너, 사람 검증의 내부 보류 표시는 `reader_public` 표지·hero·목차·footer·행동 카드에 두지 않는다.
- 독자에게 필요한 한계·주의는 실제 주제의 위험, 적용 조건, 검증 행동으로 작성한다. 제작팀의 편의를 위한 상태 설명으로 바꾸지 않는다.
- 생성 이미지는 구체 장면과 독자 경험을 돕는 경우 사용한다. 이미지가 순서·라벨·근거·주장 경계를 대신 설명하게 두지 않으며, 그 정보는 독자가 읽을 수 있는 문장과 구조로 제공한다.
- 본권/워크북의 역할, 공개 문구 금지 목록, 포맷별 표준 기능 및 인증 주장 상태를 `publication_surface_contract.json` 또는 프로젝트 SoT에 잠근다. 일반 구조와 결정적 검사 형식은 `references/publication-surfaces.md`와 `scripts/validate_publication_surface_contract.py`를 사용한다.

**표준 기능과 인증 주장의 분리**: 적용 가능한 PDF/HTML/EPUB/문서 표준 기능은 먼저 목록화하고, 사용하거나 비적용 사유를 기록한다. 단, PDF/A·PDF/UA 등 적합성은 전용 검증 증거가 있을 때만 주장한다. 기능을 사용했다는 사실과 인증을 받았다는 주장은 같은 것이 아니다.

**구현 모드**:

### Mode L — Landing / Promo
Hero → Support → Detail → (Social Proof/FAQ) → Final CTA. Hero full-bleed(내부 `.container`만 폭 제한). 브랜드 > 헤드라인 > 본문 > CTA 순 크기. 시네마틱 요구 시 Cinematic Immersion Plan(핵심 메시지·story beat·시각 인과·주의 경로·관점 앵커·5초 테스트) 추가. 모션 2개+.

### Mode A — App UI
Linear-style 절제: primary workspace / navigation / secondary context(inspector) / one accent. 카드 모자이크 대시보드 금지 — 평면 레이아웃 + 구분선·여백·정렬. Utility copy(방향감·상태·행동, hero 카피 금지). 폼/모달 필수 패턴: sensible defaults / shared schema validation / Error Translation Layer(raw 서버 에러 UI 누출 금지) / field-local inline 에러 / progressive disclosure / input formatting(표시≠저장) / live preview / severity tiering / idempotent submit. 모션 절제.

### Mode B — Book / Textbook / Workbook
`교재`, `워크북`, `전자책`, `배포 PDF` 요청에는 먼저 artifact role map을 만든다. 한 파일의 길이, 표지 유무, 체크리스트 수로 본권과 워크북을 판단하지 않는다.

- **본권(교과서)**: 왜 필요한지, 핵심 개념과 원리, 작동 방식, 오해하기 쉬운 지점, 판단 기준, 사례를 설명한다. 각 장은 최소 `설명 → 예시/대조 → 독자가 해 볼 행동`의 흐름을 가진다. 워크시트만으로 본권을 대체하지 않는다.
- **워크북**: 본권의 개념을 실제 맥락에 적용하는 기록지, 점검표, 실험 설계, 회의·실습 표면을 제공한다. 각 활동은 어떤 본권 개념을 적용하는지 연결하며, 근거 설명을 생략한 채 체크 항목만 늘리지 않는다.
- **병행 패키지**: 본권과 워크북을 둘 다 제공할 때는 각각의 파일·목차·표지·메타데이터·링크를 분리하고, 서로를 보완하도록 참조를 제공한다. 한 파일에 합친 경우에도 장과 활동의 역할을 명시적으로 구획한다.
- **독자 경험 가설**: `이해했다`, `저자가 전문가로 보인다`, `나도 해볼 수 있다`는 목표가 아니라 사람 검증 전의 설계 가설이다. 설명의 충분성, 근거의 투명성, 첫 행동의 실행 가능성을 proxy로 점검하고, 사람 반응은 별도 증거로 둔다.

PDF를 배포할 때는 페이지 크기, 문서 메타데이터, 문서 언어, 글꼴 임베딩과 Unicode map, outline/bookmark, 내부 링크, 정적·무암호화·무스크립트 여부, 접근성 구조를 해당 포맷 profile에 따라 확인한다. HTML은 semantic `nav`, anchor/hash 이동, 현재 위치, keyboard focus를 기능으로 검증한다. EPUB은 cover/meta/reading order/TOC/CSS profile을 별도로 기록한다. 상세는 `references/publication-surfaces.md`.

### Mode S — Slide / PPTX
Phase 1 산출(outline notes·slide specs·symbol·visual-system)에서만 빌드. 표준 XML-aware 생성(복구된 PPTX 수리 금지). PresentationML/OPC/DrawingML/notes/theme/layout 검증. **Native Medium Capability Scan**, **Native Object Intent Plan**, **PowerPoint Native Conformance and Source-Level Self-Remediation Gate**, **PPTX Native Runtime Receipt Gate**를 먼저 잠근다. master/layout/theme/placeholders, notes, tables/charts/shapes/connectors, grouping/naming/z-order/read-order, accessibility, 선택적 animation/transition을 기능별 `used | intentionally_not_used | not_applicable`로 판단하고 이유를 남긴다. 기본 theme font는 Pretendard 계열이고, 목차·section·순서화한 title story·automatic slide number는 native 구조로 만든다. 도형 안의 기본 텍스트는 가운데/중간 정렬이며, 의미상 예외는 named object와 이유로만 허용한다. 복잡한 장면이나 수정 가치가 낮은 시각화는 image layer로 둘 수 있으나 raster exception과 동등 텍스트를 남긴다. 객체가 많다는 사실은 native 품질 증거가 아니다. 전체 덱 빌드 전 프로젝트 prototype manifest를 `scripts/validate_authoring_prototype_gate.py --require-authorized`로 통과시킨다. Microsoft PowerPoint open check는 **별도 수동 릴리즈 게이트**다. exact candidate hash와 fresh-process/no-recovery 관찰만 있으면 `pass_native_first_open_pending_release`이며, 전체 슬라이드 검토와 지정 객체 edit round-trip 전에는 릴리즈라고 부르지 않는다. rebuild 뒤 이전 open 증거는 stale이다. 상세 `references/pptx-native-object-authoring.md`, `references/pptx-native-conformance-and-self-remediation.md`, `references/pptx-native-runtime-evidence.md`, `references/prototype-authorization-contract.md`; 계산 감사 `scripts/audit_pptx_native_objects.py`, conformance 감사 `scripts/validate_pptx_native_conformance.py`, receipt 감사 `scripts/validate_pptx_native_runtime_receipt.py`.

원본 PPTX/이미지/HTML을 목표 PPTX로 옮길 때는 Source-First packet의 `preserve_transfer_discard_decisions`를 native 구현 계획으로 변환한다. 텍스트, 표, 차트, IA, 프로세스, 반복 카드, 제목/노트/개요처럼 사람이 고칠 의미 단위는 native placeholder/table/chart/shape/connector/notes로 만든다. 사진적 장면·복잡한 생성 이미지·배경 질감은 이미지 layer로 유지하고, 수정 가치가 큰 라벨·화살표·콜아웃·읽기 순서만 native layer로 올린다.

**External Conversion-Free Build Rule**: PPTX 빌드·렌더·릴리즈 증거는 외부 오피스 변환 프로그램에 의존하지 않는다. 새 후보는 authored source + `pptx-pattern-compiler-manifest.json` + PresentationML/OPC/native-object 감사에서 만들고, 보기 증거는 slide-scoped PNG/contact sheet, HTML/SVG prototype, 또는 이미지 base와 결정적 meaning layer의 통합 proof로 만든다. PDF 배포물이 필요하면 target-format owner가 HTML/PDF pipeline이나 수동으로 승인된 native export evidence를 별도 장부에 남긴다. 어떤 변환 결과도 source family, recovery-lineage 통과, native-runtime pass, 사람 이해 pass를 대체하지 않는다.

### Mode V — Visual Document / Key Visual (시각 시스템 정규화)
기존 CSS의 하드코딩을 토큰으로 정규화. `R→P→M→W→A`: 변수/하드코딩 분포 조사 → 치환 우선순위 → 최소 변경 토큰 치환(+레거시 alias 유지) → 스크린샷/DOM/label-masked 3초 판독 → 결과·실패 기록. 시각 의미 단위표(meaning_unit / visible_cue / masked_read_criterion / risk / recovery_action) 필수. 생성 이미지 사용 시 prompt ledger(model/prompt/output_path/integration_path/verification) 필수.

**Hard Rules**: 웹/CSS 토큰 경로는 hardcoded hex/px 0(예외: `clamp()` 내부, media query breakpoint)과 단일 namespace를 강제한다. PPTX는 선택한 style contract를 theme/master/layout/object style map으로 물질화하고 임의 개별 override를 감사한다. `bx--` Carbon 컴포넌트 클래스 금지. 카드 기본 금지(카드 자체가 인터랙션일 때만). 섹션/슬라이드당 dominant idea 1개. 라벨 가림 상태에서 핵심 의미가 안 읽히면 완료 금지(라벨 추가 말고 visible cue·배치 수정).

---

## Concrete-Language / Localization Reflow Gate

시각 산출물 안의 문장을 번역·자연화·구체화하면 copy edit만 끝난 것이 아니다. `korean`은 한국어 의미·자연스러움·용어 선택을 소유하고, `visual-authoring`은 그 문구가 실제 매체에 들어간 뒤의 줄바꿈·높이·충돌·읽기 순서·접근성·렌더·배포 증거를 소유한다.

추상 표현을 `6–8명 한 반`, `첫 유료 실험`, `2분 신청서`, `통과 기준`, `가져온 자료`처럼 독자가 행동할 수 있는 표현으로 구체화할 수 있다. 단, 원문 사실·수치·조건·주장 경계는 `preserved_facts`에 잠그고 새 사실을 만들어 구체적으로 보이게 하지 않는다. 보이는 문구뿐 아니라 alt text, `aria-label`, 표 헤더, 차트 설명, speaker notes, outline/bookmark, 링크·버튼 이름처럼 독자가 읽거나 기계가 검증하는 의미 표면도 함께 갱신한다.

가시 문구가 바뀌면 이전의 text-fit, overflow, geometry, screenshot, PNG/PDF, page count, text extraction, accessibility tree, native-open 증거는 영향을 받은 표면에서 stale이다. 다음을 다시 계산·렌더한다.

- 줄바꿈, 최소 높이, paragraph/line spacing, reserved action zone
- sibling/overlay 충돌, clipping, out-of-bounds, connector·callout 분리
- desktop, mobile, print/PDF, slide/native 등 실제 target medium의 proof
- `visible_form`, `semantic_label`, `hidden_reading`, `machine_verifiable_count`의 일치

```yaml
localization_reflow_packet:
  unit_id: <matching scene unit id>
  language_owner: korean | source_author | other:<owner>
  source_phrase: <before>
  rendered_phrase: <after>
  preserved_facts: [<number, condition, claim boundary, evidence>, ...]
  affected_surfaces: [<visible and accessible surface>, ...]
  geometry_risks: [<wrap, height, collision, clipping, bounds, pagination>, ...]
  stale_proofs: [<proof invalidated by the copy change>, ...]
  reflow_evidence:
    - surface: <affected target surface>
      proof_type: render | geometry | native_open | accessibility | format
      path: <fresh proof path under project root>
      fresh_after_copy_change: true
  localization_state: translated_pending_reflow | concretized_pending_reflow | reflow_verified
  recovery_action: <source/layout correction when reflow fails>
```

`translated_pending_reflow` 또는 `concretized_pending_reflow`는 릴리즈 상태가 아니다. 문자열 치환 뒤 overflow 0만 확인해도 충분하지 않다. 실제 장면의 의미 계층과 독자 행동이 유지되는지 보고 source/layout을 고친 뒤 fresh proof로 `reflow_verified`를 닫는다.

---

## PowerPoint Native Object Intent / Geometry / Semantic Coverage Contract

PPTX는 `Native Medium Capability Scan` → `native-object-intent-plan.json` → 빌드 → `native-object-audit.json` 순서로 닫는다. intent plan은 의미 단위마다 `semantic_role`, `criticality`, `native_requirement`, `expected_native_type`, semantic object name, edit boundary, group/z-order/read-order, geometry relations, presentation behavior, raster exception을 기록한다. detailed schema와 계산식은 `references/pptx-native-object-authoring.md`.

Fixed 감사는 PPTX와 intent plan의 SHA-256을 기록하고 `out_of_bounds_non_bleed_count`, `unintended_overlap_count`, `max_alignment_error_pt`, `max_spacing_deviation_ratio`, `detached_required_connector_count`, `object_density`, native/critical/relation coverage를 계산한다. critical blocker는 missing/type/relation/read-order와 의도하지 않은 bounds/overlap/connector 위반이 하나도 없어야 한다. 분모가 없으면 full coverage로 간주하지 않고 `not_applicable`로 기록한다.

프로젝트별 의미 그룹·목표 간격·tolerance·noncritical coverage·raster exception은 Flexible이다. 코드는 그 의도값에 대한 편차를 계산하지, 모든 객체를 같은 간격으로 만들거나 “미적 점수”를 만들지 않는다. Decisional 상태는 `pass_local | revise | blocked | needs_human_choice`이며 fixed 관찰, content-fit 판단, render/native/human 증거 trace를 함께 남긴다.

객체 수, shape 비율, geometry audit만으로 좋은 디자인·콘텐츠 적합성·편집 경험·학습성과를 주장하지 않는다. PowerPoint master/layout/theme/placeholders, semantic names/groups, connectors, editable tables/charts, notes, accessibility, 필요한 animation을 의미와 발표 행동에 맞게 의도적으로 쓴다. rebuild 후 geometry/native/render/manual-open 증거는 모두 stale이다.

---

## PowerPoint Native Conformance and Source-Level Self-Remediation Gate

새 PPTX family는 emit 전에 `pptx-native-conformance-contract.json`을 만든다. 이는 PowerPoint 기능을 무조건 전부 넣는 체크리스트가 아니다. `slide_master_layout_theme`, `theme_font_scheme`, `title_placeholder`, `outline_navigation`, `automatic_slide_number`, notes, native text/shape/connector/table/chart, naming/read-order/accessibility, hyperlink, animation/transition, media를 모두 `used | intentionally_not_used | not_applicable`로 분류하고 **각 선택의 이유**를 남기는 capability decision catalog다.

기본 규약은 다음과 같다.

- theme의 major/minor Latin·East Asian 기본 글꼴은 Pretendard 계열이다. 글꼴을 이미지로 연출해야 할 때만 raster exception과 동등 텍스트를 남긴다.
- 제목은 native title placeholder, 개요는 native section list와 TOC native text, 쪽번호는 `automatic_powerpoint` placeholder/field를 쓴다. 일반 텍스트로 번호를 입력하지 않는다.
- 도형 안의 기본 text는 `a:pPr@algn=ctr`와 `a:bodyPr@anchor=ctr`으로 가운데/중간 정렬한다. 왼쪽 정렬 같은 예외는 semantic object name과 이유를 contract에 적는다.
- 사진적 장면·복잡한 일러스트·수정 가치가 낮은 시각화는 image layer로 둘 수 있다. 다만 모든 picture는 semantic role, image 필요 이유, equivalent text를 가진 raster exception으로 등록한다. 의미 라벨·화살표·순서는 native layer가 소유한다.
- 제목을 순서대로 읽었을 때 문서의 방향이 드러나도록 `direction_statement`, ordered `sections`, `title_sequence`, `toc_entries`를 source에 둔다. 순서나 문구가 바뀌면 TOC/section/title/쪽번호 증거를 stale 처리한다.

빌드 뒤에는 다음을 실행한다.

```bash
scripts/visual-authoring-runtime run scripts/validate_pptx_native_conformance.py \
  --pptx build/deck.pptx \
  --contract pptx-native-conformance-contract.json \
  --report build/pptx-native-conformance-report.json \
  --repair-plan build/pptx-native-repair-plan.json
```

`repair_required`는 PPTX를 몰래 수정하라는 뜻이 아니다. 검사기는 source-level self-remediation plan만 쓰고, authored source/manifest/compiler를 고친 뒤 새 `source_family_id`로 다시 빌드하게 한다. recovery dialog 이력이 있는 PPTX는 계속 incident artifact로만 보관한다. `pass_local`도 PowerPoint actual open, selection/edit, 시각 품질, 사람의 이해·행동 변화를 뜻하지 않는다.

상세 schema, status, 검증 경계는 `references/pptx-native-conformance-and-self-remediation.md`가 소유한다.

---

## PPTX Native Runtime Receipt Gate

PowerPoint가 한 번 열렸다는 말은 native-runtime 릴리즈 통과가 아니다. compiler는 build마다 exact candidate path/SHA-256, slide count, baseline criteria, 필요한 named edit round-trip을 담은 `*.powerpoint-native-gate.json`을 만든다. 관찰자는 새 PowerPoint process에서 실제로 본 사실만 별도 observation JSON에 기록한다. `scripts/validate_pptx_native_runtime_receipt.py`만 receipt status를 계산한다.

- **Fixed**: hash binding, `fresh_process`/`exact_candidate`/`no_recovery_dialog`/`all_slides_reviewed` baseline, status vocabulary, receipt 계산은 코드가 소유한다.
- **Flexible**: deck의 slide count, named editable object, 관찰한 사실은 후보마다 바뀐다.
- **Decisional**: 요청한 릴리즈가 first-open까지만 필요한지 전체 review/edit evidence까지 필요한지는 사람이 정한다. partial evidence를 통과로 바꾸지 않는다.

`pass_native_runtime`은 필요한 native 관찰이 모두 끝난 상태다. `pass_native_first_open_pending_release`는 exact hash의 fresh first open에 recovery가 없었지만 review 또는 edit round-trip이 아직 비어 있는 상태다. `fail_native_runtime`은 recovery dialog, hash mismatch, 기록된 edit round-trip 실패다. 그 후보는 incident artifact로 동결하고 source/compiler를 고쳐 새 family를 만든다. `pending_native_observation`과 `blocked_invalid_gate`도 릴리즈 상태가 아니다.

이 기본 경로는 PowerPoint를 자동으로 열거나 버튼을 누르지 않는다. 그런 document-runtime action을 구현해야 하면 먼저 `generate-skill`의 native action-binding contract와 static audit를 적용하고, exact target·권한·event ledger·독립 postcondition을 남긴다. 보통은 사람의 target-bound observation과 결정적 receipt만 사용한다.

```bash
scripts/visual-authoring-runtime run scripts/validate_pptx_native_runtime_receipt.py \
  --gate build/deck.powerpoint-native-gate.json \
  --observation build/deck.first-open.observation.json \
  --report build/deck.native-runtime-receipt.json
```

상세 schema와 claim boundary는 `references/pptx-native-runtime-evidence.md`가 소유한다.

---

## PPTX Pattern Compiler and Evidence-Separation Gate

PowerPoint 복구 대화상자가 한 번이라도 나타난 후보는 **진단용 incident artifact**다. 그것은 정적 구조가 깨끗해 보여도 release, rename, normalization pass, ZIP/XML repair, conversion pass, PowerPoint 재저장, 다음 full-deck build, prototype authorization의 입력으로 사용할 수 없다. 새 후보는 복구 계열과 독립된 `source_family_id`와 새 authored source에서 다시 만든다.

새 PPTX는 `pptx-pattern-compiler-manifest.json`으로 시작한다. Fixed 층은 16:9 EMU canvas, 선언된 pattern library, typed payload, outline/section/list/table/notes/native intent, OOXML/native audit, hash와 recovery-lineage 거절을 소유한다. Flexible 층은 슬라이드별 pattern route, 한국어 문구, 사례, 강사 전환, scene materiality를 판단한다. Decisional 층은 pattern 선택 근거, no-pattern exception, content-fit, `pass_local/revise/blocked` 다음 행동을 남긴다. 이 구분은 코드가 좋은 강의를 판정하거나 LLM이 패키지 규칙을 예외 처리하게 하지 않는다.

덱은 하나의 템플릿으로 복제하지 않는다. `cover`, `question`, `assertion_evidence`, `relationship_map`, `process_loop`, `comparison_matrix`, `decision_boundary`, `workshop_board`, `recap_action`처럼 **의미적 construction family**만 선언하고, 실제 선택은 독자 과업과 관계에 따라 기록한다. 전체 확장 전 선택한 family마다 실제 prototype 한 장을 만들고, fixed audit와 exact-hash PowerPoint `no_recovery_dialog` 수동 증거로만 해당 family를 scale authorization한다.

증거는 반드시 네 장부로 분리한다: `structural_package`, `reading_content`, `viewing_render`, `native_runtime`. 정적 OOXML 검사, 추출 텍스트 검토, 이미지 contact sheet, HTML/SVG prototype, imagegen scene-base 통합 proof, PowerPoint 실제 열림은 서로 대체하지 않는다. exact candidate hash의 fresh native evidence가 없으면 `native_runtime`은 `not_run` 또는 `blocked_by_manual_action`이고 release 후보가 아니다.

상세 schema, no-repair lineage, ledger 정의는 `references/pptx-pattern-compiler-and-evidence-separation.md`; 실행형 manifest 검사는 `scripts/validate_pptx_pattern_compiler_manifest.py`가 소유한다.

---

## PPTX Code-Pattern and Reader-Admission Gate

PPTX 저작의 제어권은 Fixed 코드에 두고 `control_model: fixed_code_orchestrates_flexible_decisions`로 닫는다. LLM은 학습 행동, 의미 관계, 장면 패턴, 독자 문구, 조정 이유를 **선언형 결정값**으로 제안한다. Fixed compiler는 허용된 decision schema만 받아 renderer·native object·OOXML 기능을 적용하고, 모든 pre-emit gate가 통과한 뒤에만 PPTX를 쓴다. LLM이나 프롬프트는 raw OOXML, raw `slide.add*`, 검증 상태, 증거 장부의 합격 값을 직접 만들거나 덮어쓸 수 없다.

새 PPTX family는 빌드 전에 `pptx-code-pattern-catalog.json`을 둔다. catalog는 다음 네 층을 모두 결속한다.

1. `instructional_scene`: slide kind, scene pattern, semantic job, reading sequence
2. `native_object`: renderer, layout family, editable object, connector/group/table/list/notes
3. `ooxml_capability`: `used | intentionally_not_used | not_applicable`, 이유와 코드 증거
4. `verification_evidence`: structural, reading, viewing, native-runtime 장부와 exact artifact hash

각 authored slide kind는 scene pattern·renderer·layout family에 정확히 한 번 연결한다. 보이는 텍스트와 네이티브 객체 생성은 공용 gateway를 통과시키고, 허용된 raw emission API는 gateway 내부의 단일 호출만 남긴다. 공개 독자 문구는 별도의 reader-public policy로 검사한다. 내부 빌드·검증·릴리즈 언어가 발견되면 허용 목록을 넓혀 통과시키지 말고 독자 문장으로 다시 쓴다.

이 게이트의 상세 계약과 최소 예시는 `references/pptx-code-pattern-admission.md`가 소유한다. catalog 결속은 `scripts/validate_pptx_code_pattern_catalog.py`, pre-emit 독자 문구 등록·raw gateway cardinality는 `scripts/reader_surface_admission.mjs`가 강제한다. 패키지에 prompt/reference/code가 모두 들어갔는지는 `references/pptx-code-pattern-admission.capability.json`을 `generate-skill/scripts/audit_capability_embedding.py`로 검사한다.

---

## Phase 5 — Verify & Release

**근거 기반 판정**: 취향 코멘트로 끝내지 않는다. 캡처 경로/DOM 근거 포함 `PASS / CONDITIONAL / FAIL`. 상세 체크리스트 `references/checklist.md`.

- **label-masked 판독**: 라벨을 가려도 key unit 3개+ 식별 가능.
- **5초 / 3초 테스트**: 첫 화면에서 무엇으로 읽히는가. 사람 실측 전에는 `CONDITIONAL` 또는 `candidate/hypothesis only`.
- **claim 분리 보고**: `observable_proxy` / `inferred_risk` / `human_outcome_claim`을 섞지 않는다.
- **format/native 증거**: 스크린샷·모바일(375px 가로스크롤 0)·`prefers-reduced-motion`. Slide는 렌더 증거와 별도로 PPTX open check(no_recovery_dialog) + PresentationML spec + native feature preflight.
- **source-role 증거**: fidelity baseline이면 source parity table을 남긴다. reference benchmark면 콘텐츠 적합성 관찰만 기록하며 1:1 비교를 합격 게이트로 쓰지 않는다.
- **fixed geometry/native 증거**: `observed_computation`으로 계산한 배치·경계·connector·intent coverage를 보고하고, 콘텐츠 적합성/사람 이해를 계산값으로 가장하지 않는다.
- **system/scene 증거**: artifact-level design-system lock과 주요 의미 단위의 scene-first packet이 일치하는지 확인한다. 시스템 일관성을 반복 레이아웃으로, 장면 자유도를 무규칙 스타일 변경으로 대체하지 않는다.
- **localization/reflow 증거**: 번역·자연화·구체화된 가시 문구가 있으면 영향 표면의 이전 proof를 stale 처리하고 fresh geometry/render/native/accessibility proof로 `reflow_verified`를 닫는다.
- **artifact-surface 분리**: learner_facing / instructor_facilitator / production_source / evidence_fact_table / render_native_proof / delivery_handoff. "slides done" 같은 단일 blended 상태로 닫지 않는다.
- **저자 표기 결정**: 배포·공개 인계 전에 저자 표기 포함·생략·맞춤 표기와 위치를 명시적으로 확인한다. provider/provenance와 output brand를 저자 표기로 자동 전환하지 않는다.
- **사람 피드백 상태**: 현재 사람 이해·행동 변화 검증이 `OFF`면 리커트 문항은 제공만 하고 수집·판정하지 않는다. 사용자가 `ON`을 명시한 뒤에만 `references/user-decision-and-feedback.md`의 동의·대상·중단 기준과 함께 사용한다.

사람 이해·설득·몰입·전이·학습성과·릴리즈 준비는 **각각 별도 증거**로만 확정. proxy 통과를 human outcome으로 승격 금지.

---

## Code / LLM Boundary

### Code가 강제 (예외 없음)
- 각 Phase 게이트 미통과 시 다음 Phase 진행 차단.
- 웹/CSS 경로의 hardcoded hex/px와 선택 namespace 밖 style 신규 추가 차단. PPTX 경로는 theme/style map과 Native Object Intent Plan 누락 차단.
- 한 화면에 두 token namespace 혼용 차단(트랙 accent 예외).
- artifact-level design-system lock 뒤 token/style namespace, typography hierarchy, spacing/density, component grammar, status semantics, accessibility/contrast가 새 `lock_id`와 stale proof 갱신 없이 drift하면 차단한다. 같은 레이아웃 반복은 잠금 이행 증거가 아니다.
- 모든 주요 의미 단위는 이미지 여부와 무관하게 scene-first packet을 갖고 `scripts/validate_scene_materiality_reflow_contract.py`를 통과해야 한다. `SVG_PROXY_ONLY`/`BLOCKED_IMAGEGEN`과 localization pending 상태는 릴리즈 후보가 아니다.
- Phase 0에서 forbidden 어휘 본문 카운트 > 0 이면 릴리즈 차단. 정본·외부 원본 수정 발생 시 차단.
- 원본 artifact가 있는데 `original_source_inventory`와 `source_decomposition`이 없으면 faithful transfer/improvement/recreation 주장 차단.
- fidelity baseline인데 source parity table 없이 `그대로`, `동일`, `faithful transfer` 주장 차단. reference benchmark에는 parity table을 강제하지 않는다.
- Phase 2 route_status가 `SVG_PROXY_ONLY`/`BLOCKED_IMAGEGEN`이면 `Done`/`*_pass` 차단.
- 이미지 생성 결과에 의미 경로·추상 라벨·조건 게이트를 맡기지 않는다(SVG/HTML layer 소유).
- 라벨 가림 상태에서 핵심 의미 미판독 시 완료 선언 차단.
- 생성 이미지 사용 시 prompt ledger 누락 차단.
- Slide: zip/XML/PDF/PNG/QuickLook/구 open check로 PowerPoint 릴리즈 준비 주장 차단(rebuild 후 stale).
- Slide: PowerPoint recovery dialog 이력이 있는 candidate, normalized package, conversion output, UI-resave output을 새 candidate family/prototype/release의 source로 쓰는 것을 차단한다. 새 family는 `recovery_lineage_policy: reject_as_source`의 pattern compiler manifest를 가져야 한다.
- Slide: external office conversion output을 build/render/release/native-runtime evidence 또는 source-family seed로 쓰는 것을 차단한다. 대체 경로는 pattern compiler manifest, PresentationML/OPC/native-object 감사, imagegen scene-base + deterministic SVG/HTML/PPTX meaning layer, slide-scoped contact sheet, exact-hash PowerPoint fresh-open evidence다.
- Slide: 새 PPTX family는 `scripts/validate_pptx_pattern_compiler_manifest.py`를 통과하기 전 build/scale 선언을 차단한다. `structural_package`/`reading_content`/`viewing_render`/`native_runtime` 중 하나의 pass를 다른 ledger의 pass로 복사하는 것을 차단한다.
- Slide: 새 PPTX family는 `PPTX Code-Pattern and Reader-Admission Gate`를 통과하기 전 파일 쓰기를 차단한다. LLM decision packet이 raw OOXML, raw emission API, validator 상태, evidence-ledger status를 소유하면 실패한다. authored kind와 scene pattern·renderer·layout이 1:1로 결속되지 않거나 reader-public 문구가 공용 gateway를 우회해도 실패한다.
- Slide: Native Object Intent Plan 없이 객체 수·shape 비율만으로 native 품질 주장 차단. geometry 감사 결과를 human outcome이나 content-fit pass로 승격 금지.
- Slide: `PowerPoint Native Conformance and Source-Level Self-Remediation Gate` 없이 PPTX 릴리즈 후보 선언을 차단한다. capability catalog의 누락·무이유 status, Pretendard theme font drift, native title/section/TOC/automatic slide number 누락, 도형 텍스트의 무이유 비가운데 정렬, 등록되지 않은 raster picture는 `repair_required`다. validator는 report와 source-level repair plan만 만들며 candidate PPTX를 patch·normalize·convert·UI-resave하는 경로를 제공하지 않는다.
- Slide: `PPTX Native Runtime Receipt Gate` 없이 PowerPoint native-runtime 릴리즈 통과 선언을 차단한다. exact candidate hash, fresh process, recovery dialog 부재, ordered full-slide review, named edit round-trip은 receipt validator가 계산한다. first-open만 끝난 후보는 `pass_native_first_open_pending_release`이며, recovery/hash mismatch/recorded round-trip 실패는 incident artifact를 동결한 `fail_native_runtime`이다.
- Slide: 표현군 prototype manifest가 `--require-authorized`를 통과하지 않으면 전체 덱 빌드 차단. 이 validator는 게이트 완료만 증명하며 미적 품질·이해·학습성과를 판정하지 않는다.
- Slide: 여러 섹션/장형 덱에서 `visual-silhouette-manifest.json`과 프로젝트별 diversity policy가 없거나 `validate_visual_silhouette_budget.py`가 실패하면 전체 확장·릴리즈 후보 선언 차단. 색상·장식 변화는 별도 실루엣으로 계산하지 않는다.
- Slide: 새로 만들거나 전면 재구성하는 여러 섹션/장형 덱은 `schema_version: 2`의 인지 시각 인코딩 패킷을 갖추고 `validate_visual_silhouette_budget.py --require-cognitive-encoding`을 통과하기 전 전체 확장·릴리즈 후보 선언 차단. validator의 proxy pass를 사람의 이해·몰입·학습성과로 승격하지 않는다.
- 공개 교재·워크북·배포 문서에서는 `Publication Surface Contract`를 잠그기 전 `reader_public` 표면 릴리즈 후보 선언을 차단한다. 공개 표면에 지정된 내부 제작·검증 언어가 남아 있으면 차단하고, 실제 주제 개념을 본문에서 가르치는 경우는 독자 언어의 정의와 사례를 갖췄는지 별도 판단한다.
- `artifact_profile: textbook_with_workbook`이면 `textbook_main`과 `workbook_companion` 역할·파일·필수 마커가 모두 없을 때 릴리즈 후보 선언을 차단한다. 본권에는 설명·원리·사례, 워크북에는 적용 활동과 본권 연결이 있어야 하며, 파일 수나 페이지 수만으로 통과시키지 않는다.
- `User Decision, Comparative Preview, and Progress Gate` 없이 목적 확인, 원본 계속/새 시작 선택, 열린 전략의 후보 preview, 전체 표면 색상 비교, 릴리즈 저자 표기를 추정으로 닫는 것을 차단한다. preview가 막히면 선택 상태는 `blocked_preview_generation`으로 남긴다.
- 필요한 도구·기능이 실행 가능한 adapter와 evidence path 없이 서술만 되어 있으면 구현 완료·preview 완료를 차단한다. `output_surface: html`/`web_ui`는 code render와 인앱 브라우저 capture·DOM/상태 증거 없이 전체 화면 비교를 닫지 않는다.
- 포맷 표준 profile이 활성화되면 적용 기능 목록, 사용/비적용 사유, 포맷 검증 증거, 인증 주장 상태가 없을 때 릴리즈 후보 선언을 차단한다. PDF/A·PDF/UA 등 인증 문구는 전용 validator 또는 동등한 증거 없이 허용하지 않는다.
- 기존 시각 산출물의 보이는 문구나 접근성 의미 표면이 번역·자연화·구체화되면 영향받은 text-fit/geometry/render/PDF/native-open/accessibility proof를 stale 처리한다. fresh reflow evidence 없이 `reflow_verified` 또는 릴리즈 후보를 선언하지 않는다.
- 신규 핵심 섹션(`Conflict Resolution`, `3-Layer Classification`, `Legacy Package Distillation Gate`, `Runtime Compatibility Gate`, `Provider / Provenance vs Output Brand`)은 Rubric Must에 이름으로 인용 — 삭제 시 validator가 깨진다.

### LLM이 판단 (유연)
- Phase 선택·skip 여부(규모 적합성).
- 콘텐츠 시각 전략과 선택형 표현 시스템 후보 선택(선택/거절 근거). 매체/native 구현은 별도 축.
- 잠긴 시스템 안에서 장면별 open materiality 후보를 만들고, source·brand·license·safety·accessibility·medium·production 제약으로 선택·거절 근거를 판단한다.
- 인지작업·독자상황·의미적합·claim 강도 판단.
- 어떤 제작·검증 용어를 실제 학습 개념으로 가르칠지, 독자용 언어로 어떻게 번역할지, 공개 표면에서 제외할지는 청중·주제·역할 맥락으로 판단한다.
- 본권/워크북 역할의 세부 분량·장 구성·활동 형태, 그리고 적용 가능한 표준 기능의 우선순위와 비적용 사유를 판단한다.
- 어떤 색/간격 토큰을 어떤 컴포넌트에, 시각 계층 우선순위.
- 이미지 생성을 쓸지 고밀도 SVG로 충분한지.
- 반복 리뷰 코멘트가 재사용 패턴인지 일회성 취향인지.
- CONDITIONAL 보완 우선순위.
- 이 bounded judgment는 validator·label-masked·format 증거보다 하위다.

---

## Conflict Resolution

충돌 시 우선순위:
1. 사용자의 최신 명시 요구 + 파괴적 작업 경계
2. 프로젝트 `AGENTS.md` / workspace SoT
3. 본 `SKILL.md`
4. 번들 `references/`
5. 대상 산출물 역할·청중 / 소스 증거·라이선스 / 네이티브 도구·릴리즈 제약
6. 일반 스타일 취향

**스킬 우선 예외(하위 문서 침범 불가)**: `name`/`description`/metadata·포맷 계약, token namespace 단일 규칙, 두 시스템 혼용 금지, label-masked 완료 금지, PPTX rebuild-stale 규칙. 하위 우선 항목은 deferred/`blocked`/target-specific으로 기록하고 조용히 섞지 않는다.

---

## 3-Layer Classification (Fixed / Flexible / Decisional)

| 층 | 위치 | 예시 |
|---|---|---|
| **Fixed** (실행 가능) | 스키마·validator·계산 코드·status enum | 순서/필수 필드, scene/localization 상태, design-system lock id, bounds/overlap/alignment/spacing/connector/object-density 계산, evidence state, 번역·재빌드 stale 규칙 |
| **Flexible** (맥락 생성) | 프로젝트 SoT·references·후보/수정안 | 콘텐츠 전략, 장면 연출, 구체 문구, 실제 theme/color/font 값, 열린 시각 재료 후보, 의미 그룹과 목표 간격, native/image 조합 |
| **Decisional** (판정) | fixed 관찰 + content-fit 판단 + 사람/렌더 증거 | `pass_local`, `revise`, `blocked`, `needs_human_choice`; preserve/transfer/discard, materiality/route 후보 선택, 보완 우선순위 |

**Drift 방지**: 문서에 “계산한다”고 적은 것만으로 Fixed로 분류하지 않는다. 계산은 실행 코드와 재현 가능한 입력/출력을 가져야 한다. 프로젝트별 임계값·실제 hex·의미 그룹은 Flexible에 두되 status vocabulary와 evidence state는 Fixed에 둔다. Decisional은 어떤 fixed 관찰과 content-fit 판단을 썼는지 trace를 남긴다.
**Snapshot note**: 프로젝트의 현재 PASS/FAIL/blocked 상태와 실제 수치는 이 스킬 본문이 아니라 해당 프로젝트 SoT와 최신 검증 로그에서 읽는다.
Phase별 세부 판단 기준은 defined in `references/design-systems.md`, `references/review-gate.md`, `references/slide-authoring.md`, `references/checklist.md`.

---

## Fixed–Flexible–Decision Visual Support Convergence Pattern

장형·다섹션 산출물에서 시각적 지원 편차를 줄이거나 같은 실수의 재발을 막으라는 요청이 있으면 `references/fixed-flexible-decision-visual-convergence.md`를 사용한다. 층 분류는 Fixed/Flexible/Decision으로 유지하되 실행 순서는 `Decision premise → Flexible exploration → Fixed realization/audit → Decision close → learning update`다.

패턴이 활성화되면 현재 가장 약한 장면과 의미를 가장 잘 지원한 장면을 고르고, 강한 장면의 색·카드·배치가 아니라 `관계 → visible cue → 독자 추론/행동 → 전이 조건`을 추출한다. 그 원리를 약한 장면과 관계가 다른 두 번째 장면에 각각 맞게 전이하고 최소 5회 반복한다. 편차 감소는 모양의 평준화가 아니라 `support_floor`를 끌어올리면서 관계별 실루엣 차이를 보존하는 것이다.

코드는 선언된 object relation, bounds, overlap, spacing, connector, hash, native coverage를 검증한다. content-fit, improved-variant, 사람 이해를 판정하지 않는다. 각 회차는 Fixed rule, Flexible evidence path, Decision status와 pattern guard를 ledger에 남긴다. 같은 실패가 강화된 written gate 뒤에도 재발하면 executable stop condition으로 승격한다.

## LLM + VLPP Improvement Contract

VLPP와 LLM의 통합 결과는 산출물의 합격 등급이나 독자 성과 판정이 아니라 **다음 개선 행동을 고르는 보조 체계**다.

| 층 | 책임 | 기록 |
|---|---|---|
| VLPP / 결정적 계산 | 목표 표현 벡터와 후보 렌더의 거리, 선언한 구조·형식 상태 관찰 | metric, input version/hash, distance, evidence state |
| LLM / 전문 판단 | 독자 과제·관계·맥락을 기준으로 거리의 의미를 해석하고 개선 가설을 제안 | diagnosis, alternatives, constraints, uncertainty |
| 통합 decision | `retain`, `revise`, `needs_human_review`, `blocked` 중 다음 행동 선택 | chosen action, rationale, expected verification surface |

단일 합성 점수로 `전문적`, `이해됨`, `개선 완료`, `학습 성과`를 선언하지 않는다. 거리가 줄어든 것은 목표 표현에 가까워졌다는 계산 관찰일 뿐이며, 개선 여부는 현재 콘텐츠·독자 과제·접근성·브랜드·렌더·사람 증거와 함께 다시 판단한다. 모든 개선 회차는 `target_expression`, `candidate_expression`, `VLPP observation`, `LLM diagnosis`, `next action`, `verification result`를 ledger에 남긴다. VLPP 계산 코드와 schema owner는 `vector-language-cognition`; 본 스킬은 그 출력을 시각 저작의 개선 루프에만 연결한다.

---

## Legacy Package Distillation Gate

본 스킬은 5개 스킬을 흡수한 정본이다. owner split과 흡수 라벨:

| 소스 | 라벨 | 처리 |
|---|---|---|
| `document-slide-authoring-agent-system` | `merge` | Phase 1 저작 계약 + `scripts/portable_agent_system.js` 이관, references 이관 |
| `ggaca-authoring` | `merge` | Phase 0 흡수 사이클(R1~R6/M0~M8/5카운트)로 이관, `references/absorption-cycle.md` |
| `universal-visual-vlc` | `merge` + `route` | Phase 2 리뷰 게이트로 이관. 프로젝트 소유 VLC CLI가 있으면 project config로 route |
| `visual-implementation` | `merge` | Phase 4 Mode L/A로 이관, tokens/section/motion/checklist references 이관 |
| `geo-carbon-visual-integrator` | `merge` | Phase 4 Mode V + label-masked/scene-layer로 이관, `references/visual-semantic-encoding.md` |

원본 5개 SKILL.md는 provenance 스냅샷으로 `_absorbed/`에 read-only 보존(스킬로 노출 안 됨). 5개 옛 이름을 참조하던 다른 스킬은 `visual-authoring`로 갱신했다(sweep 로그는 검증 증거 참조). CLI 도구·외부 SoT 문서는 원위치 유지(route). 한 화면 안에 두 토큰 시스템을 부활시키지 않는다.

검증 경계: `_absorbed/` 아래 파일은 active runtime skill이 아니라 보존 증거다. 이 하위 스냅샷에 `agents/openai.yaml` 또는 현재 형식의 `Rubric (Must/Should)`가 없어도 직접 보강하지 않는다. active 검증과 라우팅은 이 `visual-authoring/SKILL.md`와 references/scripts에서 수행하고, 스냅샷 누락은 `read_only_provenance_exempt`로 기록한다.

---

## Runtime Compatibility Gate

Closure state: **`runtime-delta implemented`**.

- Shared portable core: Markdown 파이프라인·게이트·토큰 references·Python/Node 스크립트는 어느 shared skill root에서도 상대 경로로 사용한다.
- 번들 adapter: scripts/visual-authoring-runtime(Windows: `.cmd`)이 Python 3.9+를 탐색하고, 없으면 OS 패키지 관리자로 설치를 시도한다. 그 뒤 scripts/portable_visual_runtime.py가 image converter와 Chromium 계열 browser를 탐색해 image conversion·web capture·DOM text assertion을 실행한다. 외부 실행 파일이 없으면 `bootstrap` 또는 원래 작업 안에서 알려진 OS 패키지 관리자로 설치를 시도하고, 재탐색 뒤 원래 작업을 다시 실행한다. 설치 불가·비활성·실패 시에는 `dependency_installation_required`/`unavailable`/`failed`와 사람이 실행할 수 있는 명령을 남긴다. 발견 후 browser 실행이 실패하면 runtime은 안전한 headless profile과 다른 발견 후보를 순차 확인하고, 모두 실패하면 설치 실패로 바꾸지 않고 `browser_runtime_failed`·signal/명령/DOM 기록·manual guidance를 남긴다.
- 런타임 제공 imagegen, PowerPoint native open, VLC CLI는 선택형 보강 기능이다. 이 패키지에는 모델·브라우저 엔진·PowerPoint를 포함하지 않으므로 해당 기능은 사용 가능한 owner/runtime이 없으면 manual fallback 또는 blocked다.

---

## Provider / Provenance vs Output Brand

- `provider_provenance`: 어떤 에이전트·모델·스킬·소스 코퍼스·도구·수동 과정이 산출·검증했는가 → evidence/audit/notes/handoff 표면에만.
- `output_brand`: 독자가 볼 산출물 정체성(강의명·리포트명·클라이언트 패키지) → 산출물 표면.
- 둘을 한 필드로 합치지 않는다. 프로젝트가 provider를 고정했다고 그것을 전역 브랜드 기본값으로 승격하지 않는다. 브랜드가 불명확하면 clarification packet에 잠근다.

---

## Runtime Adaptation Default

Shared portable core 하나를 유지하고 Codex/Claude/Gemini 차이는 runtime-adaptation surface로만 표현(호출 문구, 로컬 명령명, UI handoff). 고정 게이트·릴리즈 경계·소스 역할·artifact surface 역할은 version bump + routing 실험 없이 바꾸지 않는다. ordinary skill 전체를 fork하지 않는다.

---

## Setup / Dependencies / Permissions

- **Setup**: 지원되는 shared skill root에 설치 후 `visual-authoring`로 활성화한다. Python이 확실하지 않으면 먼저 `scripts/visual-authoring-runtime probe`를 실행한다. launcher는 Python 3.9+가 없을 때 macOS Homebrew, Linux의 apt/dnf/yum/pacman/apk, Windows winget을 이용해 자동 설치를 시도한다. `VISUAL_AUTHORING_AUTO_INSTALL_PYTHON=0`이면 설치하지 않고 blocked JSON을 반환한다. browser와 converter는 `scripts/visual-authoring-runtime bootstrap` 또는 실제 `capture-web`/`convert-image` 요청에서 자동 설치·재탐색·재시도를 수행한다. `probe`는 발견값만 보므로 capture pass를 뜻하지 않으며, 실행 실패는 `browser_runtime_failed`로 별도 기록한다.
- **Dependencies**: 기본 validator와 portable runtime은 Python 3.9+ 표준 라이브러리만 쓴다. launcher 자체는 POSIX shell 또는 Windows cmd로 동작한다. Mode S scaffold는 Node.js. image conversion에는 ImageMagick·librsvg·Inkscape 중 하나, web capture에는 Chromium 계열 browser가 필요하다. portable_visual_runtime.py는 `probe`로 발견 여부를 보이고, 필요하면 macOS Homebrew, Linux apt/dnf/yum/pacman/apk, Windows winget으로 설치를 시도한다. `VISUAL_AUTHORING_AUTO_INSTALL_TOOLS=0` 또는 명령별 `--no-auto-install`은 설치 대신 명령과 이유만 반환한다. 발견된 browser가 실제 capture를 못 끝내면 runtime은 안전 profile·발견 후보 기록과 `browser_runtime_failed`를 남기며 host URL 정책을 우회하지 않는다. 이미지 생성은 선택형 imagegen owner다.
- **Credentials**: 번들 계약은 외부 credential 불요. 이미지 모델 사용 시 해당 owner가 소유.
- **Write boundary**: 사용자가 명시 요청할 때만 대상 프로젝트/산출물에 쓴다. Mode S scaffold는 기본적으로 기존 파일 미덮어씀(`--force` 명시 시만). 정본·외부 원본(Phase 0) 수정 0건. 파괴적 삭제 없음.
- **Network**: 기본 불요. 다만 Python·browser·converter 자동 설치가 필요한 경우 패키지 관리자와 네트워크를 사용하며, OS 권한 상승 또는 패키지 관리자 동의를 요구할 수 있다. Linux 자동 설치는 보이지 않는 비밀번호 입력을 기다리지 않도록 `sudo -n`만 시도하고, 권한이 없으면 상호작용 터미널의 `sudo` 명령 또는 관리자/root shell용 명령을 남긴다. 임의 URL에서 실행 파일을 내려받지는 않는다.

---

## Source and License Notes

- 흡수 원형: `document-slide-authoring-agent-system`, `ggaca-authoring`(원형 2026-05 의도적 수익 체계론×fitCrafting 통합 사이클), `universal-visual-vlc`, `visual-implementation`(frontend-skill+frontend-carbon 후속), `geo-carbon-visual-integrator`. 스냅샷은 `_absorbed/`.
- 대상 프로젝트·산출물은 자체 product/domain SoT를 유지한다. 본 스킬은 시각 저작 파이프라인·라우팅·검증 계약만 소유.
- 하위 프로젝트가 더 엄격한 라이선스·콘텐츠·권한 규칙을 가지면 그 표면이 본 계약보다 우선.

---

## References

| 파일 | 로드 시점 |
|---|---|
| `references/glossary.md` | 용어 확인 |
| `references/concept-map.md` | 정보 관계·Markdown 문서 토폴로지·검증 경로 확인 |
| `references/source-first-regeneration.md` | 원본 기반 재생성/이관, source parity, 편집 가능성 판단 |
| `references/pptx-native-object-authoring.md` | PPTX native object intent, geometry relations, semantic coverage, threshold/waiver/evidence 경계 |
| `references/pptx-native-conformance-and-self-remediation.md` | PowerPoint 기능별 intentional status, Pretendard theme, outline/automatic slide number/text alignment/raster exception, source-level self-remediation |
| `references/pptx-native-runtime-evidence.md` | exact candidate hash의 fresh PowerPoint observation, partial first-open 상태, full review/edit round-trip receipt, no-automation boundary |
| `references/pptx-standard-xml-generation.md` | PPTX OPC/PresentationML 생성 규칙과 fresh-open 검증 경계 |
| `references/pptx-pattern-compiler-and-evidence-separation.md` | fresh PPTX pattern family, no-repair lineage, Fixed/Flexible/Decision ownership, four proof ledgers |
| `references/absorption-cycle.md` | Phase 0 (GGACA 상세 게이트·카운트·충돌 카드) |
| `references/slide-authoring.md` | Phase 1 (인지 저작 패킷·순서·PPTX 게이트·npm route) |
| `references/course-flow-to-design-system-sequence.md` | Phase 1에서 course flow를 디자인 시작 경계로 연결 |
| `references/slide-authoring-methods.md` | 저작 방법·증거 계층·gate test 보조 계약 |
| `references/cognitive-authoring-process.md` | 범용 저작 전략 루프, 3층 전략 ledger, 표현군 prototype, 저작/장애 대응 루프 분리 |
| `references/cognitive-slide-quality-factors.md` | 기존 PPTX 전체 비교, 인지 요인 코드북, 구조 분포/PCA와 render review의 분리 |
| `references/fixed-flexible-decision-visual-convergence.md` | 가장 약한/강한 장면 비교, 지원 원리 전이, 최소 5회 수렴, 반복 실수 방지 ledger |
| `references/prototype-authorization-contract.md` | 반복 순서 이탈을 막는 표현군 prototype 실행형 승인 계약 |
| `references/review-gate.md` | Phase 2 (route_status·claim 경계·image-required·CLI) |
| `references/review-packet.md` | 모든 경로의 scene-first review packet과 evidence/claim 구조 |
| `references/image-required-route-gate.md` | SVG/image/hybrid route 상태와 실패 종료 조건 |
| `references/visual-gate-conditions.md` | 보조 진입·탈출 gate 조건 |
| `references/visual-rubric-design.md` | 시각 결과 Must와 과정 Should 보조 루브릭 |
| `references/design-systems.md` | Phase 3 (기본값 없는 Visual Strategy & System Select 루브릭) |
| `references/semantic-staging-design-framework.md` | Phase 3 (artifact-level system lock·열린 시각 재료·장면 중심 의미 연출) |
| `references/tokens-carbon.md` | Phase 3/4 (Carbon `--cds-*` 토큰) |
| `references/tokens-vivid.md` | Phase 3/4 (Vivid `--viv-*` 토큰) |
| `references/section-patterns.md` | Phase 4 (섹션 패턴) |
| `references/motion-recipes.md` | Phase 4 (모션 레시피) |
| `references/landing-page-template.html` | Mode L 구현 출발점(선택한 전략·토큰을 물질화할 때) |
| `references/visual-normalization-process.md` | 기존 시각 산출물의 R→P→M→W→A 정규화 과정 |
| `references/visual-semantic-encoding.md` | Phase 4 Mode V (label-masked·의미 단위표) |
| `references/publication-surfaces.md` | 교재/워크북/배포 PDF·HTML·EPUB의 공개 표면, 역할 분리, 표준 profile, 인증 주장 경계 |
| `references/checklist.md` | Phase 5 (검증 체크리스트) |
| `references/user-decision-and-feedback.md` | 목적·원본 처리·전략/색상 preview·저자 표기·향후 리커트 피드백을 사용자에게 요청할 때 |
| `references/tool-runtime-implementation.md` | imagegen·renderer·인앱 브라우저를 실제 코드/도구 어댑터와 evidence path로 묶을 때 |
| `references/session-feedback-and-surface-gates.md` | 실제 세션 피드백을 다음 gate와 분리 증거 표면으로 환류 |
| `references/retrospective-design-system-default-bias-20260709.md` | Phase 5/회고 학습 (기본값 편향·장면 구체성·네이티브 기능 보강 근거) |
| `references/retrospective-strategy-sequencing-20260710.md` | Phase 5/회고 학습 (N=2 전략 순서·prototype/native-open 조기 게이트 근거) |
| `references/retrospective-calmness-silhouette-diversity-20260710.md` | Phase 3/5 회고 학습 (차분함과 실루엣 반복의 잘못된 등치, N=1 가설) |
| `references/retrospective-cognitive-visual-encoding-20260711.md` | Phase 3/5 회고 학습 (관계→추론 목표→시각 문법 선택과 사람 검증 경계) |
| `references/retrospective-fixed-system-open-materiality-localization-reflow-20260713.md` | Phase 3/4/5 회고 학습 (고정 시스템·열린 장면 재료 N=2, 번역 reflow N=1) |
| `references/source-notes.md` | provenance·라이선스 경계 |
| `scripts/portable_agent_system.js` | Mode S scaffold/check |
| `scripts/audit_pptx_native_objects.py` | PPTX 객체/bbox/relation/coverage 결정적 감사 |
| `scripts/validate_pptx_native_conformance.py` | PPTX native convention audit와 PPTX를 수정하지 않는 source-level repair plan 생성 |
| `scripts/validate_pptx_native_runtime_receipt.py` | exact candidate PowerPoint observation을 receipt status로 결정적으로 계산하고 PPTX/UI를 변경하지 않음 |
| `scripts/validate_pptx_pattern_compiler_manifest.py` | 새 PPTX family의 16:9/pattern route/recovery-lineage/evidence separation 결정적 검사 |
| `scripts/validate_authoring_prototype_gate.py` | 표현군 검토·format gate·전체 확장 승인 일관성 검증 |
| `scripts/validate_visual_silhouette_budget.py` | 관계 유형·실루엣 가족·연속 반복·지배 비율·의미 시각화 비율 검사 |
| `scripts/validate_publication_surface_contract.py` | reader_public 용어 차단, 본권/워크북 역할 marker, 표준 profile·인증 주장 상태의 결정적 검사 |
| `scripts/validate_scene_materiality_reflow_contract.py` | artifact-level system lock, 모든 경로의 scene-first packet, localization/reflow proof freshness 검사 |
| `scripts/analyze_slide_quality_factors.py` | read-only PPTX 구조 관찰, 인지 코드북 결합, 비교 분포와 descriptive PCA 산출 |
| 프로젝트 소유 `surface_vlc_gate` 호환 CLI | Phase 2 선택형 로컬 어댑터(있을 때) |

---

## Rubric (Must / Should)

### Must
- 스킬 목적·사용 시점이 본문과 일치한다. — Evidence: `name`/`description`/Trigger Contract/Phase 순서 무충돌.
- 요청마다 밟은/건너뛴 Phase를 명시한다. — Evidence: 응답에 Phase skip 사유.
- `Working Source of Truth and Clarification Intake` 섹션 존재, user 자료를 정본으로 잠그고 미확정은 TODO/blocked로. — Evidence: 본문 grep + packet 필드.
- `Source-First Sequential Action Plan` 섹션 존재, 원본 artifact의 역할을 먼저 분류한다. fidelity baseline만 source parity를 강제하고 reference benchmark는 content-fit observation으로 닫는다. — Evidence: source role packet + 역할별 proof.
- `Content-Fit Quality Hierarchy`를 기준으로 시각 전략·선택형 표현 시스템·매체 구현을 분리하고, Carbon/Vivid/Brand를 시각화나 native medium과 혼동하지 않는다. — Evidence: `references/design-systems.md` + 3축 선택 기록.
- `Publication Surface Contract`가 공개 독자·진행/편집·제작/검증 표면을 분리하고, 내부 제작 언어를 표지·hero·목차·상태 문구에 노출하지 않는다. — Evidence: audience surface policy + public scan + `references/publication-surfaces.md`.
- Mode B는 본권과 워크북의 역할을 분리한다. 본권은 개념·원리·사례·판단 기준을, 워크북은 적용 활동과 본권 연결을 제공한다. — Evidence: artifact role map + 각 artifact의 목차/marker + `validate_publication_surface_contract.py`.
- 배포 포맷은 적용 가능한 표준 기능을 의도적으로 사용하거나 비적용 사유를 기록하고, 인증 주장과 기능 사용을 분리한다. — Evidence: format standard profile + format/native validation report; PDF/A·PDF/UA 주장은 전용 증거가 있을 때만.
- Phase 3에서 실제로 열려 있는 축의 `Design Exploration Gate`를 통과하고, 선택/거절 근거와 no-default를 기록한다. 웹/CSS는 token namespace를, PPTX는 theme/style materialization을 감사한다. — Evidence: 3축 packet + style proof.
- Phase 2 claim 3분리(`observable_proxy`/`inferred_risk`/`human_outcome_claim`)와 route_status enum 유지, SVG_PROXY_ONLY/BLOCKED는 pass로 닫지 않음. — Evidence: `references/review-gate.md` + Output Contract.
- `Scene Specificity Gate`가 생성 이미지/하이브리드 경로에서 구체 인물·공간·사물·행동·통합 계획을 확인한다. — Evidence: `references/review-gate.md` + prompt ledger.
- label-masked 판독 미통과 시 완료 금지, 사람 실측 전 human-outcome 확정 금지. — Evidence: Phase 4/5 + checklist.
- 생성 이미지 사용 시 prompt ledger(model/prompt/output_path/integration_path/verification) 존재. — Evidence: 산출물/검증 로그 grep.
- `PowerPoint Native Object Intent / Geometry / Semantic Coverage Contract` 섹션 존재. Mode S는 intent plan과 exact PPTX hash의 audit, critical exact-zero blocker, critical/relation coverage를 닫고 geometry proxy를 quality/human proof로 승격하지 않는다. — Evidence: intent/audit JSON + `references/pptx-native-object-authoring.md`.
- `PowerPoint Native Conformance and Source-Level Self-Remediation Gate` 섹션 존재. Mode S는 모든 core PowerPoint capability를 intentional status와 reason으로 닫고, Pretendard theme font, native title/section/TOC/automatic slide number, named text-alignment exception, raster exception을 exact PPTX에서 검사한다. 위반 시 report와 fresh-source repair plan만 만들며 recovery/normalized/conversion/UI-resave artifact를 source로 쓰지 않는다. — Evidence: `pptx-native-conformance-contract.json`, exact candidate report/repair-plan, `references/pptx-native-conformance-and-self-remediation.md`, `scripts/validate_pptx_native_conformance.py`.
- `PPTX Native Runtime Receipt Gate` 섹션 존재. exact candidate hash, fresh PowerPoint process, recovery dialog 부재, ordered full-slide review, gate에 이름으로 지정한 editable object의 save/reopen round-trip을 별도 observation으로 기록하고 receipt validator만 status를 계산한다. `pass_native_first_open_pending_release`는 release pass가 아니며, recovery/hash mismatch/recorded round-trip 실패는 source-level fresh-family remediation으로 이어진다. — Evidence: `*.powerpoint-native-gate.json`, observation JSON, `references/pptx-native-runtime-evidence.md`, `scripts/validate_pptx_native_runtime_receipt.py`.
- Mode S는 outline notes 선행 + `Native Medium Capability Scan` + fresh PPTX open check를 rebuild-stale 규칙과 함께 별도 게이트로. — Evidence: `references/slide-authoring.md`.
- `PPTX Pattern Compiler and Evidence-Separation Gate`가 존재한다. 복구·normalized·conversion·UI-resave PPTX는 후속 후보의 source family가 될 수 없고, fresh manifest가 pattern route와 recovery-lineage 거절을 검사한다. 구조·읽기·보기·native runtime 증거는 네 장부로 분리한다. — Evidence: `references/pptx-pattern-compiler-and-evidence-separation.md` + `scripts/validate_pptx_pattern_compiler_manifest.py`.
- `PPTX Code-Pattern and Reader-Admission Gate`가 존재한다. LLM은 선언형 장면·문구·선택 이유만 제안하고 Fixed 코드가 renderer·native object·OOXML·pre-emit gate·파일 쓰기를 소유한다. scene pattern과 code route는 1:1로 결속되고 reader-public 문구는 공용 gateway에서 fail-closed 검사된다. — Evidence: `references/pptx-code-pattern-admission.md` + `references/pptx-code-pattern-admission.capability.json` + `scripts/validate_pptx_code_pattern_catalog.py` + `scripts/reader_surface_admission.mjs`.
- Phase 0(GGACA) 진입 시 R1~R6 상속 + forbidden 어휘 본문 0 + 정본·외부 원본 무수정 증명. — Evidence: `references/absorption-cycle.md` + 5카운트.
- `Conflict Resolution` 섹션 존재(우선순위 + 스킬 우선 예외). — Evidence: 본문 grep.
- `3-Layer Classification` + Drift 방지 존재(live 수치 references 위임). — Evidence: 본문 grep + Flexible pointer.
- `Legacy Package Distillation Gate` 존재, 5개 소스를 merge/route 라벨 + owner split으로 기록, `_absorbed/` provenance 보존. — Evidence: 본문 grep + `_absorbed/` 존재.
- `_absorbed/` read-only provenance는 active validation 대상에서 제외하고 `read_only_provenance_exempt`로 기록한다. — Evidence: Legacy Package Distillation Gate의 검증 경계.
- `Runtime Compatibility Gate` 존재, 현재 runtime 한계와 자동 설치·재탐색·재시도 경계를 하나의 closure state로 기록하고, 외부 CLI는 project config로만 연결한다. — Evidence: 본문 grep + `scripts/visual-authoring-runtime self-test` + `scripts/portable_visual_runtime.py probe`.
- `Provider / Provenance vs Output Brand` 존재, 둘 분리, 프로젝트 fallback을 전역 브랜드로 승격 금지. — Evidence: 본문 grep.
- 5개 옛 이름 inbound 참조가 `visual-authoring`로 갱신되거나 alias로 닫힘. — Evidence: sweep grep 결과 로그.
- `Retrospective Signal Gate`가 반복 리뷰 신호를 기본값 편향·장면 불명확·네이티브 기능 누락 중 하나로 분류하고 다음 산출물 게이트에 반영한다. — Evidence: `references/checklist.md` + 회고 reference.
- `Universal Authoring Strategy Loop`와 `Authoring Loop vs Incident-Response Loop`를 유지한다. 전체 제작 전 표현군별 prototype을 실행형 승인 게이트로 통과시키고, 국소 진단을 저작·평가 방법으로 승격하지 않는다. — Evidence: `references/cognitive-authoring-process.md` + `references/prototype-authorization-contract.md` + V18/S15/S16 + N=3 회고.
- `Semantic Silhouette Diversity Gate`가 존재하고 `차분함`을 낮은 표현 강도로만 해석하며 관계 구조의 다양성을 축소하지 않는다. 장형/다섹션 덱은 프로젝트별 policy가 있는 `visual-silhouette-manifest.json`을 만들고 실행형 validator를 통과한다. — Evidence: `references/design-systems.md` + `references/checklist.md` V19/S17 + `scripts/validate_visual_silhouette_budget.py`.
- `Cognitive Visual Encoding Gate`가 존재하고 관계→추론 목표→후보 문법→선택 근거→가시/억제 cue→읽기 경로를 기록한다. 새 장형/다섹션 덱은 schema v2 validator를 통과하고, `vector-language-cognition`의 evidence state와 사람 검증 경계를 임의로 재정의하지 않는다. — Evidence: `references/design-systems.md` + `references/checklist.md` V20/S18 + `scripts/validate_visual_silhouette_budget.py --require-cognitive-encoding`.
- `Fixed Design System / Open Visual Materiality / Scene-Centered Meaning Contract`가 존재한다. artifact-level system lock은 스타일 문법을 고정하되 반복 레이아웃을 강제하지 않고, 모든 이미지/SVG/native 경로의 주요 의미 단위는 open-set materiality 후보와 scene-first packet을 남긴다. — Evidence: `references/design-systems.md` + `references/review-packet.md` + `scripts/validate_scene_materiality_reflow_contract.py`.
- `코퍼스 기반 에세이 문법 모듈`은 특정 저자 코퍼스나 경계가 명시된 대화 코퍼스를 플랫폼 공식 문법으로 바꾸지 않고, 최소 세 표본의 관찰·이식·폐기 결정을 분리한다. 대화 표본은 여섯 이론 렌즈를 제한된 해석으로만 기록한다. — Evidence: `references/author-corpus-essay-grammar.md` + `scripts/validate_essay_grammar_packet.py` + 유효/플랫폼-주장 결함 fixture.
- `User Decision, Comparative Preview, and Progress Gate`가 목적 확인, 원본 계속/새 시작, imagegen+전체 표면 후보 비교, HCI 색상 비교, 릴리즈 저자 표기, 현재 OFF인 사람 피드백 문항을 분리한다. — Evidence: `references/user-decision-and-feedback.md` + `scripts/validate_visual_authoring_decision_packet.py` + 유효/우회 fixture.
- `Tool Runtime Implementation Gate`가 필요한 기능을 실행 가능한 code/tool adapter와 evidence path로 묶는다. HTML/web UI는 코드 렌더와 portable browser adapter의 전체 화면·DOM/상태 증거를 함께 남긴다. Python이 없으면 launcher의 자동 설치 시도 또는 blocked JSON을 남긴다. browser·converter가 없으면 adapter가 known package manager 설치→재탐색→작업 재시도를 수행하고, 불가·비활성·실패 시 `dependency_installation_*` 명령 안내를 남긴다. 발견된 browser 실행 실패는 `browser_runtime_failed`의 profile/candidate/signal 기록으로 분리하고 host URL 정책은 우회하지 않는다. — Evidence: `references/tool-runtime-implementation.md` + `scripts/visual-authoring-runtime self-test` + decision packet validator + 유효/도구-우회 fixture.
- `Concrete-Language / Localization Reflow Gate`가 존재한다. 한국어 문장 판단은 `korean`, 시각 물질화와 proof freshness는 본 스킬이 소유하며, 번역·구체화 뒤 pending 상태와 stale proof를 fresh reflow evidence 없이 닫지 않는다. — Evidence: localization reflow packet + validator + fresh target-medium proof.
- `Fixed–Flexible–Decision Visual Support Convergence Pattern`이 존재한다. 패턴 활성화 시 현재 weak/strong scene, 표면이 아닌 지원 원리, primary/secondary transfer, 최소 5회 ledger, Fixed audit와 content-fit/human evidence 분리, 재발 pattern guard를 남긴다. — Evidence: `references/fixed-flexible-decision-visual-convergence.md` + `references/checklist.md` V21/S19 + cycle ledger.
- `LLM + VLPP Improvement Contract`가 존재하고, VLPP 계산·LLM 진단·통합 다음 행동을 분리한다. 단일 점수로 품질·이해·학습성과·완료를 선언하지 않는다. — Evidence: target/candidate/metric/diagnosis/next-action ledger + `references/cognitive-authoring-process.md`.
- 출력은 `결론 + 근거 + 다음 행동` 1세트로 닫는다. — Evidence: 마감 보고 절제.

### Should
- 긴 자료는 `references/`로, 반복 코드는 `scripts/`로 분리(본문은 파이프라인 spine).
- 선택 후보군 중 최소 2개 이상에 대해 데스크톱+모바일(375px) 판정 근거 기록, `prefers-reduced-motion` 존중.
- 시각 옵션 리포트는 취향이 아니라 semantic fit·계산 가능한 표현 거리·접근성·레이아웃 tradeoff로 우열을 보이되, 계산값이 콘텐츠 적합성이나 미적 판단을 대체하지 않게 한다.
- PPTX audit는 slide/object별 finding 분포와 geometry heatmap을 제공할 수 있지만, 점수 최적화를 디자인 목표로 삼지 않는다.
- 반복 PowerPoint 복구 이슈·반복 리뷰 코멘트는 패턴 항목·릴리즈 blocker로 격상(조용한 재시도 금지).

---

## Preflight

닫기 전:
1. `generate-skill/scripts/quick_validate.py`와 `generate-skill/scripts/audit_three_layer_separation.py`로 `visual-authoring/` 검증 통과.
2. Source role/Phase 순서/Content-Fit hierarchy/3축 선택/claim 3분리 grep 확인.
3. Visual Strategy & Expression Select 기록(콘텐츠 전략/표현 시스템/매체 구현/선택·거절/no-default) 존재.
4. PPTX 경로는 `scripts/audit_pptx_native_objects.py --self-test`와 실제 deck+intent audit를 실행하고 hash·blocker·coverage 확인.
4a. 새 PPTX family는 `scripts/visual-authoring-runtime run scripts/validate_pptx_pattern_compiler_manifest.py <manifest>`와 `--self-test`를 통과하고, recovery/normalization/conversion lineage가 source family에 없는지 확인한다. static/read/render/native 네 evidence ledger를 별도로 보고한다.
4b. 새 PPTX family는 `pptx-native-conformance-contract.json`을 만들고 `scripts/visual-authoring-runtime run scripts/validate_pptx_native_conformance.py --self-test`와 실제 deck conformance audit를 실행한다. capability status/reason, Pretendard theme, title/section/TOC/automatic slide number, default center/middle shape text, named exceptions, raster exception, source-only repair plan을 확인한다.
4c. PowerPoint native-runtime을 주장하면 `*.powerpoint-native-gate.json`과 별도 observation JSON을 만들고 `scripts/visual-authoring-runtime run scripts/validate_pptx_native_runtime_receipt.py --self-test` 및 exact candidate receipt를 실행한다. first-open only는 `pass_native_first_open_pending_release`로 기록하고, full review/edit round-trip 전에는 release pass로 합치지 않는다. 이 패키지는 PowerPoint UI를 조작하지 않으므로 native action-binding static audit은 해당 구현이 추가될 때만 적용한다.
5. 사용 모드별 증거 분리 보고(computation/content-fit/human/format/native/source-role/surface).
6. 5개 옛 이름 inbound 참조 sweep 결과 첨부. 정본 자기 설명과 `_absorbed/` read-only provenance는 allowlist로 제외하고, active 외부 SKILL inbound만 갱신 대상이다. `_absorbed/` provenance 존재도 함께 확인한다.
7. Runtime/Provider/Conflict/3-Layer/Legacy/Native Object Intent heading 존재 grep.
8. stale conflation phrase grep 0. 단, 금지 예시 자체와 checklist 문구는 allowlist로 제외한다. 대상은 active 실행 지시가 native implementation을 expression candidate로 취급하는 문구, reference-only parity gate, weak-signal default marker를 되살리는 경우다.
9. 장형/다섹션 덱은 `validate_visual_silhouette_budget.py <manifest>` 통과와 expression-family prototype 포함 범위를 확인. 신규/전면 재구성은 `schema_version: 2`와 `--require-cognitive-encoding`을 함께 사용한다.
10. 시각 지원 수렴 패턴을 활성화했다면 최소 5회 cycle ledger, weak/strong scene, primary/secondary transfer, pattern guard, support floor 변화와 증거 표면 분리를 확인한다.
11. 교재/워크북/배포 문서에서는 `publication_surface_contract.json`을 만들고 `scripts/visual-authoring-runtime run scripts/validate_publication_surface_contract.py publication_surface_contract.json --root <project-root>`를 실행한다. 독자 공개 파일은 표지/hero/목차/상태 영역을 정확히 대상으로 잡는다.
12. `artifact_profile: textbook_with_workbook`이면 본권·워크북이 서로 다른 역할을 실제로 수행하는지 렌더·목차·본문 marker로 확인한다. 체크리스트만 많은 파일을 본권으로, 설명만 있는 파일을 워크북으로 보고하지 않는다.
13. PDF/HTML/EPUB profile이 있으면 기능 사용, 비적용 사유, 포맷 검증, 인증 주장 상태를 별도 보고한다. 사람 반응 가설, format pass, 인증, 학습성과를 하나의 점수나 Done 문장으로 합치지 않는다.
14. `scripts/visual-authoring-runtime run scripts/validate_scene_materiality_reflow_contract.py --self-test`를 통과시키고, 실제 제작에서는 artifact-level design-system lock과 모든 주요 의미 단위의 scene-first packet을 검사한다. 시스템 일관성·장면 자유도·route가 서로 모순되지 않는지 확인한다.
15. 번역·자연화·구체화가 있으면 `translated_pending_reflow`/`concretized_pending_reflow`가 0인지, 영향 표면의 stale proof가 fresh geometry/render/native/accessibility proof로 교체됐는지 확인한다.
16. VLPP를 사용했다면 계산 input/version/hash와 distance, LLM diagnosis, 선택한 다음 행동, 재검증 결과를 ledger로 확인한다. VLPP distance 감소만으로 `improved` 또는 reader outcome을 선언하지 않는다.
17. 저자 코퍼스 에세이 문법을 사용했다면 `validate_essay_grammar_packet.py`로 최소 세 표본·상대 경로·플랫폼/사람 성과 비주장을 검사하고, CTA와 열린 끝을 분리했는지 확인한다.
18. 사용자 선택이 필요한 시각 저작이면 `validate_visual_authoring_decision_packet.py`로 목적 확인, 원본 처리 선택, 후보별 imagegen/전체 표면 preview, HCI 색상 비교, 릴리즈 저자 표기, 사람 피드백 OFF/ON 상태를 확인한다.
19. 필요한 기능의 tool/runtime plan이 코드·도구 adapter와 evidence path를 가리키는지 확인한다. HTML/web UI는 portable browser adapter 또는 동등한 runtime browser로 전체 표면 capture와 DOM/상태 확인을 남긴다.

## AGENTS.md Alignment

- host 또는 프로젝트 `AGENTS.md`의 Goal-First, Rubric-Driven, Completion Rule을 따른다.
- 결과는 `결론 + 근거 + 다음 행동` 형식으로 닫는다.
