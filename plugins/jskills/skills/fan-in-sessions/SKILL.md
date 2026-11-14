---
name: fan-in-sessions
description: Collect results from parallel Claude Code or Codex sessions, verify integration within existing grants, stop task-owned execution safely, and preserve remaining work in one checkpoint. Use when the user requests fan-in or parallel work is ready to collect.
---

# Fan in sessions

Read `agent-session` for provider-specific observation and closure.
The coordinator owns integration and the remaining-work record; collection does not grant merge, apply, goal pause or destructive cleanup authority.

## 1. Inventory the recorded sessions

Use the task plan or fan-out brief's exact provider, host and full IDs, including superseded identities.
Confirm current state through the appropriate provider route; a name prefix alone does not establish ownership.
For each slice collect worktree/branch, uncommitted paths, remote branch head, PR URL/head/state, checks, unresolved reviews and goal state when applicable.
Compare the local branch to its verified remote branch to establish what is unpushed; commits ahead of the base branch are not necessarily unpushed.
An exited session still needs its branch and PR checked.
Do not expose raw transcripts or logs to build this inventory.

## 2. Collect final states

Send an authorized wrap-up request through the recorded route: stop starting new work, preserve authorized changes, and return PR URL/head, pushed and unpushed work, validation, unresolved findings and next action.
Do not ask for commits or pushes beyond the original grant.
Track receipt and the final result separately; a queued message or idle state is not a reply.
For an unavailable executor, inspect its task-owned artifacts and report what remains uncertain.
Do not take over writes until its execution is confirmed stopped or the user resolves concurrent ownership.
A goal pause/cancel remains subject to the user's explicit request and the target's supported controls.

## 3. Integrate within the existing grant

Order dependencies before their consumers.
Merge only with applicable authority and all required gates passed; otherwise leave the PR open and name the next owner.
After each authorized merge, sync remaining dependent branches and retarget children under the shared workflow.
A live executor owns its rebase/fixes; a confirmed stopped executor's work can be taken over within the existing scope.
Resolve conflicts using both slices' intent and rerun relevant gates.

Verify the combined result after integration using repository-required checks.
Observe deployed state when deployment was authorized or triggered by the authorized merge.
If no integration occurred, report that clearly rather than claiming an integrated default branch passed.

## 4. Stop execution and preserve work

Use `agent-session` to stop only task-owned executors whose final checkpoint was accepted, or those the user explicitly asked to stop.
Do not automatically stop independently opened user sessions.
Report confirmed execution state, goal state and archive state separately; unsupported control remains unconfirmed.
Do not remove a superseded session while another runner uses its worktree.

Keep unmerged worktrees/branches even when pushed, unless disposal was explicitly authorized.
Clean up only confirmed-merged, task-owned work through its provider's mechanism; Codex app-managed worktrees use `archive_worktree` from their owning chat.
Never use `claude rm` as a synonym for stop or delete remote branches.
Recheck the exact managed identities after closure; report any still active or unconfirmed.

## 5. Checkpoint and report

Fold unfinished work into the existing task plan or write a self-contained handoff in the repository's established location.
Record each provider/host/ID, branch or PR, preserved local state, unresolved decisions and next owner.
Retire the fan-out brief only after its useful contents and results are preserved in that checkpoint or durable artifacts.

Report every PR as a full URL with its final state, integration verification, session/goal state and remaining actions.
Record the outcome through the repository's existing reporting workflow when authorized; do not invent a journal destination.

## Worked request and completion evidence

For “split documentation and an independent test fixture update between two sessions”, verify that the slices do not share files, record each host/repository/session identity and return route, and preserve the requested approval boundaries.
Completion requires each slice's evidence and the coordinator's integration check, not merely accepted launch requests.
If the runtime requires an explicit request for new chats, obtain it before launching; installing this skill grants none.
