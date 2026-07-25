# Absorption Cycle — Phase 0 상세 (GGACA)

규칙으로 잠그고, 정본 어휘로 외부 자산을 흡수하며, 9단계 게이트를 사이클로 닫는 집필 방법론.
원형은 `ggaca-authoring` 스킬 (전문 스냅샷: `../_absorbed/ggaca-authoring/SKILL.md`).
GGACA = Governance-Gated Absorption Cycle Authoring, 한글 명칭 "규칙-흡수-사이클 집필법".

GGACA는 본문을 쓰지 않는다 — 어휘 규칙·게이트·라우팅만 잠근다. 본문·빌드·렌더링·검증은 specialist lane이 소유한다.

## 진입 조건 (4가지 모두 참일 때만)

1. **외부 자산이 여러 개다.** 다른 저자의 책·논문·코퍼스·도구 어휘를 단일 deliverable로 묶는다.
2. **원본을 손대지 않는다.** 외부 자산은 read-only. 인용·요약이 아니라 "흡수"한다.
3. **저자 정본 어휘가 따로 있다.** 외부 어휘를 본문에 노출하지 않고 저자의 어휘 체계로 번역한다.
4. **사이클로 닫는다.** 각 사이클 끝에 게이트 통과 + 다음 사이클 인계 1문장.

하나라도 아니면 Phase 0을 skip하고 더 가벼운 방법(편집·종합·doc-as-code)을 쓴다.

## 닫힌 deliverable이 약속하는 5가지

1. 정본 어휘 본문 위반 0건 (외부 어휘는 Reference 자리에만)
2. 원본 무수정 (외부 자산 + 정본 핵심 문서 line/byte 무변경)
3. 충돌 해소 로그 (어휘·정의 충돌은 5줄 카드로 닫힘)
4. 검증 가능한 카운트 (금지·필수·근거층 어휘 자동 측정)
5. 사이클 인계 (다음 사이클이 호출 가능한 1문장)

## 6개 잠금 규칙 (R1~R6)

매 사이클이 상속. 새 사용자 결정은 충돌 카드 5줄로 R7·R8 추가 또는 R1~R6 갱신.

| 규칙 | 정의 |
|---|---|
| **R1** — 외부 어휘 본문 노출 0 | 외부 자산 내부 어휘(원본 고유명사·약어·자체 명명)는 본문 사용 금지. Reference 줄에서만 출처 표기 |
| **R2** — 비유 어휘 본문 노출 0 | 정본 정의를 흐리는 비유 어휘는 본문에서 정본 어휘로 교체 |
| **R3** — 정본 핵심 문서 무수정 | 저자의 정본 핵심 문서(통상 3~5개)는 사이클 종료까지 line/byte 수정 0건 |
| **R4** — 외부 원본 무수정 | 흡수 대상 외부 자산은 read-only. 0건 수정 |
| **R5** — 정정은 백업 필수 | baseline 정정이 불가피하면 정정 전 `*.bak_<DATE>` 백업 + 사유 명시 |
| **R6** — 새 개념 도입 0 | 흡수 본문은 정본 어휘만 사용. 외부 어휘는 정본 어휘로 번역해 흡수 |

## 9단계 게이트 (M0 → M8)

순서 의존. 게이트 통과 없이 다음 단계 진입 금지.

| 게이트 | 무엇을 닫는가 | 산출물 자리 (templated) |
|---|---|---|
| M0 — 흡수 골격 확장 | 외부 자산 식별 + deliverable 구조에 1줄 배정 | `<scaffold-dir>/absorption_skeleton_v0_X_<DATE>.md` |
| M1 — 본문 1차 (전반부) | deliverable 전반부 본문화 (`unfolding-cycle` 호출 가능) | `<draft-dir>/*_cycle_M1_<DATE>.md` |
| M2 — 본문 2차 (후반부) | deliverable 후반부 본문화 (`unfolding-cycle` 호출 가능) | `..._cycle_M2_<DATE>.md` |
| M3 — 충돌 해소 | 충돌 자리 N건을 본문 라인 번호로 닫음 | `<ops-dir>/integration_conflict_log_<DATE>.md` |
| M4 — 매니페스트·빌드 | 빌드 입력·금지·필수 어휘 잠금 | `<ops-dir>/workspace_manifest.json` 동등물 |
| M5 — 렌더링 | 단일 본문 조립 + 최종 형식(HTML·PDF·docx) | `<deliverable-dir>/*.{html,pdf,docx}` |
| M6 — 검증 게이트 | 루브릭 라인·카운트로 증명 | `<reports-dir>/*_verification_<DATE>.md` |
| M7 — 5초 테스트 | 첫 화면 약속 3요소 노출 + 사람 5인 실측 | `..._5sec_test_plan_<DATE>.md` |
| M8 — 릴리즈 | 원본 보존 증명 + 게이트 상태 동기화 | `<release-dir>/*_RELEASE.md` |

