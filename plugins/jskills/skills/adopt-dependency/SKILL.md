---
name: adopt-dependency
description: Upgrade an existing project dependency, verify the resolved artifact and release gap, update locks and validate affected behavior.
---

# Adopt a dependency

Use this for an existing dependency version change; an adoption comparison is a separate decision.

1. Identify the current pin, requested target and package manager from the repository.
   Verify that the target is published using its official registry or release source.
   If it is not published, report that fact; monitoring needs a supported wait mechanism and the user's requested duration.
2. Read every release between current and target, not only the final release note.
   Record applicable API, configuration, platform and migration changes.
   Separate the version upgrade from optional use of new features unless they are inseparable.
3. Change the intended pin and regenerate its lock with the repository's package manager.
   Review the lock diff for unrelated upgrades and install dependencies before validation.
4. Verify the resolved artifact: lock entry, integrity or digest, and commit for a Git dependency.
   A package's internal version may lag its tag; compare the resolved commit to the tag and inspect the required export or installed file.
5. Run the affected tests, type checks and build; exercise a representative use of the upgraded API.
   Commit pins and locks together, and update examples affected by changed behavior.
6. Deliver through the repository's authorized workflow.
   A package upgrade request does not grant deployment, migration, merge or new credential authority.

For example, for an npm dependency update, regenerate `package-lock.json`, use `npm ci`, run the project's actual checks, then inspect the resolved package entry.
Do not disable dependency provenance, integrity or release-age checks to make installation pass.
Report the resolved target, validation and any remaining migration or rollout gate.
