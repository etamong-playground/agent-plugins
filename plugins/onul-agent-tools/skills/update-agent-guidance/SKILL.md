---
name: update-agent-guidance
description: Turn an explicit request or recurring correction into a concise, correctly scoped agent rule or reusable skill, then verify the intended clients can load it.
---

# Update agent guidance

Preserve the conditions and scope of the user's instruction when making it durable.
An isolated task choice is not automatically a global rule.

## Establish the behavior

Identify the correction, the failure it prevents, and the desired behavior.
Distinguish an explicit durable preference from a one-time instruction.
Keep examples only when they disambiguate the rule; omit personal incident history and repetition counts.
Ask when different interpretations would impose materially different future behavior.

## Choose the owner and scope

Inspect existing repository and client guidance for the same behavior.
Use the narrowest applicable scope: task, repository, organization, or user-global.
Strengthen an existing rule rather than adding a competing duplicate.
Use a short rule for a standing constraint and a skill for a reusable multi-step procedure.
Keep permission boundaries and exceptions intact.

Find the source that owns a generated configuration before editing it.
Do not patch generated client files as a durable fix or assume one provider's memory store is shared with another.
Follow the existing configuration repository's workflow when one manages the files.
For guidance intended for multiple agents, keep one canonical rule or skill source and use each client's supported discovery mechanism.
Do not publish personal feedback, credentials, private project context, or runtime paths merely to explain why the rule exists.

## Write and verify

State an observable behavior and its trigger in plain language.
Remove redundant wording and unrelated best practices.
Read the final rule against the original request: conditions, actor, object, permissions, and exceptions must still match.
Check relevant configuration syntax, references, and a representative task where the previous behavior would fail.
When a skill changes, validate its metadata and its behavior where a realistic check is feasible.
Follow the authorized commit, review, activation, and publication process.
Verify intended clients actually discover the change; a saved file or merged PR alone does not establish activation.

## Report

Name the durable source, what behavior changed, how it was checked, and whether it is active.
State unperformed activation or validation plainly without claiming completion.
