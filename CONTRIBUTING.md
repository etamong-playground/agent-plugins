# Contribute a skill

This repository contains everything needed to maintain its public plugins.
Use Python 3.12 and Node.js 22 for the same environment as CI.
Install Python requirements in a virtual environment and use the client versions pinned in `.github/workflows/ci.yml` when running client smoke checks.

## Edit the shared package

For Onul workflows, edit only `plugins/onul/skills/<name>/`; service plugins keep their own canonical skills.
`catalog.json` assigns each Onul skill to exactly one category.
Run the generator to materialize category and compatibility packages; never edit those generated folders.
Both clients use that folder; do not add provider-specific copies.
Keep `name` in the frontmatter equal to its directory name and make the description state when to use the skill.
Preserve supporting documents, scripts, licenses and notices when importing an original skill.
Mark an adapted workflow as an edition in `sources.json` rather than claiming it is an unchanged original.
Use a public, verified origin and immutable revision for third-party imports.
Do not add unpublished source locations or dependencies on an author's machine.

Write for a reader who knows the requested task but none of the author's projects.
Include a worked request and completion evidence, specify verification limits, and keep operational authority separate from preparation.
Remove credentials, personal context, private endpoints, incident details and organization-specific access recipes.
A text-pattern scan supports review but does not establish that a workflow is safe or portable.

## Update metadata and verify

After reviewing changes, update each edited skill's file hashes in `plugins/onul/sources.json`.
For a new skill, add an entry to `skills` there with `name`, `origin`, `license`, and a `sha256` object mapping every resource's relative path to its SHA-256 digest.
Use an existing applicable origin or add a verified public origin under `origins`; add `modifications` for an adapted edition.
For example, a new standalone edition using the package's workflow license has this shape (replace the digest with the reviewed file's actual SHA-256):

```json
{
  "name": "example-workflow",
  "origin": "portable-editions",
  "license": "LICENSE.jskills",
  "sha256": {"SKILL.md": "<reviewed SHA-256 digest>"},
  "modifications": "Standalone workflow adapted for general project use."
}
```

Hash every supporting file, not only `SKILL.md`, and retain its license mapping.
Update `catalog.json` when publishing a new package version, then regenerate metadata.
Review hash changes against the diff; do not use a hash refresh to accept an unreviewed import.

```sh
python3 scripts/generate.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -p '*_test.py' -v
python3 scripts/build_onul.py --output .tmp/review-site
python3 scripts/client_smoke.py
```

Use a fresh build output directory.
The build checks full file inventories and licenses before producing the complete ZIP and individual archives.
Open the generated guide in a browser when changing guide content, diagrams or navigation.
Exercise new skills with a realistic request; inspect their proposed actions for assumptions and authority expansion.
Use synthetic data and do not execute production operations just to test an instruction file.

Open a draft PR with the task, approach and validation that a reviewer needs.
CI runs from this repository alone and requires no private service access for jskills.
Publishing a guide is separate from merging its source and follows the hosting service's deployment controls.
