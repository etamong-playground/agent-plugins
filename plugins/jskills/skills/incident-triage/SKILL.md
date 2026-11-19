---
name: incident-triage
description: Investigate service incidents using authorized logs, metrics and traces, separating observations from hypotheses before proposing recovery.
---

# Triage a service incident

Establish the affected service, environment, reported symptom, incident time and timezone, user impact and investigation authority.
Start read-only and use the existing observability interfaces and credential broker where available.
Do not infer deployment or restart authority from permission to investigate.

1. Record observed errors, response codes, latency, availability and affected operations for a bounded time range.
   Preserve timezone and clock-offset uncertainty.
   Compare affected and healthy requests or components and a healthy baseline at comparable traffic; do not infer a fleet-wide failure from one sample.
   Check traffic volume and collection health: missing requests at the application can indicate an upstream failure, while missing telemetry can indicate a broken observation path.
   Separate successful and failed request latency, inspect tail percentiles with their sample volume, and compare errors as rates with their request denominator.
   Fast failures or excluded timeouts can make latency look healthy during an outage.
2. Follow request or trace identifiers across authorized service boundaries.
   Distinguish user-facing errors, internal errors, access records and audit events.
   Do not assume every service has the same fields, dashboard or log query language.
3. Check current configuration and recent relevant changes, then form competing hypotheses.
   For each proposed cause, state the mechanism, predicted observation and next discriminating query.
   Use resource, dependency and queue evidence to narrow user-visible symptoms: rising latency with low CPU calls for checking waits, while high CPU calls for checking load, profiles and throttling.
   Inspect pool wait and resource hold duration before recommending more connections or workers.
   Check retry volume, cache misses and queue age where relevant; increased traffic can be repeated work rather than new demand.
   A successful restart does not prove what caused the incident.
4. Summarize direct observations, inferences and missing evidence separately.
   Use bounded, redacted excerpts; do not export full logs or expose tokens, personal data or customer payloads.
5. Propose the smallest recovery action with its risks, owner, authority and verification.
   Execute only if operational authority covers that action, then test the original user-visible failure and continuing health.
   Once impact is established, prioritize an authorized, verifiable recovery over exhaustive diagnosis; preserve available evidence safely and continue causal analysis after recovery.
   Compare the same route, population and observation window across gateway, application and dependency records before explaining conflicting outcomes.
   Check timeout budgets, cancellation propagation and work continuing after callers have stopped waiting where applicable.

A lack of data is an observation about the query and access path, not proof that no incident occurred.
If a required source is inaccessible, identify that exact gap without requesting broad credentials.

After recovery, record the first observed symptom, detection, response and recovery times, with clock uncertainty.
Separate detection gaps from response delays and turn confirmed gaps into scoped dashboard, alert, runbook or code changes under the project's tracking conventions.
Do not create follow-up work or change alert routing without the applicable authority.

Example: “Investigate increased 5xx responses since 09:00 UTC; no changes.”
Return the affected route/time window, correlated evidence, ranked hypotheses and a proposed next check, with no restart or configuration change.

Example: “Requests are slow, but CPU is low; investigate read-only.”
Compare the affected route's traffic, success/failure latency and pool-wait metrics over the same window.
Rising pool wait supports a waiting-work hypothesis; use dependency traces or query evidence to distinguish slow execution from lock contention or connection leaks before proposing a fix.
