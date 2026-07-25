# Slide Authoring — Phase 1 상세 인덱스

Phase 1(인지적 문서/슬라이드 저작)의 상세 계약은 아래 원형 문서들이 소유한다.
(원형: `document-slide-authoring-agent-system` — 전문 스냅샷 `../_absorbed/document-slide-authoring-agent-system/`)

## 로드 맵 — 무엇이 필요할 때 어느 파일인가

| 필요한 것 | 파일 |
|---|---|
| 인지적 저작 패킷 (R→P→M→W→A), reader_situation/cognitive_task/desired_action/semantic_fit/evidence_boundary 필드 정의, unfolding 해석(folded_unit→weakness_diagnosis→CTA 질문→unfolding_trace) | `cognitive-authoring-process.md` |
| 순서 계약: `course-flow-map.md → slide-planning-map.json → symbol-inventory.json → semantic-design-system.json` 각 파일의 필수 필드와 게이트 | `course-flow-to-design-system-sequence.md` |
| Outline Notes 게이트 필드, Storyline/Readability 6검사(Title-Only Story / Assertion-Evidence / One-Beat / 5-Second Scan / Cognitive-Load / Evidence-Boundary), 레이아웃 요소 계산(element_tradeoff/placement/front_back_order/reading_order/native_object_order/overlap_risk) | `slide-authoring-methods.md` |
| Semantic Staging design brief — 주의·호기심·유도 읽기·발화 흐름·근거 공개·행동 출구 + 설계 자유 경계(디자인을 고정하지 않으면서 의미 단계만 고정) | `semantic-staging-design-framework.md` |
| PPTX 표준 XML 생성(PresentationML/OPC/DrawingML), notes/theme/layout 검증, PowerPoint open check 릴리즈 게이트, rebuild-stale 규칙 | `pptx-standard-xml-generation.md` |
| 의미 단위→native object 의도, geometry relation, semantic coverage, threshold/waiver, 계산형 audit | `pptx-native-object-authoring.md` |
| Session-feedback 패턴 게이트(반복 리뷰 코멘트 → 재사용 검사) + artifact-surface 6분리(learner_facing / instructor_facilitator / production_source / evidence_fact_table / render_native_proof / delivery_handoff) | `session-feedback-and-surface-gates.md` |

## Native Medium Capability Scan

PPTX/Google Slides/iA Presenter 같은 네이티브 발표 매체는 PNG/PDF/스크린샷 렌더만으로 통과하지 않는다.
렌더 증거는 시각 증거이고, 편집성·발표성·협업성 보존 증거가 아니다.

원본 PPTX/이미지/HTML/PDF가 기준이면 `source-first-regeneration.md`를 먼저 로드한다. Native Medium Capability Scan은 원본 해체 결과를 목표 매체의 기능 요구로 바꾸는 단계다. 즉, 모든 것을 도형으로 바꾸는 단계가 아니라 의미·fit·수정 가능성이 큰 요소만 native로 전이하고, 형태 보존 가치가 큰 장면은 image layer로 유지하는 판단을 문서화하는 단계다.

작업 시작 전에 아래 packet을 먼저 고정한다:

