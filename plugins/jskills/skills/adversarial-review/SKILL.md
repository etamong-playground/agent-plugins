---
name: adversarial-review
description: Adversarially review existing work with N parallel critics, each from a distinct perspective, then re-verify every critique in the main session and accept only the ones that survive — repeated for 2 rounds. Use when the user says "비판적으로 검토", "여러 관점에서 검토", "적대적 리뷰", "red team this", "critique my work", "review from multiple angles", "find what's wrong with this change", or asks to harden a finished change/design/plan before shipping.
---

# Adversarial Review

Fan out **N independent critics**, each prompted from a *distinct* perspective to find what is
wrong with the work under review. Critics are read-only and adversarial — their job is to
**refute, not praise**. The main session then **re-verifies** every critique against the actual
code/context and **accepts only the findings that survive**. Run the whole loop **twice**: round 2
critiques the *post-fix* state, catching regressions and deeper issues the surface noise was hiding.

This is the "perspective-diverse verify + adversarial verify" pattern, run interactively as a skill.
Diversity beats redundancy: N critics with N *different* lenses find more than N clones of the same lens.

## Arguments

- **scope** (default: current uncommitted diff + this branch's diff vs its base) — what is under
  review. May be overridden: a PR (`#123`), a path (`src/auth/`), a design doc, "the plan", a
  specific commit range. **Always restate the resolved scope in one line before dispatching** so the
  user can correct it.
- **`--rounds N`** (default: **2**) — how many full critique→verify→accept cycles. Use two rounds unless the request specifies another count.
- **`--critics N`** (default: **3–4**, chosen to fit the work) — number of parallel critics per round.

## Procedure

### 0. Establish scope and assemble the review packet
Determine exactly what is under review and gather it into a self-contained packet (diff, the
changed files in full, the requirement/spec or task that motivated it, applicable loaded agent and repository rules).
Each critic gets this packet quarantined in its prompt — they must not have to go hunting, and you
must not pull their raw exploration back into your context.

### 1. Pick distinct lenses (the "서로 다른 관점")
Assign each critic ONE lens, chosen from the menu below to fit the work — never two critics on the
same lens. Prefer the lenses where this particular work is most likely to be weak.

- **Correctness & logic** — bugs, wrong conditions, off-by-one, race conditions, wrong assumptions.
- **Requirements & spec fit** — does it actually do what was asked? missing cases, silent scope drift.
- **Edge cases & failure modes** — empty/null/huge inputs, partial failure, error handling, rollback.
- **Security & safety** — injection, secrets, auth/authz, destructive ops, unsafe defaults, supply chain.
- **Simplicity & over-engineering** — needless abstraction, dead code, simpler equivalent, duplication.
- **Interface & convention fit** — naming, API shape, consistency with the surrounding codebase's idioms. For findings that cite a specific written rule (repo/org/global guidance) rather than general taste, this lens may delegate to the `convention-review` skill instead of reproducing its packet-and-verify procedure.
- **Performance & resources** — hot paths, N+1, allocations, unbounded growth, blocking calls.

### 2. Dispatch critics in parallel (cheap model, read-only, adversarial)
Use the current client's supported subagent mechanism to run critics concurrently.
Select only models available to the current client and keep the main agent responsible for re-verification.
If independent subagents are unavailable, disclose that limitation before offering a sequential review; do not claim independent review occurred.

Each critic prompt must:
- Carry the review packet inline (quarantined context).
- Assign exactly one lens and instruct: *"You are an adversarial reviewer. Assume there are flaws.
  Your job is to find what is wrong through the lens of **<lens>** — do not praise, do not summarize
  what the code does. Be concrete."*
- Forbid editing (critics are read-only — only the main session edits, so parallel critics never
  clobber each other or the tree).
- Demand a structured finding list, each finding: **lens · severity (must-fix / should-fix /
  nit) · location (`file:line`) · the claim · why it's a problem · a concrete failure scenario ·
  suggested fix**. Empty list is a valid answer — better than invented nits.

### 3. Collect and de-duplicate
Merge the critics' findings. Collapse duplicates (same `file:line` + same root cause) into one,
keeping the sharpest articulation. Drop pure style nits unless the user asked for them.

### 4. Re-verify in the main session (the crux — do NOT trust critics blindly)
For **each** surviving finding, independently confirm it before acting. Critics hallucinate, misread
context, and flag non-issues:
- Open the actual code/context and check the claim holds *as stated*.
- Check the critic didn't miss a guard, a caller invariant, or an intentional design choice that
  makes the "bug" a non-issue.
- For high-stakes or non-obvious findings, spawn a **fresh independent verifier** prompted to
  *refute* the finding ("try to show this is NOT a real problem; default to refuted if uncertain").
  Accept only if it fails to refute.
- Verdict each finding: **CONFIRMED** (real, accept) or **REJECTED** (with a one-line reason).

### 5. Accept = apply the confirmed fixes
Apply confirmed fixes to the working tree (in the worktree, if the work lives in one), following applicable
repository guidance (comment rule, commit policy, conventions). Guardrails:
- Apply in-scope fixes under existing implementation authority, including already agreed behavior changes.
  A finding that expands scope, changes an unresolved contract or needs destructive authority requires the relevant user decision.
- If a confirmed finding is a design flaw rather than a line fix, record it as an open item rather
  than forcing a patch.

### 6. Next round
If more rounds remain (default total = 2): re-run steps 1–5 against the **updated** state. **Rotate
the lenses** — pick angles the first round didn't cover, or fresh critics on the same lenses — so
round 2 is genuinely new eyes, not a replay. Round 2 specifically looks for: regressions introduced
by round-1 fixes, and deeper issues that were masked by the round-1 surface problems.
- Early stop: if a round yields **zero confirmed findings** and the previous round also did, note
  convergence and stop even if rounds remain — there's nothing left to find.

### 7. Report
Summarize per round, compactly:
- Findings raised → verdict (CONFIRMED/REJECTED + reason) → what was changed.
- A final list of **accepted changes applied**, **deferred-to-user items**, and **open questions**.
- If nothing was accepted, say so plainly — a clean review is a real result.

## Rules

- **Critics never edit.** Read-only fan-out; the main session is the only writer. This is both a
  correctness guarantee (no parallel clobbering) and the source of the re-verification gate.
- **Distinct lenses, always.** Two critics on the same lens is wasted budget. Diversity is the point.
- **Re-verify before accepting — every time.** The skill's value is the gate, not the volume of
  critiques. A confidently-wrong critique that gets auto-applied is worse than no review.
- **Efficiency:** critics on the cheapest capable model, dispatched in parallel, context quarantined;
  judgment stays in the main session. Scale critic count and rounds to the stakes of the work.
- Respect applicable repository guidance for commit/push/PR policy when applying or proposing fixes.
