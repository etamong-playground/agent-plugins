---
name: macos-app-development
description: Plan, implement or verify a macOS app from the user's tasks and explicit requirements, choosing platform integration, UI and tests to fit the project. Use for general Mac app development; add domain workflows only after their features are confirmed.
---

# macOS app development

Start with the user's task and intended outcome, not a demonstration project or a technology choice.
A profession, industry or prior example is context, not a feature specification.
Do not infer file processing, recording, metering, DSP, DAW integration, networking, AI or a distribution model from it.

## Establish the contract

Inspect an existing repository, plan and runnable target before changing them.
For a new app, ask about the current workflow, intended users, recurring difficulty, inputs, outputs and one observable successful task.
Clarify error/recovery behavior, data ownership, persistence, required integrations and the first version's exclusions only where they affect the selected task.
Distinguish confirmed requirements, proposed options, unknowns and deferred decisions.
Reuse accepted answers; ask a small batch of questions rather than making the user complete a technical architecture questionnaire before describing their work.
Use requirements-feedback for changes to an existing specification when available.
An interview or planning request does not authorize implementation or publication.

## Select a macOS implementation

Confirm the supported macOS versions, CPU architectures, installation audience and relevant OS integrations.
Preserve the existing language and framework when they fit the task.
Choose SwiftUI/AppKit or another suitable stack from the confirmed requirements, existing code and maintainability constraints; do not rewrite a working app to follow this skill's examples.
Native window/menu/file behavior, accessibility, device access and distribution can influence that choice.
Identify the actual build/test commands and toolchain; do not claim that a CLI package test covers an entire app target.
If the chosen native target needs Xcode, verify the selected Xcode/SDK rather than treating Command Line Tools as a full app environment.

Keep business rules, state/persistence, integrations and presentation testable at useful boundaries.
Build a single end-to-end user task before adding optional capabilities.
Define only the loading, empty, active, failed, cancelled and completed states that apply to it.
Request OS permissions when the selected feature needs them and provide a clear denial/recovery path.
Do not broaden entitlements or alter device/system settings as a generic setup step.

## Implement and verify

Turn one confirmed acceptance example into a failing test or a reproducible interaction, then implement the smallest useful slice.
Use deterministic unit/integration tests for rules and data; use the selected framework's app/UI tooling for actual interactions.
Check keyboard, menus, focus, accessibility, resizing and appearance in the real Mac app where relevant.
Use macos-ui-review for SwiftUI/AppKit screens when available; a browser mockup does not establish native interaction behavior.
Choose performance workloads, thresholds and methods from the actual use case before judging speed or memory.
A successful build is not evidence of user acceptance, OS permission handling, hardware compatibility or correct installation.

Add specialized workflows only when their features have been requested and accepted.
For confirmed audio processing or I/O, macos-audio-app and audio-validation can supply additional constraints; an app used by a sound engineer need not process audio at all.
Other integrations similarly require their own explicit data, permission and verification contracts.

## Deliver

Report implemented behavior, commands actually run and results observed against the agreed acceptance examples.
Keep unavailable native, hardware or external-integration checks unverified with concrete steps and expected outcomes.
Choose signing, sandbox and distribution requirements only after the delivery channel is agreed; consult current platform documentation.
Do not publish or change signing identities solely because implementation was requested.

## References

- [macOS design](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos)
- [Xcode tests](https://developer.apple.com/documentation/xcode/adding-tests-to-your-xcode-project)
- [macOS distribution and notarization](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution)
