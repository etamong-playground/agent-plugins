# macOS 오디오 앱 개발

음향 작업에서 반복하는 일을 Mac 앱으로 만드는 과정입니다.
먼저 파일 검사처럼 입출력이 분명한 기능을 완성하고, 필요한 경우 실시간 오디오나 DAW plug-in으로 확장합니다.
Swift를 처음 쓰더라도 작업 목적과 기대 결과는 음향 엔지니어가 정하고, 에이전트에게 설계와 구현을 맡길 수 있습니다.
스킬 설치가 필요하면 [설치와 스킬](#purpose-installation)에서 시작합니다.

## 개발 환경 준비

Native macOS 앱을 빌드하고 실행하려면 Mac과 [Xcode](https://developer.apple.com/xcode/)가 필요합니다.
오디오 계산을 별도 package로 테스트할 수 있어도 실제 앱의 화면과 권한, 서명은 앱 target에서 확인해야 합니다.
기존 프로젝트가 있다면 언어와 UI framework, 지원 macOS, 빌드와 테스트 명령을 먼저 에이전트에게 확인시킵니다.
새 프로젝트라면 첫 기능을 정한 뒤 그 기능에 맞는 macOS 앱 target과 test target을 준비합니다.

Mac 터미널에서 `xcodebuild -version`으로 선택된 Xcode 버전을 확인할 수 있습니다.
Command Line Tools만 설치된 환경에서는 전체 Xcode가 필요한 앱 빌드와 Native UI 검증을 수행할 수 없습니다.
실시간 입력을 쓸 경우에는 테스트할 오디오 인터페이스와 허용할 재생 및 녹음 범위도 지정합니다.

## 첫 앱의 범위 정하기

예를 들어 납품 전 WAV와 AIFF 파일의 길이, sample rate, 채널 수, sample peak를 확인하는 앱을 만들 수 있습니다.
파일을 선택하면 분석 결과를 표로 보여 주고, 원본 파일은 변경하지 않는 범위입니다.
처음에는 녹음, 자동 보정, LUFS 측정과 DAW 연동을 추가하지 않아도 유용한 도구를 완성할 수 있습니다.
이 예제가 작업에 맞지 않으면 본인이 반복하는 작업 하나로 바꿉니다.

| 만들 도구 | 먼저 정할 내용 | 확인 방법 |
| --- | --- | --- |
| 파일 검사와 일괄 변환 | 입력 형식, 채널 처리, 표시 단위, 저장 규칙을 정합니다. | 알려진 입력 파일과 결과를 비교하고 원본 보존을 확인합니다. |
| 실시간 미터와 녹음 | 입력 장치, sample rate, 채널, 중단과 복구 동작을 정합니다. | 자동 테스트와 별도로 실제 장치에서 확인합니다. |
| DSP와 Audio Unit | 처리 방식, parameter, 지원할 DAW와 plug-in 형식을 정합니다. | 기준 신호, offline render와 실제 host에서 확인합니다. |

파일 분석과 실시간 처리는 검증할 조건이 다릅니다.
특히 offline 테스트 통과만으로 지연 시간, 장치 호환성이나 음질을 확인했다고 볼 수는 없습니다.

## 인터뷰부터 검증까지

각 단계에서 필요한 스킬을 하나씩 선택합니다.
기획서가 이미 있다면 요구사항과 검증 기준을 확인한 뒤 구현 단계부터 시작할 수 있습니다.

<!-- workflow-diagram -->

| 관점 | 사용할 스킬 | 확인할 결과 |
| --- | --- | --- |
| 기획서 인터뷰 | grilling, platform-plan-doc | 누가 어떤 작업을 할지, 입력과 출력, 첫 버전의 범위가 정해집니다. |
| 요구사항 피드백 | requirements-feedback | 요청한 변경이 결함 수정인지 새 기능인지 구분하고 완료 조건에 반영합니다. |
| Mac 앱 설계 | macos-audio-app, codebase-design | 파일 처리, 오디오 계산, 화면 상태를 나누고 필요한 API와 지원 환경을 정합니다. |
| 테스트부터 구현 | tdd | 기대 결과를 직접 계산할 수 있는 작은 동작부터 실패하는 테스트로 확인합니다. |
| 오디오 검증 | audio-validation, diagnosing-bugs | 계산값, 파일 처리, 성능과 장치 동작을 각각 검증합니다. |
| Native UI 검토 | macos-ui-review, prototype | 키보드 조작, 단위, 상태 표시와 오류 복구를 실제 작업 순서로 확인합니다. |
| 독립적인 검토 | adversarial-review, audience-review | 요구사항, 오디오 처리, UI와 문서를 검토한 뒤 실제 근거가 있는 지적을 반영합니다. |

## 기획서 인터뷰 요청하기

완성된 기능 목록이 없어도 시작할 수 있습니다.
자주 하는 작업과 번거로운 지점을 설명하고, 중요한 질문부터 받습니다.

```text
jskills의 grilling과 platform-plan-doc을 사용해 줘.
나는 음향 엔지니어이고, 납품할 오디오 파일을 확인하는 Mac 앱을 만들고 싶어.
지금은 DAW에서 파일을 하나씩 열어 길이와 sample rate, 채널 수, peak를 확인해.
누가 어떤 파일을 검사하고 결과를 어떻게 쓸지부터 질문해 줘.
peak의 의미와 단위, 지원 형식, 원본 보존, 첫 버전의 완료 조건을 먼저 정하자.
질문은 한 번에 이해할 수 있는 분량으로 해 줘.
이번에는 기획서까지만 작성하고 코드는 수정하지 마.
설명과 기획서는 한국어로 작성해 줘.
```

기획서에는 사용자 작업, 지원 형식, 용어와 단위, 화면 상태, 실패했을 때의 동작과 완료 조건을 남깁니다.
"빠르게 처리한다"처럼 판단하기 어려운 조건은 대상 파일의 크기와 개수, 실행 환경, 허용 시간을 정한 뒤 측정합니다.
에이전트가 임의로 정한 loudness나 clipping 기준을 납품 규격으로 사용하지 않습니다.

## 피드백을 요구사항으로 바꾸기

화면을 본 뒤 생긴 의견은 원래 작업과 연결해서 정리합니다.
예를 들어 "peak가 이상하다"는 의견만으로 계산식을 바꾸기 전에 sample peak와 true peak 중 어떤 값을 기대했는지 확인해야 합니다.

```text
jskills의 requirements-feedback을 사용해 줘.
기획서와 현재 파일 검사 화면을 읽고 다음 피드백을 검토해 줘.
“파일마다 peak가 하나만 나오니 어느 채널의 값인지 모르겠다.”
현재 동작, 사용자가 해야 하는 판단, 바꿀 요구사항, 검증할 예시를 연결해 줘.
채널별 값과 전체 최대값을 어떻게 표시할지 아직 결정되지 않았다면 질문해 줘.
확인되지 않은 해석을 요구사항으로 확정하지 말고, 이번에는 변경안을 작성해 줘.
```

변경이 확정되면 기획서와 완료 조건을 함께 수정합니다.
구현까지 원한다면 수정할 범위와 검증할 동작을 이어서 지정합니다.

## TDD로 작은 기능 완성하기

TDD는 기대 동작을 테스트로 먼저 정하고, 실패를 확인한 뒤 구현하는 방식입니다.
오디오 파일 읽기와 UI를 한꺼번에 만들기 전에, sample 배열을 받아 최대 진폭을 계산하는 작은 함수부터 시작할 수 있습니다.

```text
jskills의 tdd와 audio-validation을 사용해 줘.
선형 PCM의 sample peak 계산을 먼저 구현하자.
입력 sample은 full scale을 1.0으로 표현한다고 정했어.
양수와 음수 모두 절댓값으로 비교하고, 전체 채널의 최대값을 반환해 줘.
진폭 0.5의 impulse는 약 -6.0206 dBFS이고, 무음은 별도 상태로 표현하자.
단위를 섞지 말고 sample peak를 true peak나 LUFS라고 부르지 마.
허용 오차의 근거를 먼저 정하고 테스트 하나의 실패를 확인한 뒤 구현해 줘.
숫자 계산과 화면 반올림은 따로 테스트해 줘.
```

그다음 파일 읽기, 여러 파일 처리, 취소와 화면 표시를 작은 단위로 연결합니다.
블록 끝에 최대값이 있는 파일, 마지막 블록이 짧은 파일, 빈 파일과 손상된 파일도 확인합니다.
Swift Testing과 XCTest는 프로젝트에 맞춰 선택하고, Native UI 자동화에는 XCTest와 XCUIAutomation을 사용합니다.
지원 범위는 [Apple의 테스트 target 설명](https://developer.apple.com/documentation/xcode/adding-tests-to-your-xcode-project)에서 확인할 수 있습니다.

## 무엇을 자동으로 검증할 수 있나

| 검증 대상 | 예시 | 결과를 판단할 근거 |
| --- | --- | --- |
| 오디오 계산 | 무음, impulse, 채널마다 최대값이 다른 신호를 씁니다. | 별도로 계산한 기대값과 근거가 있는 허용 오차로 비교합니다. |
| 파일 처리 | 지원 형식, 긴 파일, 손상된 파일과 취소를 확인합니다. | 메모리 사용, 결과 파일, 오류 상태와 원본 보존을 확인합니다. |
| 처리 graph | 같은 신호와 parameter로 offline render합니다. | 길이와 처리 결과를 기준 출력과 비교합니다. |
| Native UI | 열기, 분석, 취소, 저장과 오류 복구를 실행합니다. | 실제 앱의 키보드, focus, accessible value와 상태를 확인합니다. |
| 실시간 입출력 | 장치 분리, sample rate 변경, sleep/wake와 부하를 확인합니다. | 실제 장치의 누락, callback 시간과 정의한 지연 구간을 측정합니다. |

AVAudioEngine의 offline manual rendering은 하드웨어 없이 graph의 출력을 검사할 때 사용할 수 있습니다.
단순한 수치 계산에 audio engine이 반드시 필요한 것은 아닙니다.
방식과 예제는 [Apple의 offline 처리 설명](https://developer.apple.com/documentation/avfaudio/performing-offline-audio-processing)을 참고합니다.

음질과 사용감은 별도 청취와 실제 작업으로 확인합니다.
비교할 때는 level, bypass 정렬과 재생 구간처럼 판단에 영향을 주는 조건을 맞춥니다.
에이전트가 실행하지 못한 DAW, 오디오 인터페이스나 청취 검증은 미검증으로 남깁니다.

## Mac 화면 검토하기

음향 앱에서는 보기 좋은 화면만큼 단위와 상태를 정확히 읽을 수 있어야 합니다.
채널 구분, 현재 선택한 장치, 분석 중인 파일과 완료된 결과를 혼동하지 않게 표시합니다.
정밀한 값은 slider 외에 숫자로 입력할 수 있어야 합니다.

```text
jskills의 macos-ui-review를 사용해 줘.
파일 열기, 분석, 취소, 결과 확인과 내보내기 순서로 화면을 검토해 줘.
메뉴와 단축키, focus 이동, 긴 파일명, 창 크기 변경, dark mode도 확인해 줘.
미터와 오류는 색만으로 구분하지 말고 값과 상태를 읽을 수 있게 해 줘.
VoiceOver와 키보드 조작은 실제 Native UI에서 확인해 줘.
실행 환경이 없다면 코드와 설계에서 확인한 내용, 직접 실행해야 할 절차를 구분해 줘.
```

브라우저 mockup은 화면 구성을 비교할 때 유용합니다.
실제 macOS 메뉴, 접근성 정보나 장치 선택 동작을 검증한 결과로 사용하지는 않습니다.
기준은 [macOS 디자인](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos), [키보드](https://developer.apple.com/design/human-interface-guidelines/keyboards), [접근성](https://developer.apple.com/design/human-interface-guidelines/accessibility) 설명을 참고합니다.

## 실시간 기능과 배포로 확장하기

실시간 기능이 필요하면 지원할 인터페이스, sample rate, 채널 수와 buffer 조건을 먼저 정합니다.
오디오 callback에서 파일 읽기, 메모리 할당, lock 대기와 화면 갱신처럼 완료 시간을 예측하기 어려운 작업이 생기지 않게 설계합니다.
buffer frame 수를 sample rate로 나눈 값은 한 buffer의 시간이며, 입출력 전체 지연을 측정한 값은 아닙니다.
추가 real-time thread가 필요한 경우에만 [Audio Workgroups](https://developer.apple.com/documentation/audiotoolbox/understanding-audio-workgroups) 적용을 검토합니다.

마이크 입력이 필요한 기능은 사용 목적과 권한 거부 후의 동작을 함께 설계합니다.
파일만 분석하는 첫 버전에 녹음 권한을 미리 추가할 필요는 없습니다.
[macOS capture 권한](https://developer.apple.com/documentation/bundleresources/requesting-authorization-for-media-capture-on-macos)을 확인하고, 고객의 세션과 미공개 음원은 전송 승인을 받기 전까지 로컬에 둡니다.
에이전트에게는 먼저 합성 신호와 재현 절차를 전달합니다.

다른 사람에게 앱을 전달할 때는 지원 macOS와 CPU, 설치 방법과 저장 위치를 확인합니다.
Developer ID로 배포할 앱과 Mac App Store에 제출할 앱의 절차는 구분하며, [code signing과 notarization](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution) 요건을 선택한 방식에 맞춰 확인합니다.
빌드 성공과 서명된 앱의 새 Mac 설치 검증은 별개의 확인 항목입니다.

## 에이전트에게 작업을 맡기는 기준

1. 사용할 입력과 기대 결과, 보존할 파일, 수정할 범위를 알려 줍니다.
2. 기획서와 완료 조건을 확인한 뒤 작은 동작 하나를 구현합니다.
3. 실행한 명령과 실제 결과를 확인하고, 실패한 사례를 다음 테스트에 추가합니다.
4. 요구사항 피드백과 독립 리뷰를 반영한 뒤 같은 조건으로 다시 검증합니다.
5. 실제 장치, DAW와 청취가 필요한 항목은 음향 엔지니어가 확인하고 결과를 남깁니다.

새로운 스킬을 모두 한 번에 실행할 필요는 없습니다.
기획 중에는 인터뷰와 피드백, 구현 중에는 TDD, 동작을 확인할 때는 오디오 검증과 UI 리뷰를 선택하면 됩니다.
