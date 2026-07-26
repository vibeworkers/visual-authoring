# Carbon Design Tokens — CSS Custom Properties

Carbon Design System 토큰을 `:root` CSS 변수로 선언한다.
모든 랜딩 페이지는 이 블록을 복사한 뒤 페이지별 시맨틱 확장만 추가한다.

## 로드 시점

SKILL.md Step 3 (Token Plan) 수행 시 로드.

---

## Base Tokens

```css
:root {
  /* ── Core ── */
  --cds-background:       #ffffff;
  --cds-layer-01:         #f4f4f4;
  --cds-layer-02:         #e0e0e0;

  /* ── Text ── */
  --cds-text-primary:     #161616;
  --cds-text-secondary:   #525252;
  --cds-text-placeholder: #a8a8a8;
  --cds-text-on-color:    #ffffff;

  /* ── Interactive ── */
  --cds-interactive:       #0f62fe;
  --cds-interactive-hover: #0353e9;

  /* ── Brand ── */
  --cds-brand-01:  #0f62fe;   /* Blue 60 */
  --cds-brand-02:  #393939;   /* Gray 80 */
  --cds-brand-03:  #0043ce;   /* Blue 80 */

  /* ── Support ── */
  --cds-support-error:   #da1e28;
  --cds-support-warning: #f1c21b;
  --cds-support-success: #24a148;
  --cds-support-info:    #0043ce;

  /* ── Border ── */
  --cds-border-subtle:  #e0e0e0;
  --cds-border-strong:  #8d8d8d;
  --cds-border-inverse: #161616;

  /* ── Focus ── */
  --cds-focus: #0f62fe;

  /* ── Highlight ── */
  --cds-highlight: #d0e2ff;   /* Blue 20 */
}
```

## Spacing Scale (8px base grid)

```css
:root {
  --cds-spacing-01:  2px;    /* 0.25rem */
  --cds-spacing-02:  4px;    /* 0.25rem */
  --cds-spacing-03:  8px;    /* 0.5rem  */
  --cds-spacing-04:  12px;   /* 0.75rem */
  --cds-spacing-05:  16px;   /* 1rem    */
  --cds-spacing-06:  24px;   /* 1.5rem  */
  --cds-spacing-07:  32px;   /* 2rem    */
  --cds-spacing-08:  40px;   /* 2.5rem  */
  --cds-spacing-09:  48px;   /* 3rem    */
  --cds-spacing-10:  64px;   /* 4rem    */
  --cds-spacing-11:  80px;   /* 5rem    */
  --cds-spacing-12:  96px;   /* 6rem    */
  --cds-spacing-13:  160px;  /* 10rem   */
}
```

## Typography

```css
:root {
  --cds-font-sans:  'IBM Plex Sans', 'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif;
  --cds-font-mono:  'IBM Plex Mono', 'Menlo', monospace;
  --cds-font-serif: 'IBM Plex Serif', 'Noto Serif KR', serif;

  /* Type scale (px) */
  --cds-type-display-01: 42px;
  --cds-type-heading-01: 32px;
  --cds-type-heading-02: 24px;
  --cds-type-heading-03: 20px;
  --cds-type-heading-04: 16px;
  --cds-type-body-01:    14px;
  --cds-type-body-02:    12px;
  --cds-type-label-01:   11px;
  --cds-type-caption-01:  9px;
}
```

## Radius & Shadow

```css
:root {
  --cds-radius-sm:   10px;
  --cds-radius-md:   16px;
  --cds-radius-full: 100px;

  --cds-shadow-sm:  0 2px 8px rgba(15, 23, 42, 0.06);
  --cds-shadow-md:  0 4px 24px rgba(15, 23, 42, 0.08);
  --cds-shadow-lg:  0 12px 48px rgba(15, 23, 42, 0.12);
  --cds-shadow-xl:  0 24px 64px rgba(15, 23, 42, 0.16);
}
```

## Semantic Extensions (페이지별 추가)

페이지별로 아래와 같은 시맨틱 변수를 `:root` 에 추가한다.
반드시 base token을 참조하거나 같은 `--cds-` 접두사를 사용한다.

```css
:root {
  /* Hero gradient */
  --cds-hero-start:    #0f172a;
  --cds-hero-mid:      #1e3a5f;
  --cds-hero-end:      #1e40af;

  /* Hero overlay */
  --cds-hero-overlay-purple: rgba(139, 92, 246, 0.15);
  --cds-hero-overlay-blue:   rgba(56, 189, 248, 0.12);
  --cds-grid-line:           rgba(255, 255, 255, 0.03);

  /* Glass */
  --cds-glass-bg:     rgba(255, 255, 255, 0.06);
  --cds-glass-border: rgba(255, 255, 255, 0.10);

  /* Track colors (multi-track pages) */
  --cds-track-a:       #8b5cf6;
  --cds-track-a-light: #ede9fe;
  --cds-track-b:       #0891b2;
  --cds-track-b-light: #e0f7fa;

  /* Accent (CTA, highlights) */
  --cds-accent:       #f59e0b;
  --cds-accent-dark:  #d97706;
}
```

## 사용 규칙

1. 색상·간격·반지름에 hardcoded hex/px 금지. 반드시 `--cds-*` 변수 사용.
2. `clamp()` 안의 px 값과 media query breakpoint만 raw px 허용.
3. 새 시맨틱 변수 추가 시 `--cds-` 접두사 필수.
4. 기존 프로젝트의 `--primary` 등 레거시 별칭은 `var(--cds-interactive)` 등으로 참조.
