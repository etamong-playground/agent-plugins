---
name: macos-ui-review
description: Review or improve native macOS app workflows, keyboard/menu behavior, accessibility and audio-tool feedback. Use for SwiftUI/AppKit screens; browser screenshots alone cannot validate native controls.
---

# Native macOS UI review

Identify the user's actual sequence, required precision and interruption risks before changing a screen.
Inspect the existing SwiftUI/AppKit implementation and runnable target, or explicitly limit the review to supplied designs.
Preserve native conventions and the app's established shortcuts instead of replacing controls with website-style navigation.

## Task and state

Walk one representative task: open/import, select or inspect, act, cancel/recover and save/export.
Check empty, loading, processing, cancelled, denied, disconnected and failed states that exist in that task.
A progress indicator must distinguish known progress from indeterminate work; cancellation must explain whether work and partial output have stopped.
Show units, precision, channel identity and selected device clearly; use numeric entry as well as sliders when precise values matter.
Distinguish live meters from frozen/offline results and stale values from current measurements.
Avoid high-frequency VoiceOver announcements or UI redraws at the audio callback rate; choose useful display/announcement intervals without changing measurement accuracy.

## Native behavior and access

Check menu commands, contextual actions, standard shortcuts, focus order, text editing, undo/redo where appropriate and save/open dialogs.
Provide keyboard alternatives to drag-and-drop, visible focus and accessible labels/values for meters and custom graphics.
Do not communicate clipping, error or status solely through color or sound.
Check resizing, narrow windows, long file/device names, light/dark appearance and increased contrast with realistic data.
Keep destructive replacement, unsaved changes and export failures explicit; preserve the user's original file.
For capture/playback tools, show permission/device state and a predictable stop action without automatically changing system routing.

## Verification

Use the actual native app with supported XCTest/XCUIAutomation or authorized native inspection when available.
Use Accessibility Inspector and keyboard/VoiceOver checks for native accessibility; a screenshot cannot establish semantics or keyboard behavior.
A browser-rendered mockup may compare layouts but does not verify a macOS menu, focus model, permission dialog or audio device interaction.
Do not operate a headless host's desktop, start recording or play audio solely because a UI review was requested.
If native execution is unavailable, review code/designs, identify exact manual steps and expected outcomes, and label those outcomes unverified.
Report concrete mismatches with location, reader impact, proposed correction and verification method; omit invented cosmetic findings.

## Official references

- [macOS design](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos)
- [Keyboard behavior](https://developer.apple.com/design/human-interface-guidelines/keyboards)
- [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
