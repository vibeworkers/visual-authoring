# Motion Recipes

CSS-only 모션 레시피. 외부 라이브러리 없이 static HTML에서 사용 가능.

## 로드 시점

SKILL.md Step 4 (빌드) 수행 시 모션 적용 시 참조.

---

## 1. Pulse — 상태 표시 점

```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.dot {
  width: 8px;
  height: 8px;
  background: var(--cds-support-success);
  border-radius: 50%;
  animation: pulse 2s infinite;
}
```

**용도:** Hero 배지의 "모집 중" 상태 표시.

---

## 2. Fade-in Up — 진입 애니메이션

```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

.hero-badge  { animation: fadeInUp 0.6s ease both; animation-delay: 0.1s; }
.hero h1     { animation: fadeInUp 0.6s ease both; animation-delay: 0.2s; }
.hero-sub    { animation: fadeInUp 0.6s ease both; animation-delay: 0.3s; }
.hero-stats  { animation: fadeInUp 0.6s ease both; animation-delay: 0.4s; }
```

**용도:** Hero 요소의 순차 등장. stagger delay 0.1s 간격.

---

## 3. Scroll Reveal — IntersectionObserver

```css
.reveal {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
```

```html
<script>
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) e.target.classList.add('visible');
  });
}, { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
</script>
```

**용도:** 각 `<section>`에 `.reveal` 추가. 스크롤 시 등장.

---

## 4. Hover Transition — 버튼/카드

```css
.cta-btn {
  transition: background 0.2s ease, transform 0.15s ease;
}
.cta-btn:hover {
  background: var(--cds-interactive-hover);
  transform: translateY(-2px);
}

.card {
  transition: box-shadow 0.2s ease, transform 0.15s ease;
}
.card:hover {
  box-shadow: var(--cds-shadow-lg);
  transform: translateY(-4px);
}
```

**용도:** CTA 버튼, 트랙 카드, 전략 카드 등 인터랙티브 요소.

---

## 5. Gradient Highlight — 텍스트 그라디언트

```css
.highlight {
  background: linear-gradient(135deg, #60a5fa, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

**용도:** Hero 제목의 강조 텍스트.

---

## 적용 원칙

1. 랜딩 페이지에 **최소 2개** 모션 사용 (Must: 진입 + 스크롤 reveal)
2. 모든 `transition`/`animation` 시간은 **0.6s 이하** (빠르고 절제)
3. 모션이 빠른 녹화에서도 **눈에 띄어야** 함
4. 모바일에서도 **부드럽게** 작동해야 함 (`prefers-reduced-motion` 존중 권장)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
