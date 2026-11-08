# 설치와 스킬

Codex 또는 Claude Code에 플러그인을 설치하거나 필요한 스킬 폴더를 직접 복사합니다.
Mac 앱 개발 예제는 [macOS 앱](#purpose-mac), 일반적인 개발 절차는 [제품 개발](#purpose-product)에서 확인할 수 있습니다.

<!-- skill-downloads -->

## 설치 전 준비

Codex 또는 Claude Code를 설치하고, 본인 계정으로 로그인한 상태에서 시작합니다.
플러그인 설치 명령은 터미널에서 실행하고, 스킬 사용 예시는 에이전트 대화창에 입력합니다.
스킬은 작업 절차를 설명하는 파일입니다.
모델 이용권, API key, Python, Node.js, Playwright 같은 실행 도구는 별도로 준비해야 합니다.
사용할 도구와 데이터의 이용 범위를 확인하고, 예제에는 공개 데이터나 가상 데이터를 사용합니다.

## 개발과 운영에서 고르기

작업에 맞는 스킬을 이름으로 지정합니다.
운영 스킬을 설치해도 서비스나 계정에 접근할 권한이 생기지는 않습니다.
조사, 변경 준비, 실제 배포 중 어디까지 요청하는지 함께 알려 줍니다.

| 작업 | 사용할 스킬 |
| --- | --- |
| 의존성 업데이트와 CI 점검 | `adopt-dependency`, `repo-ci-baseline` |
| 브라우저 테스트와 개인정보 기록 점검 | `nextjs-playwright-e2e`, `frontend-rum-privacy` |
| 장애 조사와 관측 도구 연결 | `incident-triage`, `observability-onboarding` |
| 서비스 버전 업데이트 준비 | `bump-selfhosted-app` |
| 커밋과 worktree 정리 | `commit-cleanup`, `cleanup-orphan-worktrees` |
| 작성 규칙과 참고 자료 확인 | `convention-review`, `curate-links`, `github-permalink` |

예를 들어 대화창에서 다음처럼 요청합니다.

```text
onul의 incident-triage로 오늘 09:00 UTC부터 늘어난 5xx 오류를 조사해 줘.
조회만 하고, 서비스 재시작이나 설정 변경은 하지 마.
직접 확인한 사실과 가설, 추가로 필요한 확인을 나눠서 설명해 줘.
```

```text
onul의 bump-selfhosted-app으로 현재 버전에서 목표 버전까지 변경 사항을 확인하고 업데이트 PR을 준비해 줘.
데이터 마이그레이션, 백업과 복구 조건을 정리하되 실제 서비스에는 배포하지 마.
```

`frontend-rum-privacy`는 기록 대상과 환경별 보호 설정을 먼저 제안합니다.
`cleanup-orphan-worktrees`는 삭제 후보와 남아 있는 작업을 확인한 뒤 삭제 범위를 확인합니다.

## 플러그인으로 설치

### Codex

터미널에서 실행합니다.

```sh
codex plugin marketplace add etamong-playground/agent-plugins
codex plugin add onul@onul-services
codex plugin list --json
```

설치 후 작업할 프로젝트 폴더에서 Codex를 시작하고 스킬 선택 목록에서 `grilling`을 선택합니다.
대화창에서는 다음처럼 요청할 수 있습니다.

```text
onul의 grilling 스킬을 사용해서 만들 앱의 사용자와 첫 버전 범위를 하나씩 질문해 줘.
```

### Claude Code

터미널에서 실행합니다.

```sh
claude plugin marketplace add etamong-playground/agent-plugins
claude plugin install onul@onul-services
claude plugin list
```

작업할 프로젝트 폴더에서 Claude Code를 시작한 뒤 대화창에 입력합니다.

```text
/onul:grilling 만들 앱의 사용자와 첫 버전 범위를 하나씩 질문해 줘.
/onul:prototype 확정한 사용자 작업에 맞는 화면 구성을 비교해 줘.
/onul:tdd 확정한 핵심 동작의 정상 입력과 실패 조건부터 테스트해 줘.
/onul:diagnosing-bugs 현재 발생하는 오류를 재현하고 원인을 검증해 줘.
```

## 카테고리별 설치

전체 `onul` 대신 필요한 카테고리를 선택할 수 있습니다.
카테고리끼리는 함께 설치할 수 있으며, 전체 묶음과 카테고리를 함께 설치하면 같은 워크플로우가 중복됩니다.

| 플러그인 | 용도 |
| --- | --- |
| onul-planning | 기획, 인터뷰, 요구사항 |
| onul-development | 구현, TDD, 디버깅, 프로그램 메모리 최적화 |
| onul-verification | 리뷰, UI 검증, 테스트와 보안 |
| onul-writing | 한국어 문체, 문서와 설명 |
| onul-agent-tools | 에이전트 메모리, 지침과 스킬 개선 |
| onul-operations | 의존성, Git 작업, 운영과 장애 조사 |
| onul-macos | 일반 Mac 앱 개발과 UI |
| onul-audio | 요구사항에 따라 선택하는 오디오 개발과 검증 |

기획과 개발 카테고리만 설치하는 예입니다.
전체 묶음이 이미 설치되어 있다면 먼저 제거합니다.

```sh
codex plugin add onul-planning@onul-services
codex plugin add onul-development@onul-services
```

Claude Code에서는 다음처럼 설치합니다.

```sh
claude plugin install onul-planning@onul-services
claude plugin install onul-development@onul-services
```

전체 묶음의 기획 스킬은 `/onul:planning`, 기획 카테고리의 같은 스킬은 `/onul-planning:planning`으로 호출합니다.
Codex에서는 설치 후 표시되는 스킬 목록에서 `planning`을 선택하거나 대화로 사용을 요청합니다.
다른 카테고리의 스킬이 필요하면 설치 여부부터 확인하며, 스킬이 없어도 직접 수행할 수 있는 작업은 해당 방법으로 진행합니다.

## 기존 jskills에서 전환

`jskills`는 기존 사용자를 위한 호환 패키지로 제공하며, 기존 `feature-planning` 이름을 유지합니다.
새 패키지에서는 같은 스킬을 `planning`으로 사용합니다.
전환할 도구에서 기존 패키지를 제거한 뒤 전체 `onul` 또는 필요한 카테고리를 설치하고 새 세션을 엽니다.

```sh
codex plugin remove jskills@onul-services
codex plugin add onul@onul-services
```

```sh
claude plugin uninstall jskills@onul-services
claude plugin install onul@onul-services
```

전체 `onul`에서 카테고리로 바꿀 때도 전체 패키지를 먼저 제거합니다.
직접 복사한 스킬은 플러그인을 제거해도 남으므로, 같은 스킬이 설치 경로에 있는지 별도로 확인합니다.
기존 가이드 주소는 계속 사용할 수 있습니다.

## ZIP으로 직접 설치

[전체 스킬 ZIP](https://pages.onul.me/jskills/downloads/onul.zip)을 내려받아 압축을 풉니다.
압축을 풀면 `onul/skills/스킬이름/SKILL.md`와 각 스킬의 참고 파일이 보입니다.
`SKILL.md` 한 파일만 복사하지 말고 스킬 폴더 전체를 복사합니다.
개별 스킬 ZIP에는 스킬 폴더와 해당 스킬에 적용되는 MIT license가 들어 있습니다.
전체 ZIP에서 스킬 폴더만 복사한다면 `sources.json`의 `license`에 지정된 파일도 해당 폴더에 `LICENSE`라는 이름으로 함께 복사합니다.
스킬 폴더 안에 이미 있는 추가 license 파일도 함께 보존합니다.
`tdd`는 `codebase-design`이 설치되어 있으면 해당 설계 지침을 참고합니다.
설치되어 있지 않으면 인터페이스와 테스트 경계를 직접 검토하며, 추가 설치를 자동으로 실행하지 않습니다.

| 사용할 도구 | 개인용 설치 위치 | 프로젝트용 설치 위치 |
| --- | --- | --- |
| Codex | `~/.agents/skills/스킬이름/` | `.agents/skills/스킬이름/` |
| Claude Code | `~/.claude/skills/스킬이름/` | `.claude/skills/스킬이름/` |

프로젝트용 설치 위치는 작업할 프로젝트의 루트를 기준으로 합니다.
개인용 `~` 설치 위치에 둔 스킬은 여러 프로젝트에서 사용할 수 있습니다.
Windows에서는 `~` 대신 사용자 홈 폴더를 사용합니다.
탐색기로 위 위치에 폴더 전체를 복사해도 됩니다.
같은 이름의 스킬이 있으면 덮어쓰지 말고 먼저 기존 내용을 확인합니다.
플러그인 설치와 직접 설치 중 하나를 선택하면 중복 표시를 피할 수 있습니다.

macOS 또는 Linux에서는 `grilling.zip`을 내려받아 압축을 푼 상위 폴더에서 다음 명령으로 설치할 수 있습니다.
이 개별 ZIP에는 `grilling/LICENSE`가 포함되어 있습니다.
기존 대상 폴더가 있으면 명령은 복사를 중단합니다.

Codex:

```sh
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/grilling" && {
  cp -R ./grilling "$HOME/.agents/skills/"
}
```

Claude Code:

```sh
mkdir -p "$HOME/.claude/skills"
test ! -e "$HOME/.claude/skills/grilling" && {
  cp -R ./grilling "$HOME/.claude/skills/"
}
```

다른 스킬은 해당 개별 ZIP을 받은 뒤 위 명령의 `grilling`을 그 스킬 이름으로 바꿉니다.
새 세션에서 Codex는 `$grilling`, Claude Code는 `/grilling`으로 직접 설치한 스킬을 실행합니다.

## 프로젝트에서 시작하기

스킬을 설치한 뒤에는 작업할 프로젝트 폴더로 이동해서 에이전트를 실행합니다.
아래 `/path/to/project`를 실제 프로젝트 경로로 바꿉니다.

Codex:

```sh
cd /path/to/project
codex
```

Claude Code:

```sh
cd /path/to/project
claude
```

설치가 끝나면 프로젝트의 목적과 실행 명령을 알려 주고, 원하는 스킬을 대화에서 명시합니다.

## 두 도구에서 사용할 때의 차이

원본 파일은 영어로 작성되어 있습니다.
대화에서 "설명과 결과는 한국어로 작성해 줘"라고 덧붙일 수 있습니다.
`prototype`, `teach`, `writing-great-skills`는 직접 호출해서 사용합니다.
다른 스킬도 대화에서 이름을 명시하면 사용할 절차를 분명하게 지정할 수 있습니다.

원본 본문에 있는 `/codebase-design` 같은 이름은 다른 스킬을 가리킵니다.
Claude Code의 전체 묶음에서는 `/onul:codebase-design`, 개발 카테고리에서는 `/onul-development:codebase-design`, 호환 패키지에서는 `/jskills:codebase-design`을 사용합니다.
콜론 앞에는 설치한 플러그인 이름이 붙습니다.
Codex에서는 스킬 선택 목록에 표시된 `codebase-design`을 고르거나 해당 스킬을 사용하라고 요청합니다.
일부 스킬은 병렬 에이전트를 사용하므로 현재 클라이언트가 지원하는 도구와 모델을 사용하도록 요청합니다.
병렬 에이전트를 지원하지 않는 환경에서는 수행한 검토와 생략한 단계를 구분해서 확인합니다.

`teach`의 참고 자료 템플릿에 있는 `example.com`은 예시 주소이므로 실제 학습 자료로 바꿔야 합니다.

## 설치 확인과 업데이트

플러그인 목록에 선택한 전체 묶음이나 카테고리가 있는지 확인하고 새 세션을 엽니다.
원하는 스킬을 명시해서 실행한 뒤, 해당 스킬이 요구하는 질문이나 단계가 시작되는지 확인합니다.
스킬이 보이지 않으면 설치 위치에 `스킬이름/SKILL.md`가 있는지 확인합니다.
조직에서 관리하는 클라이언트는 플러그인 설치나 로컬 스킬 사용을 제한할 수 있습니다.

다음은 전체 `onul` 묶음의 업데이트 예입니다.
카테고리를 설치했다면 `onul@onul-services`를 설치한 카테고리 이름으로 바꿔서 각각 실행합니다.
예를 들어 기획 카테고리는 `onul-planning@onul-services`, 기존 호환 패키지는 `jskills@onul-services`입니다.
업데이트할 때 새 설치 방식을 추가하지 말고, 이미 선택한 패키지를 업데이트합니다.

Codex 업데이트:

```sh
codex plugin marketplace upgrade onul-services
codex plugin add onul@onul-services
```

Claude Code 업데이트:

```sh
claude plugin marketplace update onul-services
claude plugin update onul@onul-services
```

직접 설치했다면 새 ZIP의 내용을 기존 파일과 비교한 뒤 교체합니다.
삭제할 때는 직접 설치한 스킬 폴더만 제거합니다.
플러그인은 각 도구의 플러그인 관리 화면에서 제거할 수 있습니다.

## 라이선스와 출처

스킬을 복사하거나 재배포할 때는 해당 ZIP의 `LICENSE`와 추가 저작권 표시를 함께 보관합니다.
파일의 출처와 적용되는 라이선스는 아래에서 확인할 수 있습니다.

- [공개 원본 저장소](https://github.com/mattpocock/skills)
- [스킬별 출처와 라이선스](https://pages.onul.me/jskills/downloads/sources.json)
- [Matt Pocock 원본 MIT license](https://pages.onul.me/jskills/downloads/LICENSE)
- [개발 워크플로우 스킬 MIT license](https://pages.onul.me/jskills/downloads/LICENSE.jskills)
- [전체 ZIP과 개별 ZIP의 SHA-256](https://pages.onul.me/jskills/downloads/SHA256SUMS.txt)

## 공식 사용 설명서

설치 경로와 플러그인 사용 방법은 아래 공식 문서를 기준으로 작성했습니다.

- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code marketplace](https://code.claude.com/docs/en/plugin-marketplaces)

- [Codex 메모리 관리](https://learn.chatgpt.com/docs/customization/memories)
- [Claude Code 메모리 관리](https://code.claude.com/docs/en/memory)
