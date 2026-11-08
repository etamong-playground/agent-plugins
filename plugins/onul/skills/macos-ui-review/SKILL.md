---
name: macos-ui-review
description: Review or improve native macOS app workflows, keyboard/menu behavior, accessibility and task-state feedback. Use for SwiftUI/AppKit screens; browser screenshots alone cannot validate native controls.
---

# Native macOS UI review

Identify the user's actual sequence, required precision and interruption risks before changing a screen.
Inspect the existing SwiftUI/AppKit implementation and runnable target, or explicitly limit the review to supplied designs.
Preserve native conventions and the app's established shortcuts instead of replacing controls with website-style navigation.

## Task and state

Walk a representative task from the accepted requirements, including its start, main action, result and applicable recovery path.
Do not assume the app imports files, processes media or exports documents.
Check empty, loading, processing, cancelled, denied, disconnected and failed states that exist in that task.
A progress indicator must distinguish known progress from indeterminate work; cancellation must explain whether work and partial output have stopped.
Show task-specific labels, values, units and selection clearly; offer precise entry when the task needs it.
Distinguish current, pending and stale information where it affects a decision.
Choose useful display and accessibility-announcement intervals for frequently updated content.

## Native behavior and access

Check menu commands, contextual actions, standard shortcuts, focus order, text editing, undo/redo and save/open dialogs where the workflow includes them.
Provide keyboard alternatives to drag-and-drop, visible focus and accessible labels/values for custom controls and graphics.
Do not communicate error or status solely through color or sound.
Check resizing, narrow windows, long task-relevant labels and names, light/dark appearance and increased contrast with realistic data.
Keep destructive actions, unsaved changes and task-specific failures explicit where applicable; preserve user data.
For features that require OS permissions or devices, show their state and the relevant recovery action without changing system settings automatically.

## Verification

Use the actual native app with supported XCTest/XCUIAutomation or authorized native inspection when available.
Use Accessibility Inspector and keyboard/VoiceOver checks for native accessibility; a screenshot cannot establish semantics or keyboard behavior.
A browser-rendered mockup may compare layouts but does not verify a macOS menu, focus model, permission dialog or audio device interaction.
Do not operate a headless host's desktop, begin capture/playback or operate devices solely because a UI review was requested.
If native execution is unavailable, review code/designs, identify exact manual steps and expected outcomes, and label those outcomes unverified.
Report concrete mismatches with location, reader impact, proposed correction and verification method; omit invented cosmetic findings.

## Official references

- [macOS design](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos)
- [Keyboard behavior](https://developer.apple.com/design/human-interface-guidelines/keyboards)
- [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
