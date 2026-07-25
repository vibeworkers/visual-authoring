# Vivid Design Tokens — CSS Custom Properties (`--viv-*`)

Vivid는 Carbon과 대등한 1급 표현형(expressive) 디자인 시스템이다.
고채도 컬러·볼드 타이포·그라디언트·글로우·시네마틱 모션으로 감정·장면·전환을 만든다.
"장식 자유"가 아니라 "표현 강도 상향"이다 — 접근성·label-masked 판독·5초 테스트 게이트는 Carbon과 동일하게 적용된다.

## 로드 시점

Phase 3 (Design-System Select)에서 Vivid 선택 시, Phase 4 Token Plan 수행 시 로드.
모든 Vivid 산출물은 이 블록을 복사한 뒤 산출물별 시맨틱 확장만 추가한다.

---

## Base Tokens (Stage D — dark, 기본)

```css
:root {
  /* ── Stage (배경 무대) ── */
  --viv-background:  #0b0b12;
  --viv-layer-01:    #14141f;
  --viv-layer-02:    #1e1e2e;
  --viv-scrim:       rgba(5, 5, 10, 0.55);   /* 이미지/그라디언트 위 텍스트 보호막 */

  /* ── Text ── */
  --viv-text-primary:   #f5f6fa;
  --viv-text-secondary: #b8bcd0;
  --viv-text-muted:     #7d81a0;
  --viv-text-on-accent: #0b0b12;

  /* ── Accent slots (산출물당 primary 1종 잠금) ── */
  --viv-accent:        #7c3aed;   /* electric violet — 기본 primary */
  --viv-accent-hover:  #8f5bf5;
  --viv-accent-alt:    #06b6d4;   /* cyan — 보조. 화면 면적 10% 이하 */
  --viv-accent-hot:    #f43f5e;   /* hot rose — CTA/긴급 강조 전용 */
  --viv-accent-lime:   #a3e635;   /* lime — 성공/에너지 상태 전용 */

  /* ── Gradient (1급 토큰) ── */
  --viv-grad-hero:  linear-gradient(135deg, #7c3aed 0%, #d946ef 45%, #f43f5e 100%);
  --viv-grad-cool:  linear-gradient(160deg, #0ea5e9 0%, #7c3aed 100%);
  --viv-grad-stage: radial-gradient(1200px 600px at 70% -10%, rgba(124, 58, 237, 0.35), transparent 60%);

  /* ── Support ── */
  --viv-support-error:   #ff5d6c;
  --viv-support-warning: #fbbf24;
  --viv-support-success: #34d399;
  --viv-support-info:    #38bdf8;

  /* ── Border / Focus / Highlight ── */
  --viv-border-subtle: rgba(255, 255, 255, 0.10);
  --viv-border-strong: rgba(255, 255, 255, 0.28);
  --viv-focus:         #8f5bf5;
  --viv-highlight:     rgba(124, 58, 237, 0.22);
}
```

## Spacing Scale (Carbon과 동일 8px grid)

간격 체계는 Carbon과 동일한 스케일·번호를 쓴다. 표현 차이는 색·타이포·모션에서 내고,
공간 리듬은 시스템 간 호환을 유지한다 (Mode V 정규화 시 1:1 치환 가능).

```css
:root {
  --viv-spacing-01:  2px;
  --viv-spacing-02:  4px;
  --viv-spacing-03:  8px;
  --viv-spacing-04:  12px;
  --viv-spacing-05:  16px;
  --viv-spacing-06:  24px;
  --viv-spacing-07:  32px;
  --viv-spacing-08:  40px;
  --viv-spacing-09:  48px;
  --viv-spacing-10:  64px;
  --viv-spacing-11:  80px;
  --viv-spacing-12:  96px;
  --viv-spacing-13:  160px;
}
```

## Typography (볼드 디스플레이 우선)

```css
:root {
  --viv-font-display: 'Pretendard Variable', 'Pretendard', 'Inter', 'Noto Sans KR', sans-serif;
  --viv-font-sans:    'Pretendard Variable', 'Pretendard', 'Inter', 'Noto Sans KR', sans-serif;
  --viv-font-mono:    'JetBrains Mono', 'IBM Plex Mono', 'Menlo', monospace;

  /* Type scale — display는 clamp 반응형 */
  --viv-type-display-01: clamp(48px, 8vw, 96px);
  --viv-type-display-02: clamp(36px, 5.5vw, 64px);
  --viv-type-heading-01: 36px;
  --viv-type-heading-02: 28px;
  --viv-type-heading-03: 22px;
  --viv-type-heading-04: 17px;
  --viv-type-body-01:    15px;
  --viv-type-body-02:    13px;
  --viv-type-label-01:   11px;

  /* Weight / tracking */
  --viv-weight-display: 800;
  --viv-weight-heading: 700;
  --viv-weight-body:    450;
  --viv-tracking-display: -0.03em;
}
```

## Radius / Shadow / Glow

