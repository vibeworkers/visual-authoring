---
name: visual-implementation
description: >
  시각 구현(Visual-Implementation) 통합 스킬. 랜딩/홍보 HTML과 앱 UI(대시보드, 폼, 입력 모달)
  양쪽을 동일 원칙(구성·위계·절제·모션·유틸리티 카피)과 동일 디자인 시스템(Carbon 토큰)으로 빌드한다.
  트리거: "랜딩/홍보 페이지", "marketing page", "강의 상세", "대시보드/앱 UI/폼/모달 구현".
  frontend-skill + frontend-carbon을 합친 후속 스킬.
---

# visual-implementation

**한 문장 정의**: 시각 판단(`visual-judgement-rubric`)에서 합격선이 정해진 화면을 실제 코드로 옮기는 단일 스킬. 랜딩이든 앱 UI든 같은 art-direction 원칙과 같은 Carbon 토큰 시스템을 쓰되, **모드(Mode)** 만 갈라진다.

---

## Trigger

### Mode A — Landing / Promo
- 랜딩, 홍보, marketing page, promo HTML, 강의 상세, 모집/제품 상세
- 기존 랜딩 리디자인
- "영화처럼 몰입", "시네마틱" 흐름 요구

### Mode B — App UI
- 대시보드, 관리/운영 도구, admin
- 입력 폼, 모달, 인스펙터, 설정
- 데이터 테이블, 차트 패널
- "직관적으로 상태 파악 → 행동/판단" 도구

### 트리거되지 않는 경우
- 문서 내보내기 → `carbon-doc-builder`
- PPTX/DOCX/HWPX → `carbon-doc`
- 시각 판단/평가만 → `visual-judgement-rubric`

---

## Working Model (모드 공통)

빌드 전 **3가지 선행 작성**:

1. **Visual Thesis** — 한 문장: 분위기·소재감·에너지
   - Mode A 예: "다크 그라디언트 위 글래스카드, 데이터 권위감"
   - Mode B 예: "calm surface, 라벨/숫자만으로 의미가 통하는 운영 표면"
2. **Content Plan** — 모드별 시퀀스 (아래)
3. **Token Plan** — 사용/확장하는 `--cds-*` 변수 명시

Mode A에서 시네마틱 요구 시 **Cinematic Immersion Plan** 추가:
- 핵심 메시지 / story beat / 시각 인과성 / 주의 경로 / 관점 앵커 / 5초 이해 테스트
- 기준: `/Volumes/Extend/.codex/skills/cognitive-content-rubric/references/cinematic-immersion-rubric.md`
- 5초 테스트 미실시 → 완료 판정 `CONDITIONAL`

---

## Common Principles (모드 공통)

### Composition First
- 컴포넌트 개수가 아니라 **구성·위계·절제·이미지·모션**으로 품질이 결정.
- 한 섹션/뷰 = 하나의 지배적 아이디어.
- 공백·정렬·스케일·크롭·대비를 chrome(테두리/그림자)보다 먼저.
- 시스템 제한: 서체 2종, accent 1종.
- **카드 기본 금지** — 카드 자체가 인터랙션일 때만.

### Typography
- Primary: IBM Plex Sans / Noto Sans KR
- Code: IBM Plex Mono
- Serif: IBM Plex Serif (인용 한정)
- 반응형: `clamp()`

### Carbon Tokens
- 모든 색·간격·반지름·그림자는 `--cds-*` CSS 변수.
- Base: `references/tokens-css.md`의 `:root` 블록 복사.
- 페이지/뷰별 시맨틱 토큰 추가 (`--cds-hero-*`, `--cds-track-*`, `--cds-accent`, `--cds-warning`, `--cds-critical`).
- **금지**: hardcoded hex/px (예외: `clamp()` 내부, media query breakpoint).
- **bx-- 클래스 금지** — 시맨틱 클래스 사용.

