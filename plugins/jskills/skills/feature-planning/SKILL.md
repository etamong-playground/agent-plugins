---
name: feature-planning
description: Plan a feature, fix, or implementation task from repository evidence, with scope, acceptance criteria, dependencies, and a resumable checkpoint; reuse an accepted plan when available.
---

# Feature planning

Use the repository's existing plan, tracker, and review conventions.
This sharing edition has no organization-specific tracker, credentials, issue claims, or publication rules.

## Establish scope

Read the repository guidance, existing plans, and the task or issue discussion.
Identify the requested outcome, related work, existing decisions, and the smallest independently useful slice.
A question or plan-only request does not authorize implementation or external writes.
Do not create or update an issue without the user's authorization or an applicable repository grant.

## Ground the plan

Inspect the code path and affected examples before proposing changes.
Separate known behavior, user requirements, assumptions, and unresolved choices.
Ask only questions whose answers change scope or approach; continue independent authorized work.
Use domain-modeling for ambiguous terms and compare-spike only when an implementation comparison is authorized.
Reuse accepted decisions rather than reopening them without new evidence.

## Write the plan

Follow an existing local plan format; otherwise include:

- Outcome and scope, including exclusions.
- Evidence and decisions, with references a reader can open.
- Work slices and dependencies in execution order.
- Observable acceptance criteria and relevant validation commands.
- Current checkpoint, remaining decisions, and next action.

Match the detail to the task.
Prefer one coherent plan over duplicated local and remote versions that can drift.
Keep temporary plans out of commits when that is the repository convention.
Do not impose a new plan directory or tracker on an established project.

## Continue within authorization

For implementation requests, proceed after the applicable decisions and approvals are settled.
Checkpoint when a slice finishes, an approach changes, or work is handed off.
Record what changed, what was verified, what remains, and where the task branch and artifacts live.
Respect concurrent work and preserve unfamiliar edits until ownership is established.
Publish updates only through already authorized repository workflows.

## Finish

Compare the result against every acceptance criterion.
Distinguish committed code, merged code, deployed behavior, and live verification.
Keep an incomplete plan when a required check or delivery step remains.
Remove only task-owned temporary planning material after its completion conditions are met.
