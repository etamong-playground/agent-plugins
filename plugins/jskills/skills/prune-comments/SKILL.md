---
name: prune-comments
description: Audit the comments in the regions a branch changed, or in a whole file, path or repo on request, and delete the ones the code already says. Use when the user says "불필요한 코멘트 정리/제거", "주석 정리해줘", "prune the comments", "remove redundant comments", "clean up the comments", or when a change has left behind narration comments.
---

# Prune Comments

Find comments that carry nothing the code does not already say, and delete them.
The rule this enforces is the global Comment Rule: a comment must carry the **why** — hidden constraints, non-obvious invariants, workarounds for specific bugs.
Everything else is noise a reader has to check against the code.

## STEP 1 — Fix the scope before reading anything

Ask which one applies if the request does not say:

- **Changed hunks** — the comments inside the regions the current branch changed, including ones that predate the branch. **The default.**
- **Added lines only** — just the comments the branch introduced. Narrower still; use it when a changed region carries old comments the branch has no mandate to clean.
- **Touched files** — every changed file in full. Use it when the branch rewrote the file, or when the user asks for it.
- **Path** — one file, module, or directory the user named.
- **Repo** — a full sweep. Available on request, but confirm before starting; it produces a large diff that has to be reviewed as its own change.

A repo sweep never rides along with unrelated work. Ship it as its own commit or PR.

## STEP 2 — Collect the candidates

Read the code around each comment, not the comment list alone — the judgment is whether *this* comment says something *that* code does not.
So collect files and read them; never work from a list of comment lines stripped of their surroundings.

For the default scope that means `git diff --unified=10 <base>...HEAD` to locate the changed regions, then opening each file and reading those line ranges in the working tree — the diff picks the range, the file supplies the code. Not `git diff | grep '^+'`, which yields exactly the context-free comment list this step forbids and hides every stale comment sitting in a region the branch edited.
The same holds for the added-lines and touched-files scopes: the command only decides what is in range, and the judgment always happens against the file.

For a large scope, delegate the sweep to a subagent that returns candidates with file, line, the comment text, and the code it sits on, so the raw dump stays out of the main session.

## STEP 3 — Classify each one

**Delete:**
- Restates the next line or the signature (`# returns the user` on `return user`).
- Narrates control flow (`// loop over items`, `// if the user is admin`).
- Section banner or decorative divider (`// --- helpers ---`, `#####`).
- Change history, task notes, author initials, dates — git holds these.
- Reader-directed remarks (`// note that`, `// as you can see`, `// don't forget to`).
- Docstring that only re-lists the parameters the signature already declares.
- Commented-out code.

**Keep:**
- Why a non-obvious choice was made, or why the obvious alternative fails.
- A workaround pinned to a specific bug, version, or upstream issue — keep the link.
- An invariant, precondition, unit, ownership or lifetime the types cannot express.
- A legal header, license block, or generated-file marker.
- A pragma or tool directive (`# noqa`, `// eslint-disable-next-line`, `//go:generate`, `# type: ignore`) — these are code, not prose.
- `TODO`/`FIXME` that names a real, still-open follow-up.

**Rewrite instead of delete:**
- The comment decodes an unclear name, a magic number, or a dense expression → rename, extract a named constant, or split the expression, and drop the comment.
- The comment gestures at a real constraint but states it vaguely → state the constraint.

When a comment is genuinely ambiguous, keep it and list it for the user rather than guessing.

## STEP 4 — Apply

Delete in place. Two things to watch:

- Removing a line comment can leave a stray blank line or break the shape of a block — read the result, do not trust a line-delete.
- A comment inside a string, heredoc, template literal, or markdown code fence is data, not a comment. Never touch it.

## STEP 5 — Verify

- The scope's build, type check, lint, and tests still pass. A comment removal that breaks a build means a pragma or a directive was deleted — restore it.
- `git diff` shows deletions only. Any changed code line is either the STEP 3 rewrite case or a mistake.
- Report the ambiguous ones you kept, so the user can decide.

Commit as its own change, in the repo's own language and scope vocabulary, never mixed into a behavior change.
