---
name: repo-ci-baseline
description: Audit whether pull-request CI actually executes meaningful tests and prepare the appropriate enforcement through the repository workflow.
---

# Audit the CI test gate

Inspect repository scripts, workflows, test discovery and live check configuration before proposing changes.
A successful build does not establish that tests ran, and a check with the right name may have skipped its meaningful cases.

1. Map existing test suites to PR jobs and identify trigger/path/condition gaps.
   Read job output to confirm discovered tests executed, including database-dependent cases.
   A source search for a test command is only a discovery aid.
2. Reproduce the intended job with matching runtime and lockfile versions, isolated fixtures and required service dependencies.
   Use commands that exist in the repository and discover its naming convention explicitly.
3. Include a representative failure check: a relevant assertion must fail for an incorrect behavior and pass after restoration.
   Cross-language formats need fixtures or integration checks that cross the actual boundary rather than two independent round trips.
4. Add the smallest appropriate PR test job using supported runner and service capabilities.
   Do not run untrusted PR code on privileged self-hosted runners or expose secrets to fork builds.
   Preserve package integrity and provenance checks; do not disable them preemptively.
5. Verify successful and failing job behavior before proposing a required-check setting.
   Required-check enforcement follows the owner's settings-management process and authority; never edit protection settings merely because workflow changes were requested.
   Confirm the required context exactly matches the emitted check.

Report suites that ran, meaningful skips, required checks and remaining gaps separately.
Do not create an organization-wide gate for a local repository task.

Example: “Our PR is green but database tests are skipped.”
Trace the missing test environment, run the suite against an isolated database, demonstrate a failing assertion, then validate the PR job.
