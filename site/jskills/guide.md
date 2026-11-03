# jskills

해커톤에서 아이디어를 구체화하고, 동작하는 데모를 만들고, 오류를 확인할 때 쓰는 AI coding skill 모음입니다.
Codex와 Claude Code에서 사용할 수 있습니다.
SK하이닉스 공식 자료나 공식 플러그인은 아닙니다.

## 먼저 쓰면 좋은 스킬

처음에는 `grilling`, `prototype`, `tdd`, `diagnosing-bugs`부터 쓰면 됩니다.
아래 순서는 해커톤 진행을 위한 제안이며, 대회 평가 기준을 설명하지 않습니다.

| 단계 | 스킬 | 사용할 때 | 요청 예시 |
| --- | --- | --- | --- |
| 문제 정하기 | grilling | 사용자, 해결할 문제, 데모 범위를 정할 때 씁니다. | 설비 이상 알림 데모를 만들려고 해. 사용자가 누구이고 어떤 행동을 할지부터 하나씩 질문해 줘. |
| 데모 만들기 | prototype | 화면 후보나 상태 변화를 빠르게 확인할 때 씁니다. | 가상 센서 데이터로 이상 징후 화면을 만들어 줘. 서로 다른 화면 구성을 비교하고 싶어. |
| 핵심 기능 확인하기 | tdd | 정상 입력과 오류 입력의 결과를 테스트할 때 씁니다. | 정상 값, 임계값 경계, 누락 값의 동작을 정한 뒤 테스트 하나씩 구현해 줘. |
| 오류 고치기 | diagnosing-bugs | 증상을 재현하고 원인을 검증할 때 씁니다. | CSV 업로드가 실패해. 같은 오류가 나는 실행 명령부터 만들고 원인 후보를 검증해 줘. |

`prototype`은 버릴 코드를 빠르게 만드는 스킬입니다.
선택한 구성을 실제 기능으로 옮길 때는 오류 처리와 테스트를 추가해야 합니다.
`tdd`는 인터페이스와 검증할 동작을 먼저 질문하므로, 핵심 동작을 정한 뒤 실행하면 됩니다.

## 설계와 학습에 쓰는 스킬

| 스킬 | 용도 | 요청 예시 |
| --- | --- | --- |
| domain-modeling | 팀에서 쓰는 용어와 데이터의 의미를 정리합니다. | 측정값, 이상 징후, 알림의 뜻을 구분하고 용어집을 만들어 줘. |
| codebase-design | 복잡한 기능을 작은 인터페이스로 나눕니다. | CSV 파싱과 이상 판단을 따로 테스트할 수 있게 인터페이스를 설계해 줘. |
| writing-great-skills | 반복 작업을 팀의 스킬로 정리할 때 참고합니다. | 데모 전 점검 절차를 반복해서 쓸 수 있는 스킬로 작성해 줘. |
| teach | 익숙하지 않은 기술을 연습하면서 배웁니다. | 이 프로젝트에서 쓰는 embedding을 작은 예제로 설명하고 연습 문제를 내 줘. |

## 설치 전 준비

Codex 또는 Claude Code를 설치하고, 본인 계정으로 로그인한 상태에서 시작합니다.
플러그인 설치 명령은 터미널에서 실행하고, 스킬 사용 예시는 에이전트 대화창에 입력합니다.
스킬은 작업 절차를 설명하는 파일입니다.
모델 이용권, API key, Python, Node.js, Playwright 같은 실행 도구는 별도로 준비해야 합니다.
해커톤에서 허용한 도구와 데이터 범위를 먼저 확인하고, 회사 자료 대신 공개 데이터나 가상 데이터로 예제를 실행합니다.

## 플러그인으로 설치

### Codex

터미널에서 실행합니다.

```sh
codex plugin marketplace add etamong-playground/agent-plugins
codex plugin add jskills@onul-services
codex plugin list --json
```

설치 후 새 세션을 열고 스킬 선택 목록에서 `grilling`을 선택합니다.
대화창에서는 다음처럼 요청할 수 있습니다.

```text
jskills의 grilling 스킬을 사용해서 해커톤 아이디어의 사용자와 데모 범위를 하나씩 질문해 줘.
```

### Claude Code

터미널에서 실행합니다.

```sh
claude plugin marketplace add etamong-playground/agent-plugins
claude plugin install jskills@onul-services
claude plugin list
```

새 세션의 대화창에서 실행합니다.

```text
/jskills:grilling 설비 이상 알림 아이디어의 사용자와 데모 범위를 하나씩 질문해 줘.
/jskills:prototype 가상 센서 데이터로 화면 구성을 비교해 줘.
/jskills:tdd CSV 입력의 정상 값과 누락 값부터 테스트해 줘.
/jskills:diagnosing-bugs CSV 업로드 오류를 재현하고 원인을 검증해 줘.
```

jskills에는 MCP 연결, 로그인 연동, 자동 실행 hook이 없습니다.
같은 marketplace에 있는 다른 플러그인은 이 가이드에서 설치하지 않습니다.

## ZIP으로 직접 설치

