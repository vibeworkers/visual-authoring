# Tool Runtime Implementation Guide

## Principle

필요한 결과를 “만들어야 한다”는 문장만으로 닫지 않는다. 기능마다 실행 주체, 입력, 결과 파일 또는 URL, 검사 증거를 tooling_implementation에 기록한다. LLM은 어떤 기능이 필요한지 판단하지만, 이미지 변환·브라우저 검토·구조 검사는 code 또는 명시된 tool adapter가 실행한다.

scripts/visual-authoring-runtime(Windows: `visual-authoring-runtime.cmd`)은 Python 3.9+를 먼저 찾는다. 없으면 macOS Homebrew, Linux apt/dnf/yum/pacman/apk, Windows winget으로 설치를 시도한다. 설치는 네트워크와 권한을 쓸 수 있고, `VISUAL_AUTHORING_AUTO_INSTALL_PYTHON=0`이면 실행하지 않는다. 지원 패키지 관리자·권한·네트워크가 없으면 `blocked_missing_python` JSON으로 닫는다. 임의 URL 다운로드나 번들 외 실행 파일은 사용하지 않는다.

설치가 끝나면 scripts/portable_visual_runtime.py가 Python 표준 라이브러리만으로 local browser와 image converter를 탐색한다. browser/converter가 없을 때 `capture-web`과 `convert-image`는 다음 상태 기계를 실제로 실행한다.

1. 지원 실행 파일을 탐색한다.
2. 없으면 OS와 package manager를 판별해 명령 배열을 만든다.
3. 기본값에서 package manager 설치를 실행한다. macOS는 Homebrew, Linux는 apt/dnf/yum/pacman/apk, Windows는 winget만 사용한다.
4. 설치 직후 실행 파일을 다시 탐색하고, 발견되면 요청한 capture 또는 conversion을 자동으로 다시 실행한다.
5. 설치를 못 하거나 사용자가 끄면 `dependency_installation_required`, `dependency_installation_unavailable`, `dependency_installation_failed` JSON에 이유와 `manual_install_commands`를 남긴다.

`VISUAL_AUTHORING_AUTO_INSTALL_TOOLS=0` 또는 명령별 `--no-auto-install`은 3단계를 실행하지 않고 설치 안내만 낸다. `scripts/visual-authoring-runtime bootstrap`은 browser와 converter를 선제 설치·재탐색하며, `--dry-run`은 명령을 실행하지 않고 계획만 보인다. Linux 비관리자 계정에서는 `sudo -n`으로만 자동 시도해 숨은 비밀번호 입력을 피하고, 권한이 없으면 상호작용 터미널의 `sudo` 명령 또는 관리자/root shell용 명령을 제공한다. 어떤 경로도 `blocked_missing_browser`나 `blocked_missing_image_converter`를 반환하지 않는다.

## Browser runtime failure boundary

`probe`의 `dependencies_ready`는 browser와 converter 실행 파일이 보인다는 관찰일 뿐, capture가 성공했다는 증거가 아니다. `capture-web`은 기본 `headless_new`와 호환 `headless_compatibility`를 먼저 순서대로 실행하고, 사용자가 `--browser` 또는 `VISUAL_AUTHORING_BROWSER`로 하나를 고정하지 않았을 때만 발견된 다른 Chromium 계열 실행 파일도 우선순위대로 확인한다. `--no-sandbox`처럼 안전 경계를 낮추는 옵션은 추측으로 추가하지 않는다.

각 시도는 browser 경로, profile, 임시 경로를 가린 명령, stdout/stderr, 반환 코드 또는 signal, screenshot 생성 여부, DOM assertion 결과를 남긴다. screenshot과 대응 DOM assertion이 모두 통과한 뒤에만 요청한 output 경로로 이미지를 복사한다. 모두 실패하면 `browser_runtime_failed`와 `manual_runtime_guidance`를 반환한다. 이 상태는 browser가 없다는 뜻이 아니며, package manager 설치를 반복하지 않는다.