### Motion
- CSS-only 우선, 외부 라이브러리 최소 (Mode A에서만 Framer Motion 허용).
- duration ≤ 0.6s, `prefers-reduced-motion` 존중.
- 빠른 녹화에서 인지, 모바일에서 부드러움.
- 레시피: `references/motion-recipes.md`.

---

## Mode A — Landing / Promo

### Sequence
| 순서 | 섹션 | 역할 | 필수 |
|------|------|------|------|
| 1 | Hero | 브랜드·약속·CTA·핵심 수치 | Yes |
| 2 | Support | 하나의 증거/기능/패러다임 전환 | Yes |
| 3 | Detail | 비교·커리큘럼·워크플로 | Yes |
| 4 | Social Proof / FAQ | 증거·이의 처리 | Optional |
| 5 | Final CTA | 전환 | Yes |

### Hero Rules
- **Full-bleed**: 섹션에 `max-width` 없음, 내부 `.container`만 1120px.
- 브랜드 > 헤드라인 > 본문 > CTA 순으로 큼.
- `--cds-hero-start/mid/end` 그라디언트 토큰화.
- 글래스모피즘: `backdrop-filter: blur()` + `--cds-glass-bg/border`.
- 첫 뷰포트에 맞춤 (고정 헤더 시 `calc(100svh - header-height)`).
- 기본 금지: hero cards, stat strips, logo clouds, pill soup, floating dashboards.
- 첫 화면에서 이미지를 빼도 작동하면 이미지가 약함. 네비를 가렸을 때 브랜드가 사라지면 위계가 약함.

### Imagery
- 실사 우선, 추상 그라디언트/가짜 3D는 보조.
- 텍스트가 앉을 안정 톤 영역 가진 이미지.
- 박힌 로고/UI 프레임/패널 금지.
- 콜라주 1장보다 여러 장.

### Marketing Copy
- 헤드라인이 의미 운반, 보조 카피는 한 문장.
- 섹션 간 반복 제거. 30% 잘라도 좋아지면 더.

### Motion (Mode A)
필수 2개 이상:
- Hero 진입 시퀀스 (fadeInUp 순차)
- Scroll-linked / sticky / depth 1개
- Hover/reveal 1개

---

## Mode B — App UI

### Surface Hierarchy
- Linear-style 절제: calm surface, 강한 타이포·간격, 적은 색.
- 4 영역: **primary workspace / navigation / secondary context (inspector) / one accent**.
- 카드 모자이크 대시보드 금지 — 평면 레이아웃 + 구분선·여백·정렬.
- 운영 표면에 hero/캠페인 카피 금지.

### Utility Copy
- 약속/무드/브랜드 보이스 < **방향감·상태·행동**.
- 시작은 작업 표면 자체: KPI, 차트, 필터, 테이블, 상태, 마지막 동기화.
- 섹션 헤딩 = 그 영역이 무엇이고 거기서 무엇을 할 수 있는가.
- 좋음: "Selected KPIs", "Plan status", "Top segments", "Last sync".
- 보조 텍스트는 범위·동작·신선도·결정 가치를 한 문장.
- 홈페이지 hero에 들어갈 법한 문장이면 다시 쓴다.
- **Litmus**: 운영자가 헤딩·라벨·숫자만 훑어도 페이지를 즉시 이해할 수 있어야 한다.

### Form / Modal Patterns (Mode B 특화)
**핵심 원칙**: 입력 단계도 "힌트만 준다" — 지시·심문이 아니다.

