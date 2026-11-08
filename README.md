# Onul Services

Service connections and workflows for Codex and Claude Code.
Plugins are public; service plugins require their own sign-in and account permissions.
The jskills plugin bundles portable development skills and requires no service connection.
Pages publishes static sites and reports, with private previews as the default workflow.

## Codex

```sh
codex plugin marketplace add etamong-playground/agent-plugins
codex plugin add pages@onul-services
```

Complete the Pages connection's OAuth sign-in when prompted by Codex.
The native connection requests Pages read/write access and `offline_access` for refresh credentials.
A revoked or expired refresh grant requires sign-in again.

## Claude Code

Install or update the public Pages CLI and verify that it supports the proxy:

```sh
curl -fsSL https://pages.onul.me/install.sh | sh
pages help mcp
unset PAGES_TOKEN
PAGES_URL=https://pages.onul.me pages login
claude plugin marketplace add etamong-playground/agent-plugins
claude plugin install pages@onul-services
```

`pages help mcp` must list `pages mcp proxy`; update the CLI if that command is absent.
Claude invokes this local stdio adapter, which uses the CLI's origin-bound OAuth credential store and locked refresh.
Complete login before starting the connection; the proxy does not launch interactive login and does not accept PATs.
Ordinary Pages CLI commands continue to support PAT automation.
For a remote CLI host, forward its loopback callback port before approving login; see the [Pages CLI workflow](https://pages.onul.me/skill.md).

## Use and update

Ask the agent to publish a private preview of a report, inspect available sites or inspect deployment history.
The shared `publish-site` skill explains supplied-file publishing, private access and preview versus production intent.
Public plugin installation does not grant site membership or make a private site public.

```sh
codex plugin marketplace upgrade onul-services
codex plugin add pages@onul-services
claude plugin marketplace update onul-services
claude plugin update pages@onul-services
```

Restart the client session after an update.

## Maintain the catalog

`catalog.json` defines public service metadata.
Each service keeps one canonical `plugins/<service>/skills/` tree shared by both clients.
Generate client-specific manifests and catalogs with `python3 scripts/generate.py`; use `--check` to detect drift.
Codex's compatibility manifest selects `.mcp.codex.json` explicitly, while Claude uses `.mcp.json`.
Do not add a portable root manifest that would override the native OAuth adapter.
Keep credentials and privileged fleet administration workflows outside these packages.

## Onul Skills

Portable skills for requirements, development, verification, writing, agent workflows, operations and macOS apps.
The [Korean guide](https://pages.onul.me/jskills/) includes worked requests, verification boundaries, category downloads and migration instructions; its header shows the bundled version.
Audio development is an optional category and follows explicit requirements.

Install the full package **or** selected categories, with no overlap:

```sh
codex plugin marketplace add etamong-playground/agent-plugins
codex plugin add onul@onul-services
claude plugin marketplace add etamong-playground/agent-plugins
claude plugin install onul@onul-services
```

For example, replace the full package with `onul-planning@onul-services` and `onul-development@onul-services` to install only those categories.
Other categories are `onul-verification`, `onul-writing`, `onul-agent-tools`, `onul-operations`, `onul-macos` and `onul-audio`.
Claude's full-package planning command is `/onul:planning`; the category command is `/onul-planning:planning`.
Use the discovered skill names in Codex rather than assuming Claude's slash-command syntax applies.

Existing `jskills` users can keep receiving its generated compatibility edition, which retains `feature-planning`.
To switch, remove it first with `codex plugin remove jskills@onul-services` or `claude plugin uninstall jskills@onul-services`, then install `onul` or selected categories and open a fresh session.
Do not install the full, compatibility and category editions together: they contain equivalent workflows under different plugin namespaces.
Changing packages does not remove separately copied standalone skills; inspect those before installing an equivalent package.

`plugins/onul/skills/` is the canonical authored tree.
Category and compatibility folders are generated self-contained distributions, not separate editing locations.
Reviewed origins, modification notices, licenses and resource hashes live in [sources.json](plugins/onul/sources.json).
See [Contributing](CONTRIBUTING.md) for generation, review and qualification.

```sh
python3 -m venv .tmp/venv
.tmp/venv/bin/pip install -r requirements.txt
.tmp/venv/bin/python scripts/build_onul.py --output .tmp/onul-site
```

The build refuses an existing output directory and rejects resource or generated-package drift before creating full, category, compatibility and individual ZIPs.
Skill-only packages configure no MCP server or authentication.

PR titles and bodies are written in English; the repository owner reviews changes.
