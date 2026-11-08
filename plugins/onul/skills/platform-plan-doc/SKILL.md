---
name: platform-plan-doc
description: Write or refresh a standing service plan or design document set with qualified terms, implementation status, architecture diagrams, flow maps, functional specifications, and screen specifications. Use for planning-document and design-document requests, including 기획서, 기능설계서, 화면설계서, and 플로우맵; not for an ADR, task implementation plan, PR body, or work log.
---

# Service plan and design documents

Describe what a service does, what is planned, and what remains undecided from evidence at a named revision.
ADRs retain the decisions and rationale; these documents explain the resulting behavior.

## Repository conventions first

- Read the target repository's document guidance and existing index; update the existing document rather than starting a competing one.
- The repository owns paths, language, terms, status vocabulary, and review process.
  If it has no document location, propose one rather than silently creating a convention.
- Preserve the repository's decision ownership and approval process.
  A design document does not authorize implementation, other-repository edits, issue publication, or merge.
- Follow the repository's established document language; use `korean-prose` for Korean artifacts.
  Section names and status labels below are English defaults, not a language override.

## Evidence and terms

Record the source branch and full commit before drafting.
Read a named remote revision when available; preserve an in-progress branch rather than synchronizing it just to write documentation.
Distinguish merged code from a running deployment, and record the date and scope of any live verification.

- Read routes and imported components for screens, handlers and routers for APIs, enforcing code for state transitions and permissions, and manifests for network paths and controls.
- Copy UI strings verbatim, including register.
  Mark illustrative data and planned wireframes as examples or sketches.
- Before saying where a record is stored, logged, or displayed, trace the code path.
- Define overloaded nouns near the top in a term table with columns for term, actor, object, and system.
  Give each meaning a qualified term, state what bare uses mean, and use qualified terms in headings, table rows, and diagram labels where meanings meet.
- Record code-versus-ADR differences in a dedicated section without choosing which should change.
  A proposed decision stays a proposal until its decision owner accepts it.
- Name an owner only with the source and date of the assignment; a Git author or registry owner is not evidence of assignment.

## Standing plan

Keep existing headings and omit sections with nothing to say.
Cover scope and dated evidence, background and service roles, accepted decisions and their sources, implementation status, architecture, features in build order, execution items by owner and repository, and open decisions with proposals.
Put decisions requiring the user's answer in conversation, while retaining the unresolved proposal in the document.

Use one status-table row per capability, grouped by domain rather than file or team, with one column per owning service:

| Category | Capability | Service A | Service B |
| --- | --- | --- | --- |
| Accounts | Session renewal | Implemented (source link) | Not applicable |
| Accounts | Access review | Planned (decision link) | Undecided (ownership) |

Use the repository's vocabulary, or Implemented, In progress, Planned, Undecided, and Not applicable when none exists.
Every implemented claim points at evidence a reader can open; every planned item names its decision or dependency, and undecided items name their blocker.
State the check date and what was not verified immediately above the table.
Update dates and facts together; do not put undated deployment or PR status into durable prose.

## Design document set

When the request covers a service's design set, maintain an index and the relevant documents together:

- **Index:** document scope, source revision, status vocabulary, term table, and the rule that screen, API, state-flow, and permission changes update the affected document in the same PR.
- **Flow map:** main user journey first, then mechanisms such as login/session, background sync, state transitions, execution failures, request/grant flows, and data ingestion and reads; planned flows remain visibly distinct.
- **Functional specification:** feature table with ID, permission, status, and source ADR; common authentication, permission, error-envelope, and audit contracts; per-feature inputs, validation, processing, results, and exact error codes; planned features and code-versus-ADR differences.
- **Screen specification:** shared layout as an ASCII wireframe in a `text` block, loading/denied/failure/stale/disabled states, route-and-permission table, and per-screen APIs, wireframe, elements, actions with enabling conditions, and empty/error/denied copy.

## Diagrams

For a platform plan, include component flow and network architecture when each has something to explain.
Use Mermaid, state the purpose before each diagram, and explain non-obvious rules after it so the document remains useful without rendering.

- Solid arrows and plain nodes show existing behavior; dashed arrows (`-.->`) and a Planned label show proposals.
  Put the legend, source revision, and check date beside the diagram.
- Component arrows mean a call or a data read/write in that direction.
  Network diagrams identify trust boundaries, namespaces, ingress/gateway, TLS termination, and service-to-service paths with protocol and identity/control labels.
- Group by trust boundary, not by team.
  Draw a control as enforced only when its defining manifests and applicable path support that claim; mark absent or planned controls explicitly.
- Quote node text and edge labels containing `(`, `,`, or `:`.
  For example, `gateway["Gateway (Planned)"]` and `api -. "HTTPS, planned" .-> gateway` keep punctuation from being parsed as diagram syntax.

## Verification and delivery

Run the repository's documentation and link checks, plus a build when generated documentation changes.
Inspect the rendered Markdown and confirm each Mermaid block renders; report a rendering check that could not be performed.
Check the term table against headings and diagram labels, source links against the recorded revision, and proposed versus accepted decisions against their evidence.
Deliver through the repository's normal review workflow with its existing index and work record.