runtime이 제공하는 browser adapter는 **보강 경로**일 뿐 portable binary adapter를 몰래 대체하지 않는다. 그 adapter의 URL 정책이 목표 URL을 막으면 우회 URL·다른 제어 표면·raw CDP로 넘기지 않는다. 해당 작업 packet은 `blocked_tool_runtime`으로 남기고, 허용된 URL에서 별도 adapter가 낸 screenshot·DOM/상태 증거가 있을 때만 그 adapter를 기록한다.

## Required adapters

| 필요 기능 | 구현 adapter | 최소 실행 증거 |
| --- | --- | --- |
| 전략 콘셉트 | imagegen 또는 사용자가 제공한 이미지 + portable converter | 생성/변환 이미지 경로와 후보 ID |
| 목표 매체 preview | 코드 renderer | 렌더 파일 경로와 대상 표면 ID |
| HTML / web UI 전체 화면 | code render + portable runtime browser capture | 실행 URL, 전체 화면 capture, DOM text assertion |
| 상태·오류·반응형 확인 | portable runtime browser capture | state ID별 capture와 assertion 결과 |
| 구조·선택 packet | Python validator | 입력 packet과 pass_local / fail_local 결과 |

output_surface가 html 또는 web_ui면 portable_visual_runtime browser adapter가 기본 경로다. runtime이 제공하는 동등한 browser adapter는 해당 host가 목표 URL을 허용하고 screenshot·DOM/상태 증거를 실제로 낼 때만 기록할 수 있다. 단순 정적 source code, 부분 스크린샷, 말로 한 확인은 실제 browser evidence를 대신하지 않는다.

## Adapter packet

~~~json
{
  "tooling_implementation": {
    "status": "implemented",
    "adapters": [
      {"capability": "concept_image", "adapter": "imagegen", "implementation": "tool_call", "evidence_paths": ["decision-preview/editorial-concept.svg"]},
      {"capability": "target_surface_render", "adapter": "code_renderer", "implementation": "code", "evidence_paths": ["decision-preview/editorial-ui.svg"]},
      {"capability": "web_surface_inspection", "adapter": "portable_visual_runtime", "implementation": "code", "url": "http://localhost:3000", "evidence_paths": ["captures/desktop.png"], "assertions": ["primary-visible", "status-visible"]}
    ]
  }
}
~~~

웹이 아닌 산출물은 web_surface_inspection을 넣지 않고, 대신 해당 매체 renderer의 evidence를 기록한다. 실행 불가라면 status: blocked_tool_runtime과 blocker를 남긴다. 이 상태에서는 사용자 선택·릴리즈 완료를 선언하지 않는다.

## Portable browser execution

1. 코드로 목표 화면을 실행 가능한 URL로 연다.
2. `scripts/visual-authoring-runtime probe`로 현재 adapter 상태를 확인한다. 이 결과는 실행 파일 탐색값이며 capture pass가 아니다. 누락이 예상되면 `scripts/visual-authoring-runtime bootstrap --dry-run`으로 설치 계획을 먼저 검토하거나, `bootstrap`으로 설치·재탐색한다.
3. `scripts/visual-authoring-runtime capture-web <url> <png>`로 기본·행동·상태/오류·반응형 표면을 차례로 캡처한다. browser가 누락되면 같은 명령이 설치·재탐색 후 capture를 재시도한다. 발견된 browser가 실행에 실패하면 runtime은 안전한 headless profile과 다른 발견 후보를 제한적으로 시도하고, 시도 기록을 남긴다. 다른 번들 Python validator는 `scripts/visual-authoring-runtime run scripts/<validator>.py <args>`로 실행할 수 있다.
4. screenshot과 DOM 또는 상태 assertion이 모두 pass일 때만 각 표면의 evidence path를 artifact에 기록한다. 모두 실패하면 `browser_runtime_failed`; host adapter의 URL 정책이 막으면 `blocked_tool_runtime`으로 닫고 우회하지 않는다.
5. 비교 후보는 같은 route, viewport, 상태, 정보량으로 캡처한다.

브라우저 검사는 실제 렌더와 선언한 DOM/상태가 존재하는지 보는 local/runtime 증거다. 사용성, 선호, 이해, 행동 변화, 배포 승인을 증명하지 않는다. 이미지 생성 모델 자체는 이 패키지에 포함되지 않으므로, 모델이 없을 때는 제공 이미지 변환 또는 별도 imagegen owner로 정직하게 닫는다.
