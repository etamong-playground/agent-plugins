---
name: bump-selfhosted-app
description: Prepare and, when explicitly authorized, roll out a self-hosted application upgrade with verified artifacts, data compatibility and rollback.
---

# Upgrade a self-hosted application

Separate preparation from operational execution.
A request to prepare an upgrade does not authorize production changes.

## Prepare

Read the running version and configured target, then find every related pin across server, datastore, worker, sidecar and host configuration.
Read the entire official release gap for migrations, removed configuration, authentication, platform requirements, metric changes and component compatibility.
Verify the resolved image digest, package or commit, including any carried patches.

Trace what a merge, scheduled updater or GitOps reconciler will actually change and when.
State the required order from the vendor's compatibility rules; never assume workers always upgrade first.
Identify data transitions that prevent downgrade and the actual backup/restore requirements.
A lower version pin is not a rollback plan for a one-way migration.

Produce a scoped change, validation evidence, rollout sequence, expected interruption, abort conditions and rollback procedure.
Verify backup availability and a suitable restore check before a stateful rollout.
Keep unrelated upgrades out of the change.

## Execute only with rollout authority

Confirm the approved target, data changes, interruption and automation controls.
Use the established deployment mechanism, including any approved pause/resume of reconcilers.
Do not disable automation merely to bypass an approval gate.
Capture a suitable pre-change backup for the approved stateful transition, then deploy in the verified order.
Observe migration completion, serving version, dependent components and a representative user operation.
Recheck desired versus running configuration and restore approved automation controls.

Stop at an unmet gate or abort condition and report the observed state; do not claim a completed rollback without verifying restored service and data.

Example: “Prepare the service upgrade PR and migration runbook, but do not deploy.”
Deliver the configuration, release-gap analysis and restore requirements without changing running services.
