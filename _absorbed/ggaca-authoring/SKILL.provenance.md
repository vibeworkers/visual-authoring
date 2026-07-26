---
name: ggaca-authoring
description: 규칙으로 잠그고 정본 어휘로 흡수하며 사이클로 닫는 집필 방법론 (GGACA — Governance-Gated Absorption Cycle Authoring). 외부 자산(다른 책·논문·코퍼스·도구 어휘)을 정본 어휘로 흡수해 단일 deliverable(책·교재·논문·보고서·웹북)로 묶는 작업에 사용한다. 호출 트리거 — "외부 자료를 흡수해 책으로", "여러 자료를 통합 교재로", "원본은 보존하고 본문에 녹이고 싶다", "용어 충돌이 있는 자료들을 한 권으로", "사이클로 집필", "ggaca", "흡수 집필", "통합 교과서 작성", "정본 어휘 잠금", "draft cycle authoring", "absorption authoring". 이미 어휘 정책이 잡혀 있고 외부 자산이 여러 개이며 baseline을 손대지 않으려는 집필 작업에 가장 잘 맞는다. 단순 편집·번역·일회성 글에는 사용하지 말 것.
---

# GGACA — Governance-Gated Absorption Cycle Authoring

**한글 명칭: 규칙-흡수-사이클 집필법**
**영문 약어: GGACA**

규칙(R1~R6)으로 잠그고, 정본 어휘로 외부 자산을 흡수하며, 9단계 게이트(M0~M8)를 사이클로 닫는 집필 방법론. 본 skill은 cogarch governance 패턴이 집필 specialist lane을 만났을 때의 표준 모드를 1회 호출로 재사용 가능하게 만든 것이다.

## 언제 GGACA를 쓰는가

다음 4가지가 모두 해당되면 GGACA를 쓴다.

1. **외부 자산이 여러 개다.** 다른 저자의 책·논문·코퍼스·도구 어휘를 단일 deliverable로 묶는다.
2. **원본을 손대지 않는다.** 외부 자산은 read-only. 인용·요약이 아니라 "흡수"한다.
3. **저자 정본 어휘가 따로 있다.** 외부 자산의 내부 어휘를 본문에 그대로 노출하지 않고, 저자의 어휘 체계로 번역한다.
4. **사이클로 닫는다.** 한 번에 끝내지 않고, 각 사이클 끝에 게이트 통과 + 다음 사이클 인계 1문장으로 닫는다.

하나라도 해당되지 않으면 더 가벼운 다른 방법(편집·종합·doc-as-code)을 쓴다.

## 5초 안에 무엇을 보장하는가

GGACA로 집필을 닫은 deliverable은 다음 5가지를 약속한다.

1. **정본 어휘 본문 위반 0건.** 외부 자산 내부 어휘는 Reference 자리에만 등장.
2. **원본 무수정.** 외부 자산 + 저자 정본 핵심 문서는 line/byte 수준 무변경.
3. **충돌 해소 로그.** 정본 vs. 원본의 어휘·정의 충돌은 5줄 카드로 닫힘.
4. **검증 가능한 카운트.** 금지 어휘·필수 어휘·훈련/이론 근거층 카운트가 자동 측정 가능.
5. **사이클 인계.** 한 사이클이 끝나면 다음 사이클이 호출 가능한 1문장 인계.

## 9단계 게이트 (M0 → M8)

순서 의존. 게이트 통과 없이 다음 단계 진입 금지.

| 게이트 | 무엇을 닫는가 | 산출물 자리 (templated) |
|---|---|---|
| M0 — 흡수 골격 확장 | 외부 자산 식별 + deliverable 구조에 1줄로 배정 | `<scaffold-dir>/absorption_skeleton_v0_X_<DATE>.md` |
| M1 — 본문 1차 (전반부) | deliverable 전반부 본문화 (`unfolding-cycle` 호출 가능) | `<draft-dir>/*_cycle_M1_<DATE>.md` |
| M2 — 본문 2차 (후반부) | deliverable 후반부 본문화 (`unfolding-cycle` 호출 가능) | `..._cycle_M2_<DATE>.md` |
| M3 — 충돌 해소 | 충돌 자리 N건을 본문 라인 번호로 닫음 (`unfolding-cycle` 호출 가능) | `<ops-dir>/integration_conflict_log_<DATE>.md` |
| M4 — 매니페스트·빌드 파이프라인 | 빌드 입력·금지·필수 어휘 잠금 | `<ops-dir>/workspace_manifest.json` 또는 동등물 |
| M5 — 렌더링 | 단일 본문 조립 + 최종 형식(HTML·PDF·docx) | `<deliverable-dir>/*.{html,pdf,docx}` |
| M6 — 검증 게이트 | 루브릭 라인·카운트로 증명 | `<reports-dir>/*_verification_<DATE>.md` |
| M7 — 5초 테스트 | 첫 화면 약속 3요소 노출 + 사람 5인 실측 | `..._5sec_test_plan_<DATE>.md` |
| M8 — 릴리즈 | 원본 보존 증명 + 게이트 상태 동기화 | `<release-dir>/*_RELEASE.md` |