필수 패턴:
- **Sensible defaults** — 99% 케이스 기본값 (날짜=오늘, 상태=planned 등).
- **Shared schema validation** — 서버 스키마(예: Zod)를 클라가 재사용해 서버 도달 전 차단.
- **Error Translation Layer** — 서버 raw error(JSON/스택) UI 누출 금지. `field → 한국어 메시지` 변환기 1곳.
- **Field-local error** — 에러는 발생 필드 아래 inline. 모달 전체 빨강 금지.
- **Progressive disclosure** — 조건부 필드(예: transfer → counterparty)는 필요할 때만 등장.
- **Input formatting** — 표시(`300,000원`)와 저장(정수) 분리.
- **Live preview / what-if** — 입력 중 결과 미리보기 (잔고 영향, minSafe 위반 등).
- **Required vs optional grouping** — 선택 필드는 "추가 옵션" 토글 안으로.
- **Severity tiering** — error는 차단, warning은 통과시키되 노출.
- **Idempotent submit** — 제출 중 버튼 disable.
- **Optimistic UI** (선택) — 즉시 반영 + 실패 시 롤백.

### Motion (Mode B)
- 절제: 모달 등장/퇴장, 패널 슬라이드, 상태 점멸 정도.
- 장식 모션 금지. 위계나 affordance를 강화하지 않으면 제거.

---

## Hard Rules (모드 공통)

- No cards by default.
- No hero cards / stat strips / logo clouds (Mode A).
- No card-mosaic dashboards (Mode B).
- No `bx--` Carbon 컴포넌트 클래스.
- No hardcoded hex/px for color/spacing/radius.
- No CDN dependencies (Google Fonts만 예외, Mode A).
- No external CSS/JS 참조 (Mode A self-contained 단일 파일).
- No 2개 초과 서체.
- No 1개 초과 accent (트랙 구분 제외).
- No 1개 초과 dominant idea per section.
- No filler copy / no design commentary in UI.
- No raw server error JSON in UI (Mode B).
- No required-form submission without sensible defaults / inline validation (Mode B).

---

## Reject These Failures

### Mode A
- Generic SaaS card grid as first impression
- Beautiful image, weak brand presence
- Strong headline, no clear action
- Busy imagery behind text
- Mood-statement repetition across sections
- Carousel without narrative

### Mode B
- Stacked cards substituting for layout
- Decorative gradients behind routine product UI
- Multiple competing accent colors
- Ornamental icons that don't aid scanning
- Marketing hero on operational surface
- Raw error payload shown to user
- Empty submit hitting server before client validation

---

## Litmus Checks

### Mode A
- 첫 화면에서 브랜드/제품이 명확한가?
- 강한 시각 앵커가 하나 있는가?
- 헤드라인만 훑어 페이지를 이해할 수 있는가?
- 각 섹션의 일이 하나인가?
- 카드가 정말 필요한가?
- 모션이 위계/분위기를 개선하는가?
- 장식 그림자를 다 빼도 프리미엄으로 느껴지는가?

### Mode B
- 헤딩·라벨·숫자만 훑어 운영 가능한가?
- 입력 모달에서 첫 시도가 default로 통과 가능한가?
- 에러가 발생 필드 옆에 한국어로 뜨는가?
- 카드를 평면 레이아웃으로 바꿔도 의미가 유지되는가?
- 색이 의미(warning/critical/ok)에 일관되게 매핑되어 있는가?
- 입력 중 사용자의 다음 행동을 돕는 힌트가 있는가?

---

## Build Path

### Path 1: Hand-built (주력, 두 모드 공통)
1. Mode A: `references/landing-page-template.html` 스캐폴드 / Mode B: 직접 스캐폴드
2. `references/tokens-css.md`의 `:root` 블록 복사
3. 페이지/뷰별 시맨틱 토큰 추가
4. `references/section-patterns.md`에서 패턴 적용
5. `references/motion-recipes.md`에서 모션 적용 (A: 2개+, B: 절제)
6. `references/checklist.md`로 검증
7. 산출: A는 단일 self-contained `.html`, B는 프로젝트 트리 통합 (예: events-page.ts + ui/errors.ts)

### Path 2: Pandoc pipeline (문서형 한정)
- Markdown 보고서/기사 → `carbon-doc-builder/scripts/convert_to_carbon.py`.
- 랜딩에는 사용 X.

---

## Rubric (Must / Should)

