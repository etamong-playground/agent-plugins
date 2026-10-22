---
name: publish-site
description: Publish static reports, HTML artifacts and sites to Pages at pages.onul.me, inspect site access or deployment history, and update an existing site's preview or live version.
---

Use the Pages MCP connection to inspect the account, create private sites and publish supplied files.
The service supports static files through this workflow; container applications require a separate service workflow.

Discover the Pages tools `get_account`, `list_sites`, `create_site`, `list_deploys` and `publish_static`.
Codex uses the Pages connection's native OAuth sign-in flow and stores its offline credentials.
Claude uses the local `pages mcp proxy` adapter and the Pages CLI credential store.
For Claude, run `pages help mcp` and verify that it lists `pages mcp proxy`; install or update the public CLI if the command is missing.
Unset `PAGES_TOKEN` and run `PAGES_URL=https://pages.onul.me pages login` before starting the MCP connection.
The proxy never starts interactive login and rejects PAT credentials; ordinary Pages CLI commands retain PAT support.
Never request a pasted access token, refresh token or PAT in chat.
A revoked or expired refresh grant requires sign-in again.

Inspect the account's upload limits and existing sites before choosing a target.
Use the site the user selected when the account has the necessary role.
If the user requested a new site, choose a descriptive available slug and create it with private visibility unless they explicitly requested public access.
Publishing a production version does not make a private site public.
A private site can still have shared members.
If the user requests owner-only access, verify membership in the dashboard or with `pages members <slug>`; the initial MCP tools do not expose membership details.
Do not claim exclusive access from visibility alone, and change existing memberships only when the user's request authorizes that access change.

Supply artifact content directly to `publish_static` as relative file paths and text or base64 content.
A path on the user's computer is not readable by the remote MCP server.
Include the complete static artifact, preserving relative asset links and an `index.html` entry point for a website.
Use preview mode unless the user asked to replace the live version.
Set `mode: "production"` only for that intent and omit the preview alias.

For example, publish a private preview after creating a site named `research-notes`:

```json
{
  "slug": "research-notes",
  "mode": "preview",
  "alias": "draft",
  "files": [
    {
      "path": "index.html",
      "encoding": "text",
      "content": "<!doctype html><html lang=\"en\"><meta charset=\"utf-8\"><title>Research notes</title><h1>Research notes</h1><p>Verified findings and source links.</p></html>"
    }
  ]
}
```

Return the `site_url` from the successful tool result and state whether it is a preview or production version and whether access is private or public.
Do not construct a production URL when only a preview was published.
If a publish times out or its outcome is uncertain, inspect `list_deploys` before retrying; avoid duplicate publication after a lost response.
A matching ready deployment can establish success even when the publish response was lost.
Use a URL provided by a successful response or deployment record; otherwise report the verified deployment ID and status without inventing a URL.

For a local directory or an artifact beyond the MCP byte/file limits, use the Pages CLI and its OAuth login.
For example, `pages deploy research-notes --dir dist --preview draft` publishes a directory as a preview.
A remote CLI requires a reachable loopback callback, such as an SSH port forward; use `pages login --no-browser --callback-port 43807` and forward that port to the CLI host before approving.
Read the [Pages workflow reference](https://pages.onul.me/skill.md) for installation and detailed CLI usage when needed.