```
tool_target: pptx | google_slides | ia_presenter | ia_writer | pdf_only | html
source_format: markdown | pptx_xml | google_slides_native | html | other
delivery_format: pptx | google_slides | pdf | html | images | markdown
native_features_required:
  - slide_master_layout_theme
  - theme_font_scheme
  - title_placeholder
  - outline_navigation
  - automatic_slide_number
  - speaker_notes
  - native_text_in_shapes
  - editable_shapes
  - connectors
  - editable_tables
  - editable_charts
  - object_naming_reading_order
  - alt_text_read_order
  - hyperlinks_navigation
  - animations_transitions
  - media
capability_decision_catalog: pptx-native-conformance-contract.json
theme_font_policy: Pretendard family for major/minor Latin and East Asian faces
outline_navigation_policy: native_sections + TOC_native_text + ordered_title_story
slide_number_policy: automatic_powerpoint | not_applicable-with-reason
shape_text_default: horizontal_center + vertical_middle | named-exception-with-reason
image_layer_policy: generated_scene_base | native_shapes_only | hybrid | none-with-reason
editable_object_policy: all_key_structures_editable | intentional_raster_with_reason
image_typography_policy: native_text_default | raster_exception_with_equivalent_text
speaker_notes_policy: required | optional | not_applicable
manual_open_check: required | not_applicable
style_materialization: pptx_theme | slides_theme | tool_native_style_map | not_applicable
native_object_intent_plan: native-object-intent-plan.json | not_applicable-with-reason
native_object_audit: native-object-audit.json | not_applicable-with-reason
pptx_native_conformance_report: pptx-native-conformance-report.json | not_applicable-with-reason
pptx_native_repair_plan: pptx-native-repair-plan.json | not_applicable-with-reason
visual_silhouette_manifest: visual-silhouette-manifest.json | not_applicable-with-reason
```

`Native Medium Capability Scan`은 기능 목록을 정하고, `Native Object Intent Plan`은 각 의미 단위를 어떤 객체로 왜 구현하는지 정한다. 둘은 대체 관계가 아니다. PowerPoint를 목표로 하면 다음 순서로 실행한다.

1. 의미 단위와 `criticality`를 정한다.
2. `expected_native_type`, semantic object name, edit boundary, group/z-order/read-order를 정한다.
3. `separate/contain/overlay/connect/align/gap` 관계와 프로젝트 tolerance를 정한다.
4. image/native/hybrid 예외와 waiver를 정한다.
5. PPTX를 빌드한다.
6. `scripts/audit_pptx_native_objects.py`로 실제 object/bbox/relation/coverage를 계산한다.
7. `scripts/validate_pptx_native_conformance.py`로 capability catalog, theme font, title/section/TOC/automatic number, default shape-text alignment, raster exception을 실제 package와 비교한다. `repair_required`이면 PPTX를 patch하지 말고 source family를 새로 빌드한다.
8. render proof, fresh PowerPoint open, 실제 selection/edit proof를 별도로 닫는다.

장형/다섹션 덱은 슬라이드별 `relationship_type`과 `silhouette_family`를 저작 단계에서 함께 기록한다. 색·폰트·accent가 달라도 공간 관계와 읽기 경로가 같으면 같은 가족이다. 반복이 학습 행동에 유익한 워크시트나 상태 변화 장면은 예외로 둘 수 있지만 `diversity_exception`에 이유를 남긴다. 구현 전에 `visual-silhouette-manifest.json`을 만들고, 표현군 prototype은 manifest의 실제 가족을 대표해야 한다.

의미 그룹의 모든 간격을 기계적으로 같게 만들지 않는다. 코드는 authoring plan에서 선언한 intra-group/inter-group/title-body 관계의 목표값과 실제값 사이의 편차를 계산한다. intent plan이나 목표 관계 없이 계산한 “균일도 점수”는 시각적 개선 증거가 아니다.

PPTX 경로의 최소 native feature preflight:

