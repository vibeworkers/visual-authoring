# PowerPoint Native Conformance and Source-Level Self-Remediation

이 계약은 PPTX가 열릴 때도 있고 복구 대화상자를 띄울 때도 있는 상태를 줄이기 위해 쓴다. 목적은 모든 PowerPoint 기능을 기계적으로 켜는 일이 아니다. 덱에 적용 가능한 핵심 기능을 빠짐없이 검토하고, 각각을 `used`, `intentionally_not_used`, `not_applicable` 중 하나로 선언한 뒤 실제 패키지와 대조하는 일이다.

## PowerPoint Capability Decision Catalog

빌드 전에 `pptx-native-conformance-contract.json`을 만든다. 다음 core capability는 빠짐없이 한 번씩 결정한다.

| 기능 | `used`일 때 확인할 것 | 비사용이 허용되는 경우 |
| --- | --- | --- |
| `slide_master_layout_theme` | master, layout, theme part | 한 장짜리 이미지 배포물처럼 PPTX가 delivery format이 아닐 때 |
| `theme_font_scheme` | major/minor Latin·East Asian font face | target medium이 PPTX가 아닐 때 |
| `title_placeholder` | 모든 슬라이드의 native title placeholder | custom layout이 placeholder를 안전하게 만들 수 없고, `navigation.title_source`가 이름 있는 native text shape를 한 장에 하나씩 가리킬 때 |
| `outline_navigation` | native section list, TOC, 순서화된 title story | 한 장짜리 독립 슬라이드일 때 |
| `automatic_slide_number` | master/layout의 `sldNum` placeholder 또는 native slide-number field | 페이지 개념이 없는 단일 장면일 때 |
| `speaker_notes` | notes part | 발표·진행 정보가 전혀 없을 때 |
| `native_text_in_shapes`, `editable_shapes` | text shape와 editable shape | 의미가 없는 장식 배경만 있을 때 |
| `connectors`, `editable_tables`, `editable_charts` | 실제 connector/table/chart object | 관계·표·데이터가 없을 때 |
| `object_naming_reading_order`, `accessibility` | semantic Selection Pane names, alt/read order | 해당 객체가 없을 때 |
| `hyperlinks_navigation`, `animations_transitions`, `media` | native feature node/relationship | 독자 과업이나 발표 행동에 필요 없을 때 |

`intentionally_not_used`와 `not_applicable`도 반드시 `decision_reason`을 가진다. 기능 수를 늘리기 위해 SmartArt, 애니메이션, 미디어, 차트를 넣지 않는다. 반대로 의미·편집·진행에 필요한 기능은 “디자인이 어려움”을 이유로 이미지로 대체하지 않는다.

## Native vs Raster Decision

기본값은 **의미와 수정 가치가 높은 것은 native**다. 제목, 목차, 자동 쪽번호, 표, 차트, 프로세스, 관계선, 라벨, 콜아웃, 노트, 이동 링크, 객체 이름은 PowerPoint가 제공하는 객체로 만든다.

이미지는 다음처럼 native가 오히려 의미를 약하게 만들 때 사용한다.

- 사진적 장면, 생성 이미지, 복잡한 일러스트, 질감처럼 장면 자체를 유지해야 할 때
- 독자가 바꿀 필요가 없는 장식적 배경일 때
- 글꼴을 이미지로 연출해야만 의도한 시각적 장면이 성립할 때

이미지 예외는 `raster_exceptions`에 object name, semantic role, 왜 image가 필요한지, 동등한 텍스트를 남긴다. 글꼴을 이미지로 쓴 경우에도 `equivalent_text`를 남겨 검색·접근성·후속 수정의 경계를 잃지 않는다. 이미지 위의 의미 라벨·화살표·조건·순서는 native layer가 소유한다.

## Default PowerPoint Settings

모든 설정은 값만 두지 말고 `intentional_settings`에서 이유까지 기록한다. 최소 항목은 `slide_size`, `theme_font`, `slide_number`, `text_frame_default`, `outline_navigation`이다.