**Addendum 패턴**: 릴리즈 후 발견된 리스크는 별도 Addendum(예: `*_addendum_<DATE>.md`)으로 닫고, 릴리즈 노트의 게이트 상태를 그 결과로 동기화. baseline 자체를 재정정하지 않는다.

## 6개 잠금 규칙 (R1~R6)

매 사이클이 상속받는 정책. 새 사용자 결정이 들어오면 R7·R8로 추가하거나 R1~R6 중 하나를 갱신한다.

| 규칙 | 정의 |
|---|---|
| **R1** — 외부 어휘 본문 노출 0 | 외부 자산 내부 어휘(원본 고유명사·약어·자체 명명)는 **본문 사용 금지**. Reference 줄에서만 출처 표기 |
| **R2** — 비유 어휘 본문 노출 0 | 정본 정의를 흐릴 수 있는 비유 어휘(예: "외부 인물", "선망의 대상" 류)는 본문에서 정본 어휘로 교체 |
| **R3** — 정본 핵심 문서 무수정 | 저자의 정본 핵심 문서(통상 3~5개)는 사이클 종료까지 line/byte 수정 0건 |
| **R4** — 외부 원본 무수정 | 흡수 대상 외부 자산은 read-only. 0건 수정 |
| **R5** — 정정은 백업 필수 | baseline(통합 deliverable)에 정정이 불가피하면 정정 전 `*.bak_<DATE>` 백업, 사유 명시 |
| **R6** — 새 개념 도입 0 | 흡수 본문은 정본 어휘만 사용. 외부 자산 어휘는 정본 어휘로 번역해 흡수 |

## 5개 검증 카운트 (자동 감시 가능)

매 사이클 끝에 단일 본문에서 자동 카운트해 게이트 통과를 증명. 매니페스트의 `forbidden_terms` / `required_canonical_terms`로 잠근다.

| 검증 | 측정 | Pass 임계 |
|---|---|---|
| V-Forbidden | 금지 어휘 본문 카운트 (Reference·메타 줄 제외) | 0 |
| V-Required | 필수 정본 어휘 본문 카운트 | 각 ≥ 1 (보통 ≥ N, N은 책 분량에 맞춰 잠금) |
| V-TheoryFoundation | 책의 이론·근거층 어휘 카운트 | 각 ≥ 임계 |
| V-NewAbsorption | 이번 사이클에 흡수된 새 정본 어휘 카운트 | 각 ≥ 임계 |
| V-FrontHero | 첫 화면 hero에 약속 3요소 모두 노출 | 3/3 |

## Owner-split (cogarch boundary)

GGACA는 본문을 쓰지 않는다. 어휘 규칙·게이트·라우팅만 잠근다. 본문·빌드·렌더링·검증은 specialist lane이 소유.

| Owner | 역할 |
|---|---|
| Producer (Project) — 본문 lane | 흡수 골격, 사이클 적층본 작성 |
| Producer (Specialist) — 빌드 lane | 단일 본문 조립, 최종 형식 변환 |
| Lifecycle — 정본·원본 lane | 정본 핵심 문서·외부 원본 보존 |
| Governance — GGACA | R1~R6, M0~M8, 5 카운트 정의 + 감시 |
| Consumer/Verifier — reports lane | 검증 리포트, Addendum, 5초 테스트 |
| Release — release_notes lane | RELEASE 문서 동기화 |

## 호출 흐름 (이 skill을 부르면)

