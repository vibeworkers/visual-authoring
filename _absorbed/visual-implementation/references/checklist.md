# Build Verification Checklist

빌드 완료 후 9항목을 확인한다. 전부 통과해야 납품.

## 로드 시점

SKILL.md Step 5 (검증) 수행 시 로드.

---

## Checklist

- [ ] **C1. 토큰 사용률** — 모든 색상·간격·반지름 값이 `--cds-*` 변수를 사용한다. hardcoded hex/px 없음. (`clamp()` 내부 px와 media query breakpoint만 예외)
- [ ] **C2. Full-bleed Hero** — Hero 섹션에 `max-width` 래퍼가 없다. 내부 `.container`만 제한.
- [ ] **C3. 브랜드 가시성** — 첫 뷰포트에서 브랜드/제품명이 가장 큰 텍스트이다. nav를 숨겨도 브랜드가 보인다.
- [ ] **C4. 섹션 단일 책임** — 각 `<section>`이 하나의 역할만 수행한다. (설명 / 증명 / 심화 / 전환)
- [ ] **C5. bx-- 클래스 미사용** — Carbon 컴포넌트 클래스(`bx--*`)가 없다. (명시적 요청 시 제외)
- [ ] **C6. 모션 최소 2개** — fadeInUp(진입) + scroll reveal 최소 구현. 추가 모션은 선택.
- [ ] **C7. 모바일 반응형** — 375px 너비에서 텍스트가 읽힌다. 가로 스크롤 없음.
- [ ] **C8. 자립형 HTML** — 파일을 더블클릭하면 정상 렌더링. 외부 CSS/JS 참조 없음 (Google Fonts만 예외).
- [ ] **C9. 한국어 렌더링** — Noto Sans KR fallback이 선언되어 있고, 한글 텍스트가 깨지지 않는다.

---

## 검증 명령어 (선택)

```bash
# C1: hardcoded hex 검사
grep -nE '#[0-9a-fA-F]{3,8}' output.html | grep -v ':root' | grep -v 'var(--'

# C5: bx-- 클래스 검사
grep -n 'bx--' output.html

# C8: 외부 참조 검사 (fonts.googleapis.com만 허용)
grep -nE 'href="|src="' output.html | grep -v 'fonts.googleapis.com' | grep -v '#'
```
