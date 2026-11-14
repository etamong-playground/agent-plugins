---
name: cleanup-orphan-worktrees
description: Review stale worktrees, prune missing registrations and remove approved worktrees or branches while preserving concurrent work and private files.
---

# Clean up stale worktrees

Merged PR state identifies a candidate, not permission to discard a worktree.
Start read-only and preserve existing item-scoped approval across resumptions.

## Inventory and review

Read `git worktree list --porcelain` for every repository in the requested scope.
Identify primary and client-managed checkouts from actual paths and Git metadata, never from branch-name conventions.
Report primary checkouts, existing linked directories and missing registrations separately; `git worktree prune` does not remove existing directories.
Account for every linked worktree, using a machine-readable manifest for large batches and a grouped summary for the user.

For each candidate, inspect ownership, current HEAD and branch, tracked changes, untracked and ignored files, unpushed commits, PR state, active processes and task/session references.
Verify that the merged PR's head matches the local HEAD; squash merges need not make the branch an ancestor of the default branch.
Keep primary, locked, active, dirty and ambiguous worktrees.
Keep open-PR worktrees unless their disposition is separately established; an open PR alone does not establish active ownership.
A missing PR may be unpublished work, and a closed PR may still contain wanted changes.
Record a concrete retention reason rather than treating an old branch or a directory named `.tmp` as abandoned.

## Approve a batch

Present exact paths, repository identities, branches, HEADs, merge evidence and any unpushed commits.
Separate worktree removal, branch deletion and registration pruning in the proposal.
Include estimated reclaimable space, excluded paths and the handling of ignored files.
Obtain item-scoped deletion authority unless those exact actions are already authorized.
A request to review everything authorizes investigation; it does not authorize deletion.

Ignored files need their own disposition even when Git reports a clean checkout.
Classify regenerable outputs from repository evidence; preserve unknown files, credentials, recovery data, plans and checkpoints.
Offer approved relocation to a retention directory outside every removal target when private files are the only obstacle.
Record each original and retained path, verify the retained data and exclude it from reclaimed-space estimates.
If a retained directory also contains unchanged tracked files, retain it intact and restore only those tracked paths from the recorded HEAD before normal worktree removal.
Do not overwrite changed files to make a checkout appear clean.

## Execute and verify

Revalidate approval scope, HEAD, status, ownership, processes, task references and preservation destinations immediately before each removal.
Skip changed entries and continue independent approved entries; report each skip.
Keep an execution ledger with completed removals and retained-path mappings so an interruption does not repeat actions.

For a client-managed checkout, use the supported archive interface and its confirmed identity.
If the current client cannot archive it, report the limitation; do not delete it through the filesystem.
For a manual checkout, use `git worktree remove <path>` without force.
A dirty-state refusal stops that entry; forced removal needs separate informed authorization.
After any failure, inspect both the directory and registration before retrying: Git may have removed the registration while leaving files behind.
Preserve private data and record partial results rather than assuming rollback succeeded.

Delete a local branch only after successful worktree removal, confirmation that no remaining worktree uses it, and explicit branch-deletion authority.
A branch deletion refusal requires investigation, not automatic `-D`.
Preview registration pruning with `git worktree prune --dry-run --verbose`; verify reported paths are truly missing, rather than temporarily unavailable, before approved pruning.
Never remove the primary checkout, delete a remote branch or change PR state through this workflow.

Re-read worktree and branch lists and verify preserved data at its recorded destination.
Report actual directory removals, registrations pruned, retained candidates and branches, and remaining linked worktrees separately from primaries.
Measure free space on the same filesystem before and after, distinguishing net free-space change from directory-size estimates and concurrent disk activity.

Example: “Review all worktrees and remove the approved merged ones, keeping branches and private files.” produces a full inventory and exact manifest first.
After approval, remove only unchanged eligible entries, retain private files at recorded paths, and report measured space plus every skip.
“Show worktrees for merged PRs first.” produces only the candidate list and evidence.