```css
:root {
  --viv-radius-sm:   12px;
  --viv-radius-md:   20px;
  --viv-radius-lg:   28px;
  --viv-radius-full: 999px;

  --viv-shadow-md:   0 8px 32px rgba(0, 0, 0, 0.45);
  --viv-shadow-lg:   0 20px 64px rgba(0, 0, 0, 0.55);

  /* Glow — Vivid 고유. Stage L/Restrained에서는 금지 */
  --viv-glow-accent: 0 0 48px rgba(124, 58, 237, 0.45);
  --viv-glow-hot:    0 0 40px rgba(244, 63, 94, 0.40);
}
```

## Motion Tokens (시네마틱)

```css
:root {
  --viv-motion-fast:      160ms;
  --viv-motion-base:      320ms;
  --viv-motion-slow:      640ms;
  --viv-motion-cinematic: 1200ms;

  --viv-ease-out:      cubic-bezier(0.16, 1, 0.3, 1);
  --viv-ease-dramatic: cubic-bezier(0.83, 0, 0.17, 1);
}
```

`prefers-reduced-motion: reduce`에서는 `--viv-motion-cinematic`/`--viv-motion-slow`를 `--viv-motion-base` 이하로 강등하고 시차(parallax)·자동재생 모션을 끈다.

---

## Adaptive Profiles (범용 상황 적응)

Vivid는 dark 랜딩 전용이 아니다. 같은 `--viv-*` 접두사를 유지한 채 3개 프로파일로 상황에 적응한다.
프로파일 선택은 Phase 3 기록에 명시한다: `vivid(stage=D|L, restrained=true|false)`.

### Stage L (Light) — 슬라이드·인쇄·밝은 매체

배경/텍스트/보더만 오버라이드하고 accent·gradient는 유지한다 (대비 재검증 필수).

```css
:root {
  --viv-background:    #fafafc;
  --viv-layer-01:      #f0f0f6;
  --viv-layer-02:      #e6e6f0;
  --viv-scrim:         rgba(250, 250, 252, 0.72);
  --viv-text-primary:  #16121f;
  --viv-text-secondary:#4a4660;
  --viv-text-muted:    #807c96;
  --viv-border-subtle: rgba(10, 10, 30, 0.12);
  --viv-border-strong: rgba(10, 10, 30, 0.32);
  /* glow 토큰 사용 금지 — shadow로 대체 */
}
```

### Restrained Profile — 일반 표면 인접 시 강도 조절

제품 UI·문서·교육 자료처럼 차분한 표면과 인접할 때, Vivid 정체성(고채도 accent·볼드 타이포)은
유지하되 강도만 낮춘다. **Carbon 혼용이 아니라 Vivid 강도 조절이다** — 접두사는 `--viv-*` 그대로.

제약:
- accent 적용 면적 화면의 ~15% 이하
- gradient는 hero/헤더 1곳만, `--viv-grad-stage` 배경 장식 금지
- glow 토큰 금지
- `--viv-weight-display: 700`으로 강등
- 모션은 `--viv-motion-base` 이하만

### Full (기본) — 캠페인·런칭·키비주얼

위 제약 없음. Cinematic Immersion Plan(모드 L 참조)과 함께 사용.

---

## Semantic Extensions (산출물별 추가)

산출물별 시맨틱 변수는 base token을 참조하거나 같은 `--viv-` 접두사를 사용한다.

```css
:root {
  /* Hero */
  --viv-hero-bg:      var(--viv-grad-hero);
  --viv-hero-title:   var(--viv-text-primary);

  /* Track colors (멀티트랙 페이지 — 혼용 금지의 유일한 예외 축) */
  --viv-track-a:       #d946ef;
  --viv-track-a-dim:   rgba(217, 70, 239, 0.16);
  --viv-track-b:       #06b6d4;
  --viv-track-b-dim:   rgba(6, 182, 212, 0.16);
}
```

---

## 사용 규칙 (Carbon과 동일 강제)

1. 색상·간격·반지름·모션에 hardcoded 값 금지. 반드시 `--viv-*` 변수 사용 (`clamp()` 내부와 media query breakpoint만 raw px 허용).
2. 산출물당 `--viv-accent` primary 1종 잠금. `alt`/`hot`/`lime`은 보조·상태 용도 한정이며 사용 시 근거 1줄.
3. 본문 텍스트 대비 WCAG AA(4.5:1) 이상, display급은 3:1 이상. 고채도/이미지/그라디언트 위 텍스트는 `--viv-text-on-accent` 또는 `--viv-scrim` 경유.
4. 두 시스템 혼용 금지 — 같은 화면에 `--cds-*` 등장 0. (Mode V 정규화 중 과도기 레거시 alias만 예외, 완료 전 제거.)
5. gradient 위 장문 본문 금지 — 제목·짧은 리드만.
6. `prefers-reduced-motion` 존중 (위 Motion 절 강등 규칙).
7. 새 시맨틱 변수 추가 시 `--viv-` 접두사 필수.
8. label-masked 판독·5초 테스트는 Vivid에도 동일 게이트다 — 화려함이 판독을 이기면 FAIL.