- 기본 테마 글꼴은 `Pretendard` 계열이다. theme의 major/minor font에서 Latin과 East Asian face를 함께 지정한다. 실제 설치 여부와 대체 렌더링은 각 실행 환경의 native-open 증거로 별도로 확인한다.
- 도형 안의 기본 텍스트는 가로 가운데, 세로 가운데다. PresentationML에서는 기본적으로 `a:pPr@algn="ctr"`, `a:bodyPr@anchor="ctr"`을 쓴다.
- 설명문·표·목차처럼 왼쪽 정렬이 의미상 더 자연스러운 경우에는, 해당 object의 semantic name과 이유를 `text_frame_default.exceptions`에 선언한다. 이름 없는 예외는 허용하지 않는다.
- 쪽번호는 일반 텍스트로 직접 입력하지 않는다. `slide_number.mode: automatic_powerpoint`와 native number placeholder/field를 사용한다.

## Outline, TOC, and Direction

프레젠테이션의 방향은 제목과 목차를 순서대로 읽는 것만으로도 보이게 만든다. `navigation`에는 다음을 둔다.

1. `direction_statement`: 제목 흐름이 독자를 어디로 데려가는지 한 문장으로 적는다.
2. `sections`: section id, title, start slide을 순서대로 적는다.
3. `title_sequence`: 실제 native title source와 일치하는 슬라이드별 제목을 순서대로 적는다. 기본 source는 native title placeholder다.
4. `toc_entries`: 어느 TOC 슬라이드에 어느 section title이 나타나는지 적는다.

정적 텍스트만으로 목차를 흉내 내지 않는다. PowerPoint native section list, title source, TOC native text, automatic slide number를 함께 쓴다. 기본 title source는 title placeholder다. 다만 placeholder를 source 단계에서 안전하게 만들 수 없는 custom layout은 `title_placeholder: intentionally_not_used`와 함께 `navigation.title_source`에 `mode: named_native_shape`, `object_name_prefix`, 이유를 적는다. 해당 prefix와 맞는 수정 가능한 native text shape가 매 슬라이드에 정확히 하나 있어야 한다. 새 슬라이드를 끼우거나 순서를 바꾸면 title story, section start, TOC, 쪽번호 증거를 모두 stale로 처리한다.

## Contract Shape

아래는 최소 형태다. 프로젝트의 실제 slide title, section, raster reason, 기능 판단은 이 구조 안에서 바꾼다.

```json
{
  "contract_version": "1.0",
  "target_medium": "powerpoint",
  "source_family_id": "project-fresh-v1",
  "source_lineage": {
    "recovery_lineage_policy": "reject_as_source",
    "recovery_incident": false
  },
  "capability_catalog": [
    {
      "id": "automatic_slide_number",
      "status": "used",
      "decision_reason": "the deck has multiple pages and needs native navigation"
    }
  ],
  "theme_font": {
    "default_family": "Pretendard Variable",
    "latin_family": "Pretendard Variable",
    "east_asian_family": "Pretendard Variable"
  },
  "navigation": {
    "direction_statement": "From the reader problem to the decision and next action.",
    "sections": [{"section_id": "why", "title": "Why", "start_slide": 1}],
    "title_source": {"mode": "native_title_placeholder"},
    "title_sequence": [{"slide_number": 1, "title": "Start with the reader"}],
    "toc_entries": [{"toc_slide_number": 1, "section_title": "Why"}]
  },
  "slide_number": {"mode": "automatic_powerpoint", "show_on_title_slide": false},
  "text_frame_default": {
    "horizontal_alignment": "center",
    "vertical_anchor": "middle",
    "exceptions": [{"object_name": "Body: Evidence", "reason": "long evidence needs left scanning"}]
  },
  "intentional_settings": [
    {"setting_id": "theme_font", "value": "Pretendard Variable", "reason": "default Korean and Latin family"}
  ],
  "raster_exceptions": [
    {
      "object_name": "Scene Base: Field Photo",
      "semantic_role": "photographic context",
      "reason": "the photographed setting is not an editable diagram",
      "equivalent_text": "Field team reviewing the decision board"
    }
  ]
}
```

