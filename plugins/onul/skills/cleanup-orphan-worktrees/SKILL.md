---
name: cleanup-orphan-worktrees
description: Inspect and remove explicitly approved stale worktrees and local branches while preserving dirty, ambiguous or concurrently owned work.
---

# Clean up stale worktrees

Merged or closed PR state identifies a candidate, not permission to discard a worktree.

1. Read `git worktree list --porcelain` and identify the primary checkout.
   Inspect the task/branch ownership, PR state, local status, untracked files and commits not present remotely for each candidate.
   Read actual paths rather than constructing them from branch names.
2. Keep open-PR, active-session, dirty and ambiguous worktrees.
   A missing PR may be unpublished work; a closed PR may still contain wanted changes.
3. Present the exact paths and local branches proposed for removal, with their reasons and any unpushed commits.
   Obtain item-scoped deletion authority unless those exact removals are already explicitly authorized.
4. For a client-managed checkout, use the supported archive interface and its confirmed identity.
   If the current client cannot archive it, report the limitation; do not delete it through the filesystem.
   For a manual checkout, use `git worktree remove <path>` without force.
5. Delete a local branch only after removal succeeds, no remaining worktree uses it, and the deletion is authorized.
   A branch deletion refusal requires investigation, not automatic `-D`.
6. Re-read worktree and branch lists and report the actual removals and retained candidates.

Never remove the primary checkout, delete a remote branch or change PR state through this workflow.
A dirty-state refusal stops deletion; forced removal needs separate informed authorization.

Example: “Show worktrees for merged PRs first.” produces only a candidate list and local-state evidence.
