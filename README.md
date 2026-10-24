# Onul Services

Service connections and workflows for Codex and Claude Code.
Plugins are public; each service requires its own sign-in and account permissions.
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

## Scheduler

Scheduler uses phone device approval through its local CLI on macOS or Linux.
Install the CLI into a directory already on the executor's `PATH`, then complete approval before starting the MCP connection:

```sh
export PATH="$HOME/.local/bin:$PATH"
curl -fsSL https://scheduler-api.onul.me/install.sh | sh
scheduler login
codex plugin add scheduler@onul-services
claude plugin install scheduler@onul-services
```

Start the client with the same `PATH` so its executor can find `scheduler`; configure that path in the executor environment when the client runs on another host.
Both clients use the ordinary `scheduler mcp` stdio adapter.
The package advertises read access to the caller's account, active organizations, and personal schedules.
An existing service account and current membership are required.
Refresh does not extend the original seven-day device authorization; use `scheduler whoami` to inspect its deadline and reconnect after a replacement login.
The proxy never launches a login itself.

Catalog entries may select a `codexAdapter` for device-only stdio connections; these declare a local executor and do not configure native authorization-code OAuth.
A local adapter can omit `originEnv` when its CLI pins the service's canonical resource.
