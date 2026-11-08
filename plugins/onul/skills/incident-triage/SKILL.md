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
   Compare affected and healthy requests or components; do not infer a fleet-wide failure from one sample.
2. Follow request or trace identifiers across authorized service boundaries.
   Distinguish user-facing errors, internal errors, access records and audit events.
   Do not assume every service has the same fields, dashboard or log query language.
3. Check current configuration and recent relevant changes, then form competing hypotheses.
   For each proposed cause, state the mechanism and a discriminating observation.
   A successful restart does not prove what caused the incident.
4. Summarize direct observations, inferences and missing evidence separately.
   Use bounded, redacted excerpts; do not export full logs or expose tokens, personal data or customer payloads.
5. Propose the smallest recovery action with its risks, owner, authority and verification.
   Execute only if operational authority covers that action, then test the original user-visible failure and continuing health.

A lack of data is an observation about the query and access path, not proof that no incident occurred.
If a required source is inaccessible, identify that exact gap without requesting broad credentials.

Example: “Investigate increased 5xx responses since 09:00 UTC; no changes.”
Return the affected route/time window, correlated evidence, ranked hypotheses and a proposed next check, with no restart or configuration change.
