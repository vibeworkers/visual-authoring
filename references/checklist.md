# Verification Checklist — Phase 5

빌드/저작 완료 후 확인한다. 공통 항목 + 사용한 Mode 블록을 전부 통과해야 닫는다.
(원형: `visual-implementation/references/checklist.md` C1~C9를 토큰 중립·모드 확장)

## 공통 (모든 산출물)

- [ ] **V1. 콘텐츠 적합성 우선** — 콘텐츠·독자 과업·행동 → 의미 관계/읽기 흐름 → 매체 구현 → geometry → render/native → human outcome 순서로 판정. 기준작 유사도를 상위 gate로 쓰지 않음
- [ ] **V2. 표현 시스템은 선택형 도구** — Carbon/Vivid/Brand/Editorial/Custom을 시각화 자체나 native medium과 혼동하지 않음
- [ ] **V3. 3축 선택 기록** — `content_visual_strategy`, `strategy_rationale`, `selected_expression_system`, `token_or_style_contract`, `medium_implementation_plan`, 열려 있던 후보의 `rejected_candidates`, `no_default_assertion: true`
- [ ] **V4. style materialization** — 웹/CSS는 선택한 namespace와 hardcoded hex/px 0을 검사. PPTX는 theme/master/layout/object style map으로 물질화되고 native를 token namespace로 쓰지 않음
- [ ] **V5. CSS namespace 혼용 0** — 같은 웹 화면에 두 namespace가 함께 등장하지 않음. PowerPoint native object는 namespace 혼용 대상이 아님
- [ ] **V6. label-masked 판독** — 라벨을 가려도 key meaning unit 3개+ 식별 가능 (미통과 시 라벨 추가가 아니라 visible cue·배치 수정)
- [ ] **V7. 5초/3초 테스트(proxy)** — 첫 화면이 무엇으로 읽히는지 기록. 사람 실측 전에는 `CONDITIONAL`/`candidate`
- [ ] **V8. evidence/claim vocabulary 분리** — evidence state(`observed_computation`/`inferred_proxy`/`calibrated_proxy`/`human_outcome`/`blocked_external`)와 visual claim class(`observable_proxy`/`inferred_risk`/`human_outcome_claim`)를 섞거나 서로 대체하지 않음
- [ ] **V9. 모바일 반응형** — 375px에서 텍스트 판독 가능, 가로 스크롤 없음
- [ ] **V10. reduced-motion** — `prefers-reduced-motion` 존중 (Vivid는 cinematic→base 강등)
- [ ] **V11. 대비** — 본문 WCAG AA(4.5:1)+, display 3:1+. 고채도/이미지 위 텍스트는 scrim/on-accent 경유
- [ ] **V12. prompt ledger** — 생성 이미지를 썼다면 model/prompt/output_path/integration_path/verification 5필드 존재
- [ ] **V13. Design Exploration Gate** — 표현 시스템/브랜드가 명시적으로 고정되지 않았고 선택이 결과를 바꾸면 3개 이상 비교. PPTX 지정 자체는 탐색 생략 사유가 아님
- [ ] **V14. Scene Specificity Gate** — 이미지 경로면 scene_subject/place/objects/action/viewpoint/text_policy/negative_prompt/integration_plan/proof_surface 존재, `could_apply_to_any_project=false`
- [ ] **V15. Retrospective Signal Gate** — 반복 리뷰 신호를 `default_bias`, `scene_generic`, `native_feature_gap`, `readability_gap`, `other` 중 하나로 분류하고 다음 수정 게이트에 연결
- [ ] **V16. Source Role Gate** — 원본 artifact가 있으면 `source_role`과 `source_contract`를 먼저 분류. 원본이 없으면 `skipped_no_original`
- [ ] **V17. 역할별 증거** — fidelity baseline만 source parity table을 요구. reference benchmark는 content-fit observation을 남기고 1:1 대조를 pass/improved gate로 쓰지 않음
- [ ] **V18. Strategy/Incident Loop 분리** — 저작은 intent→content architecture→3층 ledger→표현군 prototype→전체 제작 순서. binary isolation/XML/geometry 같은 국소 진단을 콘텐츠·시각 평가법으로 승격하지 않음
- [ ] **V19. Semantic Silhouette Diversity Gate** — 차분함·일관성·편집 가능성을 실루엣 반복의 근거로 쓰지 않음. 장형/다섹션 산출물은 관계 유형과 실루엣 가족을 분리한 manifest, 프로젝트별 diversity policy, validator 결과를 보유
- [ ] **V20. Cognitive Visual Encoding Gate** — 관계→추론 목표→후보 시각 문법→선택 근거→가시/억제 cue→읽기 경로를 기록. evidence state와 시각 claim class를 혼합하지 않고 사람 실측 전 human outcome을 확정하지 않음
- [ ] **V21. Fixed–Flexible–Decision Visual Support Convergence** — 패턴 활성화 시 현재 weak/strong scene을 다시 고르고, 표면이 아닌 지원 원리를 primary/secondary scene에 전이하며, 최소 5회 cycle ledger와 pattern guard를 남김. 편차 감소를 실루엣 평준화로 대체하지 않고 Fixed audit/content-fit/human evidence를 분리
- [ ] **V22. Artifact-Level System Lock / Open Materiality** — token/style namespace, typography hierarchy, spacing/density, component grammar, status semantics, accessibility/contrast를 artifact 단위로 잠금. 같은 레이아웃 반복을 일관성 증거로 쓰지 않고, LLM이 만들 수 있는 시각 표현을 finite whitelist로 제한하지 않으며 실제 제약과 선택 이유를 기록
- [ ] **V23. Scene-Centered Meaning Gate** — 이미지/SVG/native 모든 주요 의미 단위에 scene mode, entity/anchor, action/state change, 3초 core read, reader inference/action, non-label cue, deterministic meaning owner, lock 참조, materiality 후보, route를 기록
- [ ] **V24. Localization Reflow / Proof Freshness** — 번역·자연화·구체화된 visible/accessibility copy가 있으면 pending 상태 0, preserved facts, 영향 표면, geometry risk, stale proof, fresh target-medium evidence를 확인. overflow 0만으로 닫지 않음

