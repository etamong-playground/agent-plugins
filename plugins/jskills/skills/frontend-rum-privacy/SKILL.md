---
name: frontend-rum-privacy
description: Audit frontend monitoring and session replay for displayed secrets and personal data, then propose environment-specific controls.
---

# Review frontend monitoring privacy

Identify the installed monitoring SDK and version, environments and actual recording configuration.
Check current official documentation and the installed API before naming configuration keys, defaults or sampling units.
Do not transfer one vendor's masking attributes to another vendor.

Trace data to every recorded surface:

- Inputs and ordinary rendered text, especially one-time credential reveals and clipboard-adjacent values.
- URLs, query parameters, console output, network/error telemetry and custom event attributes.
- Log viewers, response dumps, account identifiers and user-supplied content.

For each finding, cite the rendering or emission path and the recording configuration.
Input masking alone does not establish that displayed secrets are protected.
Inspect replay data separately from ordinary event filtering; prove what each configured control affects.

Propose the exact control per environment, the remaining visible data, recording and retention limits, and how to verify the result.
Privacy posture is a user decision: present the proposal before applying it unless the user already approved that exact posture.
A sampling change must not silently expand sensitive-data capture.

Validate only with synthetic, non-sensitive values and an explicitly authorized test destination.
Inspect actual captured events and replay output; a masked screenshot alone does not prove network payloads are safe.
Never trigger real secret reveals or upload production replay content to demonstrate a finding.

Example: “Audit replay around the API credential reveal screen and propose controls; do not change recording settings.”
Deliver a path-based finding, a vendor-version-verified proposal and a synthetic verification plan.
