---
name: observability-onboarding
description: Design or improve service instrumentation, monitoring dashboards and alerts using the existing telemetry stack, with actionable signals, bounded labels, correlation and privacy.
---

# Add service observability

Inspect the service, telemetry stack and applicable operational/privacy requirements before selecting instrumentation.
Reuse an existing logging, metrics and tracing interface rather than introducing a new provider by default.

Agree on the contract:

- Which user-visible success/failure and dependency conditions operators need to observe.
- Which structured fields identify the service, environment, route template and bounded result.
- How request/trace identifiers cross service boundaries and reach authorized diagnostic views.
- Which audit events need durable storage, access controls and retention independently of operational logs.
- Which sensitive fields must be omitted, masked or access-restricted.

Avoid putting user identifiers, raw URLs, request IDs or other unbounded values into metric or stream labels.
Validate inbound correlation headers for the stack's format and size; generate a trusted identifier when necessary.
Do not log raw authorization headers, secrets, request bodies or prompts by default.
Return a useful public error and correlation reference without exposing internal details.

## Dashboard decisions

Organize the initial view around user impact: traffic, latency, errors and relevant saturation.
Use resource and dependency panels to investigate those symptoms rather than treating utilization alone as user impact.
For each panel, specify the operator question, query, unit, aggregation/window, useful bounded breakdown and next diagnostic check.
Compare against a healthy baseline at comparable traffic and annotate deployments or relevant configuration changes when supported.

- Show latency distributions or suitable tail percentiles with request volume; separate successful and failed requests and state whether timeouts are included.
  Fast failures and excluded requests can make latency improve during an outage.
- Show error rates with their denominators and distinguish relevant outcomes, including intentional rejection; inspect contract-breaking client errors where appropriate.
- Select saturation evidence for the actual runtime: pool wait/hold duration, queue depth/oldest age, dependency duration, CPU throttling, event-loop delay or memory after collection as applicable.
  Preserve bounded route, instance, process or version views when aggregation could hide a failing subset.
- Treat missing telemetry and absent traffic explicitly rather than rendering no data as healthy zero.
  Use an independent availability observation when application metrics cannot show requests failing before they reach the service.

## Alert decisions

For each alert, record the user impact or justified capacity/availability risk, owner, severity, response, runbook and authorized notification destination.
Define the query, unit, evaluation window, persistence and recovery conditions, minimum traffic or sample policy, and missing-data behavior.
Choose thresholds from the service objective, measured baseline and response lead time; illustrative CPU percentages or latency values are not universal thresholds.
At low volume, choose a meaningful failure-count, synthetic-availability or longer-window policy rather than silently suppressing a complete outage.

Prefer user-impact signals for urgent paging; a resource or capacity alert needs a documented failure risk and an action the recipient can take.
Keep diagnostic-only signals on dashboards or lower-urgency routes when immediate intervention is unnecessary.
Check grouping and repeat behavior so one dependency failure does not generate an unbounded notification stream.
Where an existing service objective and error-budget policy exists, reuse it rather than introducing a competing threshold convention.

## Verify the observation path

Implement the agreed contract in small changes with controlled synthetic requests.
Verify the actual emitted records and metric series, ingestion, dashboard query and alert behavior.
A local log line alone does not establish that the operational dashboard receives it.
Exercise healthy traffic, sustained failure, a transient spike, low traffic, missing data and recovery against the specified policy using synthetic series or the stack's rule evaluator.
Check that the intended condition fires after its configured persistence and resolves after recovery, while excluded conditions do not fire.
Verify grouping and destination selection without sending real notifications unless authorized; distinguish rule evaluation, routing and actual delivery evidence.
Use isolated alert routing for tests; notification delivery requires authority to contact its recipients.

Document how an operator follows a synthetic failure from the returned reference to the relevant diagnostic record, and state unverified deployment effects.
Instrumentation preparation does not authorize deploying it or changing production retention and access settings.

Example: “Add request correlation and a dashboard query for failed draft saves.”
Define the route/result fields, emit a synthetic error and prove the query finds it without recording draft content.

Example: “Create a dashboard and alert for failed checkout requests.”
Define eligible requests and failures, show success/failure latency and volume, and pair impact with dependency and pool-wait panels.
Use synthetic request counts to verify the failure rate, persistence, low-volume and no-data policies, then prove the alert fires and resolves through isolated routing.
Report unverified ingestion or real notification delivery explicitly.

Background reading: [Server monitoring analysis guide](https://kciter.so/posts/server-monitoring-analysis-guide/).
Use its patterns to form testable hypotheses; verify them against the service rather than adopting example thresholds as policy.
