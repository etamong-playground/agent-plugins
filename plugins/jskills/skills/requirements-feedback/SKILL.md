---
name: requirements-feedback
description: Turn user interviews and feedback on an existing feature or specification into traceable requirement changes and acceptance examples. Use when feedback must be reconciled with a plan, prototype or implemented behavior.
---

# Requirements feedback

Anchor feedback to the intended user, their task, the observed problem and the current specification or behavior.
Preserve supplied wording when the requester asks to keep it; distinguish a quotation, an observation and an interpretation.
Do not treat every requested UI change as proof of the underlying problem.

## Resolve what changes

Inspect the relevant plan, prototype or implementation before classifying a gap.
For each material item, connect: source/context -> user task -> current behavior -> desired outcome -> acceptance example.
Classify it as a defect against the accepted contract, a clarified requirement, a new capability or an unresolved preference.
Separate contradictions and decisions about scope/cost/compatibility from routine implementation choices.
Reuse accepted answers; ask a small batch of questions only when the answers change behavior or validation.
An interview request authorizes analysis and a proposed specification, not implementation or external publication.

Make vague feedback observable.
For example, replace an inferred "make it fast" requirement with a question about the input size, user action, acceptable wait and measurement environment; do not invent the threshold.
For an audio tool, clarify whether "peak" means sample peak or true peak, which channels contribute and which units the user expects.
If a requirement is deferred, record the reason and the condition for reconsideration rather than leaving a hidden TODO in product copy.

## Update and validate

Within the authorized scope, update the canonical requirement and its worked acceptance example together.
Keep a compact decision/feedback record separate from the end-user guide; users of the product do not need the author's discussion history.
When implementation is authorized, map the changed requirement to a failing test or reproducible manual scenario, then implement and recheck it.
Use TDD for deterministic behavior and explicit native/hardware checks where automation cannot prove the result.
After the change, compare the original feedback with the actual observed result and ask the stakeholder only for judgments that still need their experience.
Return accepted changes, unresolved decisions and evidence without claiming that a prototype or code review establishes user acceptance.
