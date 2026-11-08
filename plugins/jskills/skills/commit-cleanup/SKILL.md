---
name: commit-cleanup
description: Reorganize an owned branch into logical commits while preserving its exact final tree and protecting concurrent work.
---

# Clean up commit history

Establish the branch, intended base, ownership and publication boundary before rewriting history.
A request for a proposed split is read-only.

1. Require a clean worktree and inspect the existing PR and review threads.
   Preserve unrelated or another session's work.
   Record the old HEAD and tree, the intended base and exact remote branch head.
   Keep a recoverable local backup ref; push a backup only when remote publication is authorized.
2. Do not merge or rebase onto a newer base merely to clean history.
   If a base update is separately required, resolve and validate it first, then record the content tree to preserve.
3. Rebuild commits in a task worktree in dependency order, staging each logical group deliberately.
   Do not reset a shared or main checkout.
   Include tests and docs with the behavior they verify or explain.
4. Compare `git rev-parse 'HEAD^{tree}'` against the recorded target tree and inspect the rebuilt diff against its base.
   A mismatch means content changed; resolve it before publication.
5. Explain each commit's intent and the useful review order.
   Keep the backup ref until the rewritten branch is verified.

Publish only within established authority.
Warn before rewriting a PR with inline review threads because their anchors may become outdated.
For an owned branch whose rewrite is authorized, use `git push --force-with-lease=<branch>:<recorded-remote-sha>`.
A rejected lease requires inspecting the unexpected remote work; never retry with a weaker force option.

Example request: “Split my WIP branch into reviewable commits; keep its final tree identical and do not push.”
The result is local commits, tree-identity evidence and a review guide, with no remote mutation.
