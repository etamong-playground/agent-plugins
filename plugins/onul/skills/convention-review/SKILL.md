---
name: convention-review
description: Review a change against applicable written repository, organization and agent conventions with rule-cited findings.
---

# Review conventions

Resolve the intended diff or paths and collect the instructions that actually apply to them.
Use the active client's loaded guidance, repository instructions and contribution policy; do not assume a provider-specific file path or an organization's rules.
Apply the instruction hierarchy and any explicit repository exceptions.

For each finding, report:

- File and line in the current revision.
- The written rule and its applicable scope.
- The conflicting behavior and a concrete correction.

Read the cited rule and affected code again before accepting a finding.
A preference without a written rule is a suggestion, not a convention violation.
An independent read-only reviewer is useful when supported and authorized; give it the exact revision and rule packet.
Do not turn the absence of an independent reviewer into a claim that a review occurred.

Fix confirmed in-scope violations only when implementation is authorized, then run checks affected by those fixes.
Do not apply a global default over an explicit repository exception or change unrelated conventions during the review.

Example: “Review this PR against CONTRIBUTING.md and the loaded agent instructions; return confirmed violations separately from suggestions.”