## Mode L — Landing / Promo

- [ ] **L1. Full-bleed Hero** — Hero에 `max-width` 래퍼 없음. 내부 `.container`만 제한
- [ ] **L2. 브랜드 가시성** — 첫 뷰포트에서 브랜드/제품명이 가장 큰 텍스트
- [ ] **L3. 섹션 단일 책임** — 각 `<section>` 역할 1개 (설명/증명/심화/전환)
- [ ] **L4. 모션 최소 2개** — fadeInUp(진입) + scroll reveal
- [ ] **L5. 자립형 HTML** — 더블클릭 렌더링, 외부 참조 없음 (Google Fonts만 예외)
- [ ] **L6. 한국어 렌더링** — Noto Sans KR(Carbon)/Pretendard(Vivid) fallback 선언, 한글 미깨짐
- [ ] **L7. (시네마틱 시) Immersion Plan** — 핵심 메시지·story beat·시각 인과·주의 경로·관점 앵커 기록

## Mode A — App UI

- [ ] **A1. 절제 레이아웃** — 카드 모자이크 없음. 평면 + 구분선·여백·정렬
- [ ] **A2. Utility copy** — hero 카피 없음. 방향감·상태·행동 문구만
- [ ] **A3. 에러 번역** — raw 서버 에러가 UI에 노출되지 않음, field-local inline 에러
- [ ] **A4. idempotent submit** — 중복 제출 방지, 입력 formatting(표시≠저장)
- [ ] **A5. `bx--` 클래스 미사용**

## Mode S — Slide / PPTX