1. **사용자 입력 1줄** → GGACA가 cogarch Path 4로 받는다 (Clarification packet 4슬롯 + Owner-split).
2. **사용자 결정이 정책에 들어오면** → §"충돌 카드 5줄 양식"으로 R1~R6에 1줄 추가.
3. **사이클 시작 신호** → M0부터 9게이트 순서대로 진행. 게이트별로 산출물·라인·카운트 명시.
4. **사이클 종료 신호** → M8 RELEASE 동기화 + 다음 사이클 인계 1문장.

## 충돌 카드 5줄 양식

매핑 지도·충돌 해소 로그에서 한 충돌을 닫는 표준 형식.

```
## 충돌 N — <충돌 제목>

| 항목 | 정본 | 원본 | 해소 |
|---|---|---|---|
| 표기 | <정본 어휘> | <원본 어휘> | 정본 어휘로 흡수, 원본은 Reference 자리에만 |

**해소 규칙**: 1줄
**닫힌 위치**: <파일> §<섹션> line <N>
**상태**: ✅ 닫힘 / ⚠️ 보류
```

## 사용 시나리오 (집필 일반)

GGACA는 도메인 중립이다. 다음 4종이 1차 use case.

1. **교재 집필** — 여러 권의 다른 저자 자산을 단일 교과서로 묶을 때 (원형 사례는 `references/case-study-suip-fitcrafting.md` 참조)
2. **논문 집필** — 선행 연구의 어휘·결과를 본인의 frame으로 흡수, 인용·요약 아닌 통합으로
3. **장편 소설/논픽션** — 외부 사료·인터뷰·corpus를 저자의 narrative voice로 흡수
4. **장기 보고서** — 여러 부서·시기의 자료를 단일 frame으로 묶을 때, baseline 보존이 중요한 경우

다음 작업에는 쓰지 않는다.

- 단일 저자 단일 글의 신규 집필 (게이트가 무거움)
- 단순 편집·교정·번역 (외부 자산 흡수 없음)
- 일회성·짧은 글 (사이클 비용이 글 비용보다 큼)

## 참조 문서 (필요할 때만 로드)

본 SKILL.md는 가볍게 두고, 길어지는 정의는 references/로 분리.

- `references/gates.md` — M0~M8 각 게이트의 상세 Pass 조건, 작업 단위
- `references/rules.md` — R1~R6의 잠금 위치·예외·확장 가이드
- `references/counts.md` — 5 카운트의 측정 스크립트 예시 + 임계 조정 규칙
- `references/conflict-card.md` — 충돌 카드 5줄 양식 + 사용 사례 3종
- `references/templates.md` — manifest/skeleton/release 템플릿 예시
- `references/case-study-suip-fitcrafting.md` — 본 방법론의 원형 사례 (의도적 수익 체계론 × fitCrafting 2026-05-18~20)

각 게이트의 본문 작성·빌드 실행은 본 skill이 아니라 호출한 specialist lane(manuscript / scripts / analysis)이 담당한다. GGACA는 위에서 게이트와 카운트만 관리한다.

## 호출하는 다른 skill

- **`unfolding-cycle` (펼침 사이클)** — M1·M2·M3 게이트에서 압축 정본 정의를 다층 표로 펼칠 때 호출. cogarch Path 4 산하 전역 보조 skill. GGACA의 종속물이 아니라 동등 skill.

## cogarch 위치

본 skill은 **cogarch Path 4 (Orchestration / Governance gateway)** 가 집필 specialist를 만났을 때 호출되는 표준 모드. 데이터 분석·디자인·시스템 설계 등 다른 specialist는 동일 패턴의 변형(Authoring 자리에 Analysis·Design·Architecture)으로 별도 skill을 둘 수 있다.

## 무엇을 *하지 않는가*

- 본문 자체를 쓰지 않음 — 호출한 본문 lane이 소유.
- 빌드 도구를 정의하지 않음 — 호출한 빌드 lane이 소유. (예시 매니페스트만 제공.)
- 정본·외부 원본 수정 0건 — Lifecycle lane이 소유.
- desktop 자원(local CLI, `~/.cogarch/*`) 호출하지 않음.
- 사용자 실측(5초 테스트 사람 5인)을 대신하지 않음.

## 라이선스 / 출처

- 원형: 2026-05-18 ~ 2026-05-20 의도적 수익 체계론 × fitCrafting 통합 교과서 사이클 (사용자 G + cogarch governance).
- 추출·잠금: 2026-05-20, `ops/cogarch_integration_cycle_pattern_20260520.md` 위에서 본 skill로 일반화.
