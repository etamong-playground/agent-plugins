# Technical writing checks

Use these checks for Korean technical documents alongside the parent skill's language and register conventions.
Review technical correctness separately from wording: a natural sentence can still describe the wrong behavior.
Apply only relevant checks and preserve the document's existing format.

## Meaning and evidence

Preserve the actor, target, condition, timing, sequence, quantity, negation, exception and obligation when editing.
Checking a state does not mean changing it; a sufficient condition does not become a necessary one.
Distinguish observed behavior, requirements, recommendations, options, plans and unverified assumptions.
When implementation, specifications and tests disagree, record the discrepancy rather than selecting a convenient interpretation.
Do not invent a default, version range, error, guarantee or recovery mechanism to make a sentence more specific.

Name the applicable product, version and environment when behavior depends on them.
Keep supported, tested and illustrative environments distinct.
State performance and cost claims with their workload, measurement method and scope.
Explain prerequisites without calling the task easy or obvious.

## Values and completion

State units, measured objects, inclusive or exclusive boundaries and the basis of a range.
Keep omission, null, empty values, false and zero distinct according to the actual interface.
For a duration, identify the starting event; for retry counts, say whether the initial attempt is included.
Use time zones where they matter and distinguish connection, read and whole-operation timeouts.
Distinguish expiration after creation from expiration after access.

Separate request acceptance from operation completion and durable persistence.
A cancellation request is not cancellation completion, and an asynchronous API is not necessarily thread-safe.
Claims such as atomic, immediate or exactly once need explicit preconditions and scope.
No response does not establish that the server made no changes.
Do not turn a tested version range into a future compatibility promise.

## API and interface contracts

Document the applicable public contract rather than every internal exception.

| Area | Check |
| --- | --- |
| Entry point | Exact function signature, HTTP method/path or CLI invocation, with the behavior it provides. |
| Inputs | Meaning, types, required/optional status, defaults, units, ranges, omission/null behavior, validation and cross-parameter constraints. |
| Results | Meaning, type, ordering, duplicates, empty results, ownership, mutability and the point at which work completes. |
| Failure | Failure conditions and channels, partial effects, recovery, and error precedence only when guaranteed. |
| Effects and lifetime | Mutation, I/O, logging, resource acquisition, ownership transfer, cleanup and behavior after closure. |
| Concurrency | Caller synchronization, ordering, retry eligibility/count/delay, duplicate effects, idempotency scope, timeout and cancellation. |
| Interface details | Relevant authentication, pagination, rate limits, stream delivery/backpressure, CLI exit status and interactivity, configuration precedence and apply timing. |
| Stability | Public guarantees versus implementation details, deprecation/removal state and verified migration paths. |

For an asynchronous or lazy API, distinguish its immediate object from eventual results and later errors.
When string length matters, specify bytes, code points or user-perceived characters and the relevant normalization behavior.
Do not attach a network checklist to a pure function or assign an unsupported removal date.

## Runnable examples

Label complete runnable examples, insertion snippets and pseudocode accurately.
For a complete example, include needed imports, setup, inputs, invocation, result checks and cleanup.
State the relevant runtime, dependencies, shell and working directory.
Distinguish reproducibility pins from recommended versions.
Keep validation, error propagation and secret handling that are necessary for safe reuse.
Explain material omissions and placeholder replacement before commands, including shell metacharacters that need quoting.
Separate copyable commands from prompts and output; distinguish observed output from expected and variable fields.

Execute complete examples in their stated environment only when authorized and feasible.
State untested, mocked or inaccessible boundaries honestly.
Documentation work does not authorize external writes, paid operations or access to production data.
Preserve generator tags, code, literal messages and canonical type information during wording edits.

## Operational procedures

State scope, target, prerequisites and material risks before actions, then provide success checks and cleanup.
Separate steps that have independent failure or rollback decisions.
Explain optional and conditionally required branches and where they rejoin.
Before a destructive, privileged, costly or disruptive operation, state its impact, stop conditions and verified recovery limits.
Do not invent a dry-run flag or rollback support, or disable a security check as the default example.
Check duplicate effects and costs before recommending a retry.
Identify sensitive diagnostic fields that must be redacted.

Troubleshooting starts with observable symptoms, then checks, confirmed or possible causes, actions and verification.
Changelogs state changed behavior, affected users or versions, compatibility impact and required migration or verification.

## Final review

Check links, signatures and examples against their actual sources.
Treat length, passive voice and vague referents as review signals rather than automatic rewrite targets.
Keep literal values, Markdown, quotations and meaning intact.
Update affected examples, glossaries and translations when behavior changes, without requiring new files for every task.
Report unresolved technical questions separately from corrected text.
If missing safety or data-loss information prevents a usable procedure, report the blocker instead of inventing executable steps.
Do not add mandatory reviewer names, approval records or new gates to a writing task.
