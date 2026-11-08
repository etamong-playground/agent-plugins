---
name: audio-validation
description: Validate an audio tool's numerical output, file handling, offline processing and real-device behavior with controlled fixtures and explicit measurement tolerances. Use for DSP regressions, audio app acceptance or release checks.
---

# Audio validation

Define the signal contract before selecting tests: supported encodings, sample rates, layouts, processing state, output units and acceptable error.
Separate correctness of numerical results, file/UI integration, resource use, live I/O and human listening.
Do not invent a broadcast/mastering target or claim standards compliance from a few examples.

Read [the validation matrix](references/validation-matrix.md) and select rows that apply to the feature.
Use deterministic generated signals or licensed fixtures; record their generation parameters and provenance.
Keep customer sessions and unreleased recordings out of uploads and logs unless explicitly authorized.

## Test-first numerical work

Choose one requirement-backed observable assertion, prove it fails for the defect, implement the smallest correction, then refactor.
Use analytic expectations or a separately established reference, not the implementation under test to generate its own answer.
For linear PCM sample peak, define full-scale normalization, maximum absolute amplitude across channels and the silence representation before computing dBFS.
Distinguish sample peak, RMS, true peak and integrated/short-term/momentary loudness; each needs its own algorithm and reference conditions.
Choose absolute/relative tolerances from floating-point precision, quantization and the actual algorithm rather than changing them until a test passes.
Cover chunk boundaries and final partial blocks, mono/stereo/multichannel handling, silence, impulses, known-amplitude tones, invalid/empty files and format changes as applicable.
Keep numeric test results independent of UI rounding and localization.

## Integration and performance

Use AVAudioEngine offline manual rendering when testing an engine graph without hardware; pure measurement functions need no engine.
Bound retry loops, render frames and file sizes; test cancellation, partial exports and preserved originals.
Keep UI/transport controls testable without requiring a physical device in every unit test.
Use Swift Testing or XCTest according to the existing target; use XCTest/XCUIAutomation for native UI workflows and supported performance tests.
Derive exact schemes and destinations from the repository before running xcodebuild; swift test alone does not exercise an Xcode app's entire UI or signing setup.

Measure memory, processing time and real-time callback overruns on a fixed workload and build configuration, with a stated warm-up and duration.
Buffer frames divided by sample rate gives one buffer interval, not measured end-to-end latency.
Record the device, driver, channel count, sample rate, I/O buffer setting, CPU architecture, OS/build and measurement method for hardware-dependent claims.
Device changes, disconnects, underruns and recovery need actual I/O tests; an offline test cannot certify them.
Listening evaluation should control gain/level, bypass alignment and comparison conditions relevant to the claim; record it as human evidence, not an automated pass.
Never start playback/capture or alter the engineer's device routing merely to run a test without task authorization.

## Evidence report

Return a compact matrix of requirement, fixture/configuration, expected result, observed result and pass/fail/unverified.
State which checks ran, which were simulated and which require a device, DAW or a human listener.
A missing environment is unverified, not skipped-as-passed.
Keep release decisions proportional to the actual feature; a file metadata inspector does not need a real-time engine qualification.

[Apple test frameworks](https://developer.apple.com/documentation/xcode/adding-tests-to-your-xcode-project) and [offline audio processing](https://developer.apple.com/documentation/avfaudio/performing-offline-audio-processing) describe the relevant platform capabilities.
