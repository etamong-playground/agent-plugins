---
name: macos-audio-app
description: Implement explicitly requested macOS audio processing, capture/playback or Audio Unit features with defined file, device and real-time boundaries. Use after audio requirements are confirmed; a sound-engineering role alone does not select this workflow.
---

# macOS audio app development

First verify that the user has requested audio processing, I/O or a plug-in feature.
If only the user's profession or an unspecified Mac app is known, establish the app task before selecting this specialized workflow.
Start from the confirmed audio task: input, operation, expected output and how the user judges it.
Do not assume that an audio tool needs live capture, an Audio Unit, AI inference or cloud storage.
Reuse the project's language, build system and supported hardware instead of replacing them by default.

## Choose the smallest useful slice

Establish the minimum macOS version, CPU architectures, Xcode/SDK, distribution channel and required audio formats/devices.
Inspect existing project targets and test schemes before suggesting commands.
Choose a vertical slice from the confirmed task; do not replace a live-I/O requirement with file analysis or add live I/O to a file-only task.
Ask only unresolved questions that change behavior, compatibility or the verification method.
Record units and meaning: sample rate in Hz, frames versus samples, channel layout, sample peak dBFS versus true peak or LUFS, and latency measurement endpoints.
Never invent a delivery loudness target or label sample peak as true peak.

Choose APIs from the required behavior and current Apple documentation:
- File decoding/inspection: consider AVAudioFile and bounded chunk processing; preserve original files and metadata unless edits are requested.
- Playback or processing graphs: consider AVAudioEngine; use offline manual rendering when the graph must run without audio hardware.
- Device-level configuration or custom low-latency I/O: evaluate Core Audio only when higher-level APIs cannot meet the requirement.
- Audio Unit plug-ins: determine extension/host format, state serialization, automation, bus/channel support and actual DAW/host test matrix before implementation.
- Native UI: use SwiftUI or AppKit to fit the existing app and platform behavior; separate display updates from the audio path.

## Implement with observable contracts

Keep decoding, DSP/measurement, application state and presentation independently testable.
Agree on a short acceptance example, then use the project's test framework for one failing behavior, a minimal implementation and refactoring.
Keep file processing cancellable and bounded for long sessions; do not load entire recordings merely to draw a waveform.
Represent loading, ready, processing, cancelled, failed and completed states explicitly where they apply.
Preserve an original input, use a new destination for exports and handle interrupted/partial writes.

For real-time work, identify the exact callback and its deadline.
Keep allocation, locks, file/network I/O, logging and UI work out of that path; prepare buffers/state outside it and use bounded handoff with an explicit overflow policy.
Do not assume an actor, async task or lock-free queue automatically satisfies a real-time deadline.
Test device removal, sample-rate/channel changes, overload, sleep/wake and stopped-engine recovery on the actual supported configuration.
If auxiliary real-time threads are required, consult Audio Workgroups; framework-provided audio threads do not need an additional workgroup solely to use the framework.

Request microphone or other capture access only for the selected feature, explaining the purpose and handling denial.
Check current platform-specific usage descriptions, entitlements and sandbox file access rather than copying iOS-only session recipes into a Mac app.
Keep client recordings local unless their owner authorizes transfer; synthetic fixtures should be the default material for agent debugging.

## Verify and deliver

Use audio-validation for numerical/file/device evidence and macos-ui-review for native interactions when available; otherwise perform those checks directly.
Report build/test commands, fixtures and measurements actually run, then separate hardware, listening, host and signed-distribution checks that remain.
A successful build or offline render does not qualify live latency, audible quality or DAW compatibility.
Before distribution, choose Mac App Store versus Developer ID delivery and verify the applicable signing, sandbox and notarization requirements on the final artifact.
Do not publish, change signing identities or disable Gatekeeper merely to make a test pass.

## Official references

- [Offline rendering](https://developer.apple.com/documentation/avfaudio/performing-offline-audio-processing)
- [Audio Workgroups](https://developer.apple.com/documentation/audiotoolbox/understanding-audio-workgroups)
- [macOS capture authorization](https://developer.apple.com/documentation/bundleresources/requesting-authorization-for-media-capture-on-macos)
- [Notarization](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution)