실제 계약은 모든 core capability와 모든 required intentional setting을 포함해야 한다. 코드가 이 표본의 축약형을 pass로 간주하지 않는다.

## Source-Level Self-Remediation

`self-repair`는 PPTX package를 몰래 고치는 의미가 아니다. 복구 이력이 있는 PPTX를 ZIP/XML patch, conversion, PowerPoint 재저장으로 살리는 것은 다음 후보를 다시 오염시킨다.

```text
exact PPTX + conformance contract
  -> deterministic package/feature audit
  -> native-object geometry audit (including undeclared text overlap)
  -> repair_required report + source-level repair plan
  -> update authored source / manifest / compiler
  -> new source_family_id + fresh build
  -> rerun audits, render proof, and manual PowerPoint open
```

geometry audit가 `unplanned_text_overlap` 또는 선언한 `separate` 위반을 찾으면, PPTX XML을 덮어쓰지 않는다. 겹친 object name·좌표·교차 비율을 report에 남기고, 카드 폭·행 위치·여백처럼 **저작 원본의 geometry 규칙**을 고친 뒤 새 source family로 빌드한다. 의도한 text-on-text 연출만 `native-object-intent-plan.json`의 `overlap_exceptions`에 두 이름과 이유를 적어 예외로 선언한다.

상태는 다음처럼 읽는다.

| 상태 | 의미 | 다음 행동 |
| --- | --- | --- |
| `pass_local` | 선언한 package conformance를 통과함 | 동일 hash를 Microsoft PowerPoint에서 열어 별도 native-runtime 증거를 남김 |
| `repair_required` | source에서 고칠 수 있는 위반이 있음 | repair plan의 source action을 반영해 fresh family로 재빌드 |
| `blocked_missing_contract` | 의도·예외·설정이 선언되지 않았거나 schema가 깨짐 | contract를 먼저 완성 |
| `blocked_recovery_incident` | recovery incident가 source로 들어오려 함 | incident artifact를 동결하고 새 authored source family 시작 |

검사기는 PPTX를 절대 수정하지 않고 report와 repair plan만 쓴다. `pass_local`은 Microsoft PowerPoint open, 실제 selection/edit, 가시 품질, 독자 이해·행동 변화를 뜻하지 않는다.

## Run

```bash
scripts/visual-authoring-runtime run scripts/validate_pptx_native_conformance.py \
  --pptx build/deck.pptx \
  --contract pptx-native-conformance-contract.json \
  --report build/pptx-native-conformance-report.json \
  --repair-plan build/pptx-native-repair-plan.json
```

도구 자체의 valid/invalid fixture 검사는 다음으로 실행한다.

```bash
scripts/visual-authoring-runtime run scripts/validate_pptx_native_conformance.py --self-test
```

## Evidence Boundary and Source Notes

- master/layout/theme은 PresentationML의 반복 구조이고, slide number는 header/footer 또는 placeholder/field 구조로 다룬다. [Microsoft PresentationML structure](https://learn.microsoft.com/en-us/office/open-xml/presentation/structure-of-a-presentationml-document), [PowerPoint HeaderFooter](https://learn.microsoft.com/en-us/office/vba/api/PowerPoint.HeaderFooter)
- PowerPoint text vertical anchor는 middle을 지원하고 DrawingML paragraph alignment는 center를 표현한다. [TextFrame.VerticalAnchor](https://learn.microsoft.com/en-us/office/vba/api/powerpoint.textframe.verticalanchor), [DrawingML ParagraphProperties](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.paragraphproperties?view=openxml-3.0.1)
- theme font scheme은 major/minor font pair를 소유한다. [DrawingML FontScheme](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.fontscheme?view=openxml-3.0.1)

위 문서는 native package feature의 구조적 경계만 다룬다. 실제 PowerPoint open, 사람의 편집 경험, 이해·행동 변화는 별도 증거다.