**Addendum 패턴**: 릴리즈 후 발견된 리스크는 별도 Addendum(`*_addendum_<DATE>.md`)으로 닫고
릴리즈 노트의 게이트 상태를 동기화한다. baseline 자체를 재정정하지 않는다.

## 5개 검증 카운트 (자동 감시)

매니페스트의 `forbidden_terms` / `required_canonical_terms`로 잠그고 사이클 끝에 자동 카운트.

| 검증 | 측정 | Pass 임계 |
|---|---|---|
| V-Forbidden | 금지 어휘 본문 카운트 (Reference·메타 줄 제외) | 0 |
| V-Required | 필수 정본 어휘 본문 카운트 | 각 ≥ 1 (분량에 맞춰 N 잠금) |
| V-TheoryFoundation | 이론·근거층 어휘 카운트 | 각 ≥ 임계 |
| V-NewAbsorption | 이번 사이클에 흡수된 새 정본 어휘 카운트 | 각 ≥ 임계 |
| V-FrontHero | 첫 화면 hero에 약속 3요소 노출 | 3/3 |

## 충돌 카드 5줄 양식

```
## 충돌 N — <충돌 제목>

| 항목 | 정본 | 원본 | 해소 |
|---|---|---|---|
| 표기 | <정본 어휘> | <원본 어휘> | 정본 어휘로 흡수, 원본은 Reference 자리에만 |

**해소 규칙**: 1줄
**닫힌 위치**: <파일> §<섹션> line <N>
**상태**: ✅ 닫힘 / ⚠️ 보류
```

## Owner-split

| Owner | 역할 |
|---|---|
| Producer (Project) — 본문 lane | 흡수 골격, 사이클 적층본 작성 |
| Producer (Specialist) — 빌드 lane | 단일 본문 조립, 최종 형식 변환 |
| Lifecycle — 정본·원본 lane | 정본 핵심 문서·외부 원본 보존 |
| Governance — Phase 0 (GGACA) | R1~R6, M0~M8, 5 카운트 정의 + 감시 |
| Consumer/Verifier — reports lane | 검증 리포트, Addendum, 5초 테스트 |
| Release — release_notes lane | RELEASE 문서 동기화 |

## 사이클 호출 흐름

1. 사용자 입력 1줄 → clarification packet + owner-split으로 받는다.
2. 사용자 결정이 정책에 들어오면 → 충돌 카드 5줄로 R1~R6에 반영.
3. 사이클 시작 → M0부터 9게이트 순서대로, 게이트별 산출물·라인·카운트 명시.
4. 사이클 종료 → M8 RELEASE 동기화 + 다음 사이클 인계 1문장.

## 사용 시나리오 / 비사용

**쓴다**: 통합 교재 집필, 논문(선행연구 흡수), 장편 사료 기반 저작, 장기 통합 보고서.
**안 쓴다**: 단일 저자 단일 글 신규 집필, 단순 편집·교정·번역, 일회성 짧은 글.

**연계 스킬**: `anthropic-skills:unfolding-cycle`(펼침 사이클) — M1·M2·M3에서 압축 정의를 다층 표로 펼칠 때 호출. `unfolding`(펼침 해석)과 함께 동등 스킬로 취급.

## 원형·출처

- 원형: 2026-05-18~20 의도적 수익 체계론 × fitCrafting 통합 교과서 사이클.
- 일반화: 2026-05-20 `ops/cogarch_integration_cycle_pattern_20260520.md` → `ggaca-authoring` 스킬.
- 본 문서: 2026-07-07 `visual-authoring` Phase 0으로 흡수. 원문 스냅샷 `../_absorbed/ggaca-authoring/SKILL.md`.
- 원형 스킬이 참조하던 `references/gates.md` 등 하위 문서는 배포본에 존재하지 않았다 — SKILL.md 스냅샷이 완결 정본이다.
