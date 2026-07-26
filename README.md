# Visual Authoring

`visual-authoring`은 문서·슬라이드·랜딩 페이지·앱 UI 등 여러 매체의 시각 저작을 한 흐름으로 다루는 통합 스킬이다. 무엇을 왜 보여줄지 먼저 정하고, 콘텐츠 적합성을 검토한 뒤, 장면과 의미·시스템·매체 구현을 분리해 만들며, 구조·렌더·native runtime·사람 증거를 서로 다른 장부로 확인한다.

## 정본과 공개 저장소

- **전역 정본**: 이 디렉터리의 `SKILL.md`
- **전역 진입점**: `~/.cogarch/skills/visual-authoring/`
- **공개 저장소**: [vibeworkers/visual-authoring](https://github.com/vibeworkers/visual-authoring)
- **이전 관리 체크아웃**: `projects/visual-authoring/`

전역 정본이 런타임에서 사용하는 유일한 스킬이다. `projects/visual-authoring/`는 이전에 GitHub 게시를 위해 사용한 독립 Git 체크아웃이며, 두 번째 런타임 스킬이 아니다.

전역 정본과 GitHub 저장소 사이에는 동기화 계약이 없다. 둘 중 한쪽의 변경이 다른 쪽을 자동·반자동으로 바꾸지 않으며, 이후 게시나 역이관은 별도의 명시적 결정으로만 한다.

## 패키지 구성

| 경로 | 역할 |
|---|---|
| `SKILL.md` | 통합 저작 파이프라인과 런타임 계약 |
| `agents/openai.yaml` | 스킬 표시 이름과 기본 진입점 |
| `references/` | 저작·리뷰·PPTX·증거 계약의 상세 기준 |
| `scripts/` | 구조와 native object 검증 도구 |
| `fixtures/`, `evals/` | 검증 입력과 평가 자료 |
| `_absorbed/` | 흡수 전 다섯 스킬의 읽기 전용 provenance 보관본 |

`_absorbed/`의 보관본은 `SKILL.provenance.md`와 `openai.provenance.yaml` 이름을 쓴다. 내용과 계보는 보존하지만 표준 스킬 탐색 진입점으로는 노출하지 않는다.

## 변경과 게시 경계

1. 전역 정본은 이 디렉터리에서 독립적으로 관리한다.
2. GitHub 저장소는 독립적인 공개 프로젝트로 관리한다.
3. 한쪽의 내용을 다른 쪽에 반영하려면 대상·방향·검증 범위를 별도로 정한다.

자동·반자동 양방향 복사는 하지 않는다. 과거의 연결 정보는 현재 운영 계약이 아니며, `projects/visual-authoring/` 안의 Git 이력은 전역 정본의 이력으로 간주하지 않는다.

## 검증

전역 정본과 관리 체크아웃 각각에 다음 검증을 실행한다.

```sh
python3 /Volumes/Extend/.codex-relocated/skills/generate-skill/scripts/quick_validate.py <skill-directory>
python3 /Volumes/Extend/.codex-relocated/skills/generate-skill/scripts/audit_three_layer_separation.py <skill-directory>
```

`quick_validate.py`는 패키지 형식을 확인하고, 구조 감사는 Fixed·Flexible·Decisional 레이어가 섞이지 않았는지 보조적으로 확인한다. 렌더 성공이나 static 검사만으로 사람의 편집 가능성·native runtime·사용자 결과를 증명하지 않는다.

## 라이선스

별도 표기가 없는 이 디렉터리의 원저작물은 [CC BY-NC 4.0](LICENSE)을 따른다. 제3자 원본·상표·인물·생성 이미지에는 자동 적용하지 않으며, 각 권리 조건을 별도로 기록해야 한다.