[전체 원본 ZIP](https://pages.onul.me/jskills/downloads/jskills.zip)을 내려받아 압축을 풉니다.
압축을 풀면 `jskills/skills/스킬이름/SKILL.md`와 각 스킬의 참고 파일이 보입니다.
`SKILL.md` 한 파일만 복사하지 말고 스킬 폴더 전체를 복사합니다.
개별 스킬 ZIP에는 원본 폴더와 MIT license가 들어 있습니다.
`tdd`는 계획 단계에서 `codebase-design`을 사용하므로, 개별 ZIP으로 설치할 때는 두 스킬을 함께 설치합니다.
플러그인과 전체 ZIP에는 두 스킬이 모두 들어 있습니다.

| 사용할 도구 | 개인용 설치 위치 | 프로젝트용 설치 위치 |
| --- | --- | --- |
| Codex | `~/.agents/skills/스킬이름/` | `.agents/skills/스킬이름/` |
| Claude Code | `~/.claude/skills/스킬이름/` | `.claude/skills/스킬이름/` |

Windows에서는 `~` 대신 사용자 홈 폴더를 사용합니다.
탐색기로 위 위치에 폴더 전체를 복사해도 됩니다.
같은 이름의 스킬이 있으면 덮어쓰지 말고 먼저 기존 내용을 확인합니다.
플러그인 설치와 직접 설치 중 하나를 선택하면 중복 표시를 피할 수 있습니다.

macOS 또는 Linux에서 처음 설치한다면, 압축을 푼 상위 폴더에서 다음 명령으로 `grilling`만 설치할 수 있습니다.
기존 대상 폴더가 있으면 명령은 복사를 중단합니다.

Codex:

```sh
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/grilling" && {
  cp -R ./jskills/skills/grilling "$HOME/.agents/skills/" &&
  cp ./jskills/LICENSE "$HOME/.agents/skills/grilling/LICENSE"
}
```

Claude Code:

```sh
mkdir -p "$HOME/.claude/skills"
test ! -e "$HOME/.claude/skills/grilling" && {
  cp -R ./jskills/skills/grilling "$HOME/.claude/skills/" &&
  cp ./jskills/LICENSE "$HOME/.claude/skills/grilling/LICENSE"
}
```

다른 스킬을 설치할 때는 위 명령의 `grilling`을 원하는 스킬 이름으로 바꿉니다.
새 세션에서 Codex는 `$grilling`, Claude Code는 `/grilling`으로 직접 설치한 스킬을 실행합니다.

## 두 도구에서 사용할 때의 차이

원본 파일은 영어로 작성되어 있습니다.
대화에서 "설명과 결과는 한국어로 작성해 줘"라고 덧붙일 수 있습니다.
`prototype`, `teach`, `writing-great-skills`는 직접 호출해서 사용합니다.

원본 본문에 있는 `/codebase-design` 같은 이름은 다른 스킬을 가리킵니다.
Claude Code 플러그인으로 설치했다면 `/jskills:codebase-design`을 선택하고, Codex에서는 스킬 선택 목록에서 `codebase-design`을 고르거나 해당 스킬을 사용하라고 요청합니다.
클라이언트가 원본에 나오는 도구 이름이나 subagent 기능을 지원하지 않으면, 에이전트에게 가능한 방식으로 진행하고 생략한 단계를 알려 달라고 요청합니다.

`diagnosing-bugs`의 마지막에 나오는 `improve-codebase-architecture`는 별도 후속 스킬이며 이 모음에 포함되어 있지 않습니다.
디버깅을 마친 뒤 구조 개선이 필요할 때만 원본 저장소에서 확인하면 됩니다.
`teach`의 참고 자료 템플릿에 있는 `example.com`은 예시 주소이므로 실제 학습 자료로 바꿔야 합니다.

## 작업할 때 알아둘 팁

### 스킬은 필요한 단계에서 하나씩 사용합니다

아이디어를 정할 때는 `grilling`, 화면이나 로직을 비교할 때는 `prototype`을 사용합니다.
핵심 동작이 정해지면 `tdd`로 구현하고, 오류가 생기면 `diagnosing-bugs`로 재현합니다.
모든 스킬을 한 번에 호출하면 질문과 작업 범위가 늘어날 수 있습니다.
시간이 부족하면 먼저 보여 줄 데모 한 가지를 정하고, 그 데모에 필요한 동작부터 완성합니다.

### 결과와 완료 조건을 함께 알려 줍니다

에이전트에게 만들 결과, 사용할 입력, 지켜야 할 제약, 확인할 동작을 알려 줍니다.
기존 프로젝트라면 실행 명령과 관련 파일도 함께 지정합니다.
아래는 가상 데이터로 만드는 데모의 요청 예시입니다.

```text
가상 센서 CSV를 업로드하면 이상 징후를 표시하는 데모를 만들고 싶어.
입력은 timestamp, sensor_id, value 세 열이야.
외부 API는 사용하지 않고, 저장소의 기존 실행 명령을 유지해 줘.
정상 입력, 임계값과 같은 값, 빈 파일, 누락된 value를 확인할 수 있어야 해.
먼저 필요한 질문을 하고, 작업이 끝나면 실행 방법과 검증한 동작을 알려 줘.
설명은 한국어로 작성해 줘.
```

실제 이상 판단 기준은 팀이 정해서 전달해야 합니다.
에이전트가 예제에 임의로 넣은 임계값을 업무 기준으로 사용하지 않습니다.

### 코드 테스트와 AI 결과 평가는 따로 확인합니다

코드 테스트가 통과했어도 모델의 분류나 답변이 정확한지는 별도로 확인해야 합니다.
정상 사례, 이상 사례, 판단하기 어려운 사례를 준비하고 기대 결과와 근거를 함께 적어 둡니다.
같은 입력으로 결과를 비교하고, 틀린 사례를 확인한 뒤 prompt나 모델 설정을 바꿉니다.
데모에서는 실제 측정값, 가상 데이터, 모델이 추정한 값을 구분해서 표시합니다.

### 수정 결과는 실행해서 확인합니다

작업 전에 Git에 저장해 두면 변경 전후를 비교하기 쉽습니다.
에이전트가 작업을 마치면 변경한 파일, 실행한 검사, 아직 검증하지 못한 부분을 확인합니다.
다음 명령은 Git 저장소의 변경 상태와 내용을 보여 줍니다.

```sh
git status --short
git diff --stat
git diff
```

실행 명령으로 데모를 직접 열고, 정상 입력뿐 아니라 오류 입력도 넣어 봅니다.
스킬 설치나 테스트 통과가 서비스 배포와 실제 동작까지 보장하지는 않습니다.

### API key와 회사 자료는 공유 범위를 확인합니다

API key를 prompt, 소스 코드, 화면 캡처에 넣지 않습니다.
프로젝트에서 정한 환경 변수나 secret 저장 방식을 사용하고, `.env` 파일은 Git에 포함되지 않는지 확인합니다.
데모 화면과 로그에 key나 개인정보가 표시되지 않는지도 확인합니다.
회사 문서나 실제 설비 데이터를 사용할 때는 대회와 회사에서 허용한 환경인지 먼저 확인합니다.
공개 저장소로 옮길 때는 코드와 함께 예제 데이터, 로그, 캡처도 확인합니다.

### 데모 입력과 실행 방법을 남깁니다

README에 설치 명령, 실행 명령, 필요한 환경 변수 이름, 예제 입력 위치를 적습니다.
데모에 사용할 정상 입력과 오류 입력을 저장해 두고 처음부터 다시 실행해 봅니다.
외부 API를 쓰면 응답 지연, 요청 제한, 네트워크 오류가 났을 때 화면에 어떤 내용을 보여 줄지도 확인합니다.
가상 응답으로 시연할 경우에는 시연 중에도 가상 응답임을 알 수 있게 표시합니다.

## 설치 확인과 업데이트

플러그인 목록에 `jskills@onul-services`가 있는지 확인하고 새 세션을 엽니다.
원하는 스킬을 명시해서 실행한 뒤, 해당 스킬이 요구하는 질문이나 단계가 시작되는지 확인합니다.
스킬이 보이지 않으면 설치 위치에 `스킬이름/SKILL.md`가 있는지 확인합니다.
조직에서 관리하는 클라이언트는 플러그인 설치나 로컬 스킬 사용을 제한할 수 있습니다.

Codex 업데이트:

```sh
codex plugin marketplace upgrade onul-services
codex plugin add jskills@onul-services
```

Claude Code 업데이트:

```sh
claude plugin marketplace update onul-services
claude plugin update jskills@onul-services
```

직접 설치했다면 새 ZIP의 내용을 기존 파일과 비교한 뒤 교체합니다.
삭제할 때는 직접 설치한 스킬 폴더만 제거합니다.
플러그인은 각 도구의 플러그인 관리 화면에서 제거할 수 있습니다.

## 원본과 공개 범위

Matt Pocock의 공개 skills에서 선택한 파일을 수정 없이 제공합니다.
참고 문서와 스크립트도 함께 보존하고, MIT license를 포함합니다.
공개 묶음에는 개인 작업 기록, 계정 정보, 사내 설정, 개인 인프라 운영 스킬을 넣지 않았습니다.
다만 스킬을 실행하면 에이전트가 현재 프로젝트를 읽거나 수정할 수 있으므로, 공유할 수 있는 데이터만 작업 폴더에 둡니다.

- [공개 원본 저장소](https://github.com/mattpocock/skills)
- [이 묶음의 원본 revision](https://github.com/mattpocock/skills/tree/6eeb81b5fcfeeb5bd531dd47ab2f9f2bbea27461)
- [파일별 SHA-256과 출처](https://pages.onul.me/jskills/downloads/sources.json)
- [MIT license](https://pages.onul.me/jskills/downloads/LICENSE)
- [전체 ZIP과 개별 ZIP의 SHA-256](https://pages.onul.me/jskills/downloads/SHA256SUMS.txt)

## 공식 사용 설명서

설치 경로와 플러그인 사용 방법은 아래 공식 문서를 기준으로 작성했습니다.

- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
