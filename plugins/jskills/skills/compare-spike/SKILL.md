---
name: compare-spike
description: Settle a technology/library adoption question by building competing spike prototypes and comparing measured facts. Use when the user asks "should we adopt X or keep our own", wants to compare libraries/SDKs/approaches hands-on, or asks for an A/B prototype evaluation (비교 스파이크).
---

# Comparison Spike

An adoption decision is settled by **hands-on facts, not brochure claims**. One spike per candidate, apples-to-apples, measured, then one recommendation.

## Procedure

1. **Frame the decision.** Pin down: the candidates (2–3), the hardest feature each must express (the differentiator, not the demo case), and the criteria that will decide — bundle delta, dependency-tree consequences, expressiveness for the hard feature, maintenance surface, license. Done when the user agrees these criteria decide the question. An existing in-house implementation is a candidate at zero spike cost.
2. **One spike per candidate.** Use separate local task branches or worktrees by default. Publish separate draft PRs only when authorized by the user or repository workflow. A real integration in the actual app — a test route/page wired to real data shapes — not a sandbox toy. Implement the *same scenario* in every spike; without apples-to-apples the comparison is void.
3. **Measure.** Per candidate, one entry per criterion from step 1 — measured or verified, no "probably fine":
   - Runtime-appropriate resource changes against the same workload and baseline: browser bundles where relevant, or startup, RSS, allocations or binary size for native/server work.
   - Dependency consequences: peer conflicts, forced version promotions of shared deps, overrides needed.
   - App-imposed constraints that apply: CSP, i18n init, SSR, offline.
   - The hard feature: expressible at all? Partial counts only as partial, spelled out.
4. **Report + recommendation.** A facts table (criteria × candidates), risks measurement couldn't retire flagged as unverified, and exactly one recommendation with reasoning. Decision-centric: what to do and what it costs.
5. **Decommission.** After the user decides, preserve the comparison result. Close published candidate PRs or write durable repository records only within existing authority; a comparison request alone grants neither action.