- [ ] **S1. Outline Notes 선행** — 빌드가 Phase 1 산출에서만 나옴
- [ ] **S2. PresentationML 검증** — OPC/DrawingML/notes/theme/layout 스키마 통과
- [ ] **S3. PowerPoint open check** — 실제 열림 + no_recovery_dialog. **rebuild 후 이전 증거는 stale**
- [ ] **S4. 레이아웃 요소 계산 흔적** — element_tradeoff/placement/front_back_order/reading_order/native_object_order/overlap_risk + 선언한 geometry constraints
- [ ] **S5. surface 6분리** — learner_facing/instructor/production_source/evidence/render_proof/handoff를 blended "done"으로 합치지 않음
- [ ] **S6. Native Medium Capability Scan** — tool_target/source_format/delivery_format/native_features_required/image_layer_policy/editable_object_policy/speaker_notes_policy/manual_open_check 기록
- [ ] **S7. 편집 가능한 PPTX 기능** — master/layout/theme/placeholders/title placeholder/speaker notes/editable tables-charts-shapes-connectors/grouping-order/alt text-read order/animations-transitions가 필요 범위만큼 네이티브 객체로 존재
- [ ] **S8. Source-to-Native Transfer Plan** — 텍스트/표/차트/IA/프로세스/노트는 native화, 복잡한 장면·사진·질감은 image layer 유지 등 의미와 fit 기준의 판단표 존재
- [ ] **S9. Native Object Intent Plan** — unit_id/semantic_role/criticality/native_requirement/expected_native_type/planned_object_names/edit_boundary/group/z-order/read-order/required_relations/raster exception 기록
- [ ] **S10. Geometry Audit** — PPTX·intent plan SHA-256, threshold profile, object inventory, `out_of_bounds_non_bleed_count`, `unintended_overlap_count`, `max_alignment_error_pt`, `max_spacing_deviation_ratio`, `detached_required_connector_count`, `object_density` 보고
- [ ] **S11. Semantic Coverage** — critical missing/type/relation/read-order blocker 0, `critical_native_coverage=1.0`와 `required_relation_coverage=1.0` 또는 분모 0이면 `not_applicable`
- [ ] **S12. Threshold/Waiver Policy** — tolerance는 빌드 전에 프로젝트가 근거와 함께 선언. waiver가 finding을 삭제하거나 pass로 바꾸지 않음
- [ ] **S13. Evidence Freshness/Separation** — rebuild 후 geometry/native/render/manual-open 증거를 전부 stale 처리. geometry proxy를 좋은 디자인·콘텐츠 적합성·학습성과로 승격하지 않음
- [ ] **S14. Native PowerPoint Intent** — master/layout/theme/placeholders, semantic object names/groups, connectors, tables/charts, notes, accessibility, 필요한 animation을 의미와 발표 행동에 맞게 의도적으로 사용
- [ ] **S15. Expression-Family Prototype Gate** — 전체 덱 제작 전에 materially different 표현군 대표를 묶은 소형 PPTX가 content-fit review와 fresh PowerPoint `no_recovery_dialog`를 통과. 실패 시 source를 고치고 이후 proof를 stale 처리
- [ ] **S16. Executable Scale Authorization** — 프로젝트 prototype manifest가 `scripts/validate_authoring_prototype_gate.py --require-authorized`를 통과하기 전 전체 덱 빌드를 차단. validator 결과를 미적 품질·학습성과 판정으로 승격하지 않음
- [ ] **S17. Silhouette Budget Validation** — prototype이 실제 silhouette family를 포함하고, 최종 `visual-silhouette-manifest.json`이 가족 수·연속 반복·지배 비율·의미 시각화 비율을 선언값대로 통과. rebuild 후 이전 결과는 stale
- [ ] **S18. Cognitive Encoding Schema v2** — 신규/전면 재구성 장형 덱은 `schema_version: 2`와 슬라이드별 cognitive encoding packet을 갖추고 `--require-cognitive-encoding` 통과. legacy v1 결과는 과거 감사용이며 새 확장 승인에 사용하지 않음
- [ ] **S19. Geometry/Native Convergence Boundary** — 객체 거리·정렬·겹침·connector 계산은 먼저 선언한 의미 관계와 정확한 구현을 검증하는 데만 사용. geometry/native pass를 디자인·콘텐츠 적합성·학습성과 판정으로 승격하지 않고 source rebuild 뒤 proof freshness를 다시 확인

## Mode V — Visual Document 정규화

- [ ] **N1. 의미 단위표** — meaning_unit/visible_cue/masked_read_criterion/risk/recovery_action
- [ ] **N2. 레거시 alias 정리** — 과도기 `--primary` 등이 최종본에서 제거(또는 토큰 참조로만 잔존)
- [ ] **N3. 최소 변경** — 치환 diff가 토큰 외 스타일 의미를 바꾸지 않음

## 검증 명령어

```bash
# V1: hardcoded hex 검사
grep -nE '#[0-9a-fA-F]{3,8}' output.html | grep -v ':root' | grep -v 'var(--'

# V2: 혼용 검사 — 같은 화면에서 둘 이상 0이 아니면 FAIL
grep -c -- '--cds-' output.html; grep -c -- '--viv-' output.html

# V3/V13: stale phrase 검사 — active skill/reference에서 legacy binary/default-selection phrase가 0이어야 함
rg -n '<legacy-binary-or-default-selection-regex>' SKILL.md references

# S9-S11: PPTX native object/geometry/semantic coverage 감사
scripts/visual-authoring-runtime run scripts/audit_pptx_native_objects.py --pptx deck.pptx --intent native-object-intent-plan.json

# S15-S16: 표현군 prototype 기록 및 전체 확장 승인
scripts/visual-authoring-runtime run scripts/validate_authoring_prototype_gate.py project-gate.json --require-authorized

# V19/S17: 기존 관계 유형·실루엣 다양성 예산 감사
scripts/visual-authoring-runtime run scripts/validate_visual_silhouette_budget.py visual-silhouette-manifest.json

# V20/S18: 신규/전면 재구성 장형 덱의 인지 시각 인코딩 계약
scripts/visual-authoring-runtime run scripts/validate_visual_silhouette_budget.py visual-silhouette-manifest.json --require-cognitive-encoding

# V22-V24: artifact-level system lock, all-route scene packet, localization reflow freshness
scripts/visual-authoring-runtime run scripts/validate_scene_materiality_reflow_contract.py scene-materiality-reflow-contract.json

# A5: bx-- 클래스 검사
grep -n 'bx--' output.html

# L5: 외부 참조 검사 (fonts.googleapis.com만 허용)
grep -nE 'href="|src="' output.html | grep -v 'fonts.googleapis.com' | grep -v '#'
```
