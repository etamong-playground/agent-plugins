---
name: console-ux
description: Review or improve admin consoles and tabular report pages, including filters, pagination, status chips, editable values, forms, copy, representative sample data, and screenshot feedback. Use for management-console UI changes, generated HTML reports with tables, or screenshot-based console feedback.
---

# Console and report-page UX

Use the repository's design contract and existing components first.
This sharing edition supplements the target repository's own UI contracts without assuming an organization-specific component system.

## Tables and controls

- Give data columns suitable filters. For known finite values, support inclusion and exclusion through checkbox choices; use free text for open-ended values.
- Paginate long tables, including overview tables.
  Put pagination controls above and below the table; offer page-number jumps when the data source provides stable page numbers.
- When grouping is requested, show collapsible row groups under the selected column with counts; a filter alone does not satisfy grouping.
  Reuse the component library and follow its contribution workflow for a missing shared capability.
- When data loads asynchronously, show loading skeletons that preserve the page structure, including table headers and placeholder rows.
- Put status items requiring user action first and label the required action clearly.
- Show finite states as consistent status chips, using the existing component library.
- Make the row or card the target of its primary navigation action; keep embedded controls independently operable.
- Show an inline graph when a row represents a measured series and the trend helps the comparison.
- Keep the author or committer next to its commit hash, with a useful profile link.
- Prefer visible tabs for a small fixed choice such as daily, weekly, or monthly; use a dropdown for a long list.
- Mark editable values with a recognizable edit affordance.
- Support free-form metadata keys and values; suggested keys should not restrict the domain unless the product contract requires it.

## Forms and inherited values

- When an explicit delete exists, keep empty-input semantics distinct from deletion. Validate the actual value domain.
- Show the source of inherited values.
- Show an entity under each applicable group and indicate shared membership.
- Place related default levels together when users need to compare them.

## Copy and evidence

- Let headings, labels, and structure explain the interface; remove prose that repeats a control's visible behavior.
- Keep labels as noun phrases and necessary helper text brief.
- Write Korean copy through [korean-prose](../korean-prose/SKILL.md), preserving the interface's established language.
- Populate local samples for changed states, including empty data, inherited and overridden values, multiple membership, and limits when relevant.
- Keep screenshot feedback as a checklist and account for every requested item in the result.
- Follow the repository's browser-validation workflow and verify long content at the supported viewport sizes.
- Report the preview or deployed page URL. When the authorized merge deploys the change, verify the serving version before reporting deployment complete.

## Generated report pages

- Show the generation timestamp at the top and bottom of the report.
- Keep a current-status section focused on running and next work; retain completed history only when the report's purpose requires it.
- For developer reports, link to exact file revisions when access and the requested audience permit it.
- Follow the requested publication destination and preserve its audience and access restrictions.
  Publish only through the requested destination and existing authorized workflow.
