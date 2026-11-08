---
name: observability-onboarding
description: Define and verify a service observability contract using its existing telemetry stack, with bounded labels, correlation and privacy.
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

Implement the agreed contract in small changes with controlled synthetic requests.
Verify the actual emitted records and metric series, ingestion, dashboard query and alert behavior.
A local log line alone does not establish that the operational dashboard receives it.
Use isolated alert routing for tests; notification delivery requires authority to contact its recipients.

Document how an operator follows a synthetic failure from the returned reference to the relevant diagnostic record, and state unverified deployment effects.
Instrumentation preparation does not authorize deploying it or changing production retention and access settings.

Example: “Add request correlation and a dashboard query for failed draft saves.”
Define the route/result fields, emit a synthetic error and prove the query finds it without recording draft content.
