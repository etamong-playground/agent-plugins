---
name: fan-out-sessions
description: Split authorized work into independent slices and coordinate necessary Claude Code or Codex sessions. Use when the user requests parallel sessions or a concrete independent split warrants them within runtime limits. Use fan-in-sessions to collect the results.
---

# Fan out sessions

Work directly when a split would add more coordination than useful parallelism.
Read `agent-session` before launching; it owns provider selection, launch/message routes, goal authorization, monitoring and safe closure.
A request to improve these skills is not a request to launch sessions as a demonstration.

The current session owns the split, integration and user decisions until the user chooses another coordinator.
Preserve the user's chosen coordinator and accessible observation interface.
Executors may be Claude or Codex; choose for required capabilities and the user's preference, not to use both providers on every task.

## 1. Split only independent work

- Each slice has one owner, a clear completion condition and an isolated worktree/branch when it writes code; follow the repository's issue and PR policy.
- Avoid overlapping edits. If overlap is necessary, name the owner of each shared section and the dependency order in both briefs.
- Work that requires another slice's unmerged code is a later phase, not a parallel writer.
- Use the smallest useful set of sessions and stay within the user's authorized count; do not treat a concurrency ceiling as a target.
- Show the slice, provider, host, scope and reason for a separate session before launch. Reuse a split already approved; runtime requirements for explicit chat creation still apply.

## 2. Prepare the brief and return route

Extend the existing task plan or use the repository's handoff location.
If neither exists, keep a brief in the authorized task scratch directory and report its absolute path.
Keep one common section and one section per slice, in English.

The common section names the coordinator's provider, host and full ID; the user's constraints and actual grants with their source; shared decisions; reporting routes; and the prohibition on further session creation without authorization.
Each slice names its host, repository, worktree/branch, scope, overlap owners, acceptance criteria and stop conditions.
Codex goal use must be explicitly authorized and supported; a general fan-out request does not request a goal.

Agree on a usable reply route before launch.
Native messages, process results and a disclosed result artifact have different delivery semantics; follow `agent-session` rather than assuming replies arrive automatically.
A local file path is not a cross-host handoff.

Executors report receipt, PR creation, blockers, material changes and completion to the coordinator through that route.
They include PR URL/head, validation, pushed/unpushed work, unresolved findings and next action in the final report.
They relay user decisions to the coordinator instead of opening an invisible interactive dialog, and continue only work independent of the missing answer.
Approval/authentication requirements are not suppressed; report them for the user to handle.

## 3. Launch and verify

Use the destination route from `agent-session`; do not duplicate its commands in this skill.
Name slices consistently, for example `<task> S1`, and record each full returned identity rather than relying on a name prefix.
Each code-writing executor follows its provider's worktree rules; do not copy another live worktree or share a branch between writers.
Verify identity, host, directory and initial state before reporting a session as running.
Report slice, provider, session ID, host, model, permission mode and observation route to the user.
If launch status is ambiguous, investigate before retrying.

## 4. Coordinate and observe

- Relay user decisions verbatim to affected executors; identify reversals and verify receipt before dependent work proceeds.
- Resolve questions already settled by the agreed strategy; batch decisions that genuinely need the user.
- Relay dependency changes with PR URL and head SHA.
- Use supported event notifications or bounded state checks; do not assume cross-provider messages wake the coordinator.
- Use state-only observations. Do not print raw session logs or treat keyword redaction as a credential-safety guarantee.
- A waiting approval is not fixed by broader permissions. A stalled session gets diagnosis, not an automatic restart or duplicate writer.

Before a coordinator disconnect, checkpoint identities, pending decisions, next observer and permitted continuation.
On reconnect, observe existing executors before opening replacements.

## 5. Finish each slice

Accept the result against its completion condition, then use `agent-session` to stop task-owned execution without deleting unmerged work.
A pushed branch is not permission to remove its worktree, and archiving a chat is not proof that a goal stopped.
Update the session table with the PR state, preserved work and next owner.
Use `fan-in-sessions` when the results are ready to integrate, the user asks to collect them, or a limit/blocker prevents continued parallel work.

## Worked request and completion evidence

For “split documentation and an independent test fixture update between two sessions”, verify that the slices do not share files, record each host/repository/session identity and return route, and preserve the requested approval boundaries.
Completion requires each slice's evidence and the coordinator's integration check, not merely accepted launch requests.
If the runtime requires an explicit request for new chats, obtain it before launching; installing this skill grants none.
