# Section Patterns

랜딩 페이지에서 반복 사용하는 섹션 패턴. GEO 강의 상세 페이지에서 검증된 구조.

## 로드 시점

SKILL.md Step 4 (빌드) 수행 시 필요한 섹션 패턴 참조.

---

## 1. Hero — Full-bleed 그라디언트

```html
<section class="hero">
  <div class="hero-grid"></div> <!-- 배경 그리드 패턴 -->
  <div class="container">
    <div class="hero-badge">
      <span class="dot"></span> <!-- pulse 애니메이션 -->
      배지 텍스트
    </div>
    <h1>메인 헤드라인<br><span class="highlight">강조 텍스트</span></h1>
    <p class="hero-sub">서브 카피 (2~3줄)</p>
    <div class="hero-stats">
      <div class="hero-stat">
        <span class="number">숫자<span class="unit">단위</span></span>
        <span class="label">설명</span>
      </div>
      <!-- 최대 4개 -->
    </div>
  </div>
</section>
```

**CSS 핵심:**
- `min-height: 100vh; display: flex; align-items: center;`
- `background: linear-gradient(135deg, var(--cds-hero-start), var(--cds-hero-mid), var(--cds-hero-end));`
- `.hero-grid`: `background-image` 로 60px 그리드 라인
- `.hero-stat`: `backdrop-filter: blur(8px);` 글래스모피즘
- `.highlight`: `background: linear-gradient(...); -webkit-background-clip: text;`

---

## 2. Narrative — 스토리텔링 블록

```html
<section>
  <div class="container">
    <div class="narrative">
      <p>도입 문장</p>
      <p>전개 문장. <strong>강조</strong>는 bold.</p>
      <span class="em-line">
        핵심 메시지<br>
        <span class="highlight-text">하이라이트 구간</span>
      </span>
      <p>마무리 문장</p>
    </div>
  </div>
</section>
```

**CSS 핵심:**
- `.narrative`: `max-width: 720px; margin: 0 auto; font-size: 18px; line-height: 2;`
- `.em-line`: `font-size: 22px; font-weight: 700;` 독립 강조 줄
- `.highlight-text`: `color: var(--cds-interactive);`

---

## 3. Problem — Before/After 비교

```html
<section style="background: var(--cds-layer-01);">
  <div class="container">
    <div class="text-center">
      <p class="section-label">라벨</p>
      <h2 class="section-title">제목</h2>
      <p class="section-desc mx-auto">설명</p>
    </div>
    <div class="problem-visual"> <!-- grid: 1fr auto 1fr -->
      <div class="problem-card old">
        <h3>Before</h3>
        <div class="flow">
          <div class="flow-step">단계 1</div>
          <span class="flow-arrow">&#8595;</span>
          <div class="flow-step">단계 2</div>
          <div class="flow-result">결과</div>
        </div>
      </div>
      <div class="problem-arrow">&rarr;</div>
      <div class="problem-card new">
        <h3>After</h3>
        <!-- 동일 구조 -->
      </div>
    </div>
  </div>
</section>
```

---

## 4. Track Selector — 2트랙 비교 카드

```html
<div class="track-grid"> <!-- grid: repeat(2, 1fr) -->
  <div class="track-card track-a">
    <div class="track-header">
      <span class="track-tag">A Track</span>
      <h3>트랙 제목</h3>
      <p>한 줄 설명</p>
      <div class="track-meta">
        <span>&#9201; 시간</span>
        <span>&#128187; 요구사항</span>
      </div>
    </div>
    <div class="track-body">
      <h4>커리큘럼</h4>
      <ul class="module-list">
        <li>
          <span class="module-num">1</span>
          <span class="module-text"><strong>모듈명</strong> &mdash; 설명</span>
          <span class="module-time">30분</span>
        </li>
      </ul>
    </div>
  </div>
  <!-- track-b 동일 구조 -->
</div>
```

**색상 분리:** `--cds-track-a` / `--cds-track-b` 시맨틱 토큰 사용.

---

## 5. Strategy Grid — 카드 그리드 (3열)

```html
<div class="strategy-grid"> <!-- grid: repeat(3, 1fr) -->
  <div class="strategy-card" data-num="01">
    <h3>전략 이름</h3>
    <p class="desc">설명</p>
    <div class="strategy-bar">
      <div class="strategy-bar-fill" style="width:70%"></div>
    </div>
    <div class="strategy-meta">
      <span>난이도: 낮음</span>
      <span class="effect">+22~28%</span>
    </div>
  </div>
</div>
```

---

## 6. Persona — 고객 목소리 리스트

```html
<div class="persona-list">
  <div class="persona-item">
    <span class="persona-voice">"고객 고민 인용"</span>
    <span class="persona-context">해결 방안 설명</span>
  </div>
</div>
```

---

## 7. CTA — 최종 전환 섹션

```html
<section class="cta">
  <div class="container">
    <h2>전환 헤드라인</h2>
    <p class="cta-narrative">서브 카피</p>
    <div class="cta-cards">
      <div class="cta-card">
        <div class="track-label">트랙 라벨</div>
        <h3>상품명</h3>
        <div class="date">날짜</div>
        <div class="info">부가 정보</div>
      </div>
    </div>
    <p class="cta-note">준비물, 안내사항 등</p>
  </div>
</section>
```

**CSS 핵심:**
- Hero와 동일한 그라디언트 배경 재사용 (시각적 bookend)
- `.cta-card`: `backdrop-filter: blur(12px);` 글래스 카드