### Must
| 항목 | Evidence |
|------|----------|
| Visual thesis + content plan + token plan 선행 작성 | 빌드 전 3가지 명시 |
| Mode 명시 (A/B) 및 트리거 정합 | 첫 응답에 모드 선언 |
| 모든 style 값이 `--cds-*` 토큰 | grep으로 hardcoded hex/px 0건 |
| Mode A: Hero → Support → Detail → CTA + Hero full-bleed | 섹션 순서, max-width 부재 |
| Mode B: 폼/모달이 sensible defaults + 클라 사전검증 + field-local 에러 | 입력부 검증 |
| 시네마틱 요구 시 (Mode A) `cinematic-immersion-rubric.md` 적용 | story beat·attention path·5초 테스트 기록 |
| 산출 형태(self-contained / project-integrated) 명시 | 첫 응답 |

### Should
| 항목 | 확인 |
|------|------|
| 모션 적용 (A: 2개+, B: 절제 1~2개) | recipes 사용 |
| 모바일 반응형 (375px) | 가로 스크롤 없음 |
| `section-label` / `section-title` / `section-desc` 패턴 (Mode A) | 각 섹션 적용 |
| Utility copy 일관 (Mode B) | hero/캠페인 카피 0 |
| Token plan 문서화 | 확장 토큰 기록 |
| `prefers-reduced-motion` 존중 | media query 포함 |
| Form: live preview / what-if hint (Mode B) | 1개+ |

---

## Verification

빌드 후 `references/checklist.md`의 C1~C9 + 모드별 추가 통과.
Mode B는 입력부 추가 점검:
- 빈 제출 → 서버 도달하지 않고 인라인 메시지로 차단되는가
- 서버 에러 → 한국어 변환되어 발생 필드 옆에 뜨는가
- default 만으로 합법한 제출이 가능한가

---

## References
| 파일 | 로드 시점 |
|------|----------|
| `references/tokens-css.md` | Step 3 (Token Plan) |
| `references/landing-page-template.html` | Step 4 (Mode A 빌드 시작) |
| `references/section-patterns.md` | Step 4 (섹션 구성) |
| `references/motion-recipes.md` | Step 4 (모션 적용) |
| `references/checklist.md` | Step 5 (검증) |
| `/Volumes/Extend/.codex/skills/cognitive-content-rubric/references/cinematic-immersion-rubric.md` | Mode A 시네마틱 시 |

## 원본 스킬 참조
| 스킬 | 기여 |
|------|------|
| `frontend-skill` (deprecated, `_deprecated/`로 이동) | 구성 원칙·Hard Rules·Litmus·Motion·Utility Copy·App UI 가이드 |
| `frontend-carbon` (구 이름, 본 스킬로 흡수) | Carbon 토큰·빌드 파이프라인·랜딩 시퀀스·모션 레시피 |
| `carbon-doc-builder` | Pandoc 파이프라인 (문서 한정) |
| `carbon-doc` | 디자인 토큰 JS 원본 |
| `visual-judgement-rubric` | 본 스킬 직전 단계 (시각 판단) |

---

## Rubric (Must/Should)

### Must
- Preserve the documented mode split and build only the path that matches the task.
  - Evidence: workflow keeps Mode A and Mode B decision logic explicit
- Validate outputs against the checklist before closing.
  - Evidence: `## Verification` references `references/checklist.md` and any mode-specific checks
- Keep local policy alignment explicit.
  - Evidence: `## AGENTS.md Alignment` references `/Volumes/Extend/.codex/AGENTS.md`

### Should
- Reuse the reference files instead of duplicating design or motion guidance inline.
- Record both desktop and mobile evidence for major UI changes.

## AGENTS.md Alignment
- 본 스킬은 `/Volumes/Extend/.codex/AGENTS.md`의 Global Execution Policy를 준수한다.
- AGENTS 기준 항목: `Goal-First`, `Rubric-Driven`, `Completion Rule`.
- 변경 후 `quality-gate` 기준으로 증거를 점검해 기록한다.