| 항목 | 통과 기준 |
|---|---|
| slide master/layout/theme/placeholders | 표지·본문·섹션·감사 슬라이드가 master/layout으로 구분됨 |
| PowerPoint capability decision catalog | 모든 core feature가 `used`/`intentionally_not_used`/`not_applicable`와 이유로 한 번씩 결정됨 |
| Pretendard theme font | major/minor Latin·East Asian 기본 글꼴이 Pretendard 계열이고 actual native runtime 대체 여부는 별도 증거 |
| title placeholder | 각 슬라이드 title placeholder 또는 명시적 slide title 존재 |
| outline/TOC/title story | native section list, TOC native text, ordered title sequence를 순서대로 읽으면 방향이 보임 |
| automatic slide number | 수동 숫자 text가 아니라 PowerPoint-native `sldNum` placeholder 또는 field 사용 |
| speaker notes | 강의 진행에 필요한 노트가 notes part에 존재 |
| editable tables/charts/shapes/connectors | 핵심 표·도형·화살표가 이미지로만 박제되지 않음 |
| native shape text default | 도형 텍스트는 가운데/중간 정렬, 좌측 등 예외는 semantic object name과 reason으로 선언 |
| grouping/order/align/distribute | 객체 순서와 그룹이 사람 편집에 맞게 정리됨 |
| alt text/read order | 주요 이미지·도형·차트의 접근성 설명과 읽기 순서 기록 |
| animations/transitions | 의도한 발표 흐름이 있으면 네이티브 기능으로 기록, 없으면 no-animation 사유 |
| chart/table editability | 차트·표가 있으면 PowerPoint에서 편집 가능한 구조 또는 의도적 raster 사유 |
| semantic object naming | Selection Pane/XML object name이 의미 단위와 연결되고 자동 이름만으로 닫지 않음 |
| Native Object Intent Plan | critical 의미 단위의 native type, edit boundary, group/z/read order, geometry relation, raster exception 기록 |
| geometry/native audit | PPTX와 intent plan hash가 기록된 fresh audit, exact-zero blocker와 coverage 보고 |
| native conformance / self-remediation | actual PPTX와 contract의 feature/font/navigation/text/raster 규약을 비교. 위반 시 source-only repair plan, recovery artifact patch 금지 |
| manual PowerPoint open check | 실제 PowerPoint 열림, no_recovery_dialog. rebuild 후 이전 증거는 stale |
| semantic silhouette diversity | relationship/silhouette manifest, 프로젝트 policy, 실행형 validator 통과. 차분함을 반복 레이아웃의 근거로 쓰지 않음 |

## 스캐폴드 스크립트

새 프로젝트에 저작 에이전트 시스템 골격을 이식할 때:

```bash
node scripts/portable_agent_system.js scaffold --target <project-dir>   # 골격 생성 (기존 파일 미덮어씀; --force 시만 덮음)
node scripts/portable_agent_system.js check   --target <project-dir>   # 순서·필드 계약 검사
scripts/visual-authoring-runtime run scripts/audit_pptx_native_objects.py --pptx <deck.pptx> --intent <native-object-intent-plan.json>
```

정확한 서브커맨드·옵션은 스크립트 헤더 주석이 정본이다 (`node scripts/portable_agent_system.js --help`).

## Phase 1 탈출 게이트 (요약)

1. 저작 패킷 필수 필드 고정 (`reader_situation`, `cognitive_task`, `desired_action`, `semantic_fit`, `evidence_boundary`, `output_route`, `verification_surface`)
2. 순서 계약 4파일이 존재하고 상호 참조가 닫힘 (디자인 시스템은 앞 3개에서 파생 — 먼저 고르지 않음)
3. Outline Notes 존재 (없으면 시각화 진입 금지, writing으로 복귀)
4. Storyline/Readability 6검사 통과 — 단 이것은 proxy 판정이며 human outcome이 아님
5. (PPTX 경로) Native Medium Capability Scan + Native Object Intent Plan + PowerPoint native conformance contract + 레이아웃 요소 계산 완료 후에만 객체 배치
6. (PPTX 경로) native-object audit와 native conformance report가 hash·객체·관계·capability/font/navigation/text/raster status를 보고하고 exact-zero blocker와 source-only remediation boundary를 닫음. 계산 결과는 content-fit/human-outcome proof가 아님
7. (원본 경로) source role을 분류. fidelity baseline만 Source Decomposition Packet + Source-to-Native Transfer Plan + source parity target 고정
8. (장형/다섹션 경로) `visual-silhouette-manifest.json`과 표현군 prototype coverage를 잠그고 validator 통과
