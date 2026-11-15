---
name: estimate-service-costs
description: Estimate application hosting costs from code, traffic, data growth and reliability requirements; compare managed, serverless and self-hosted options with reproducible assumptions and sensitivity analysis.
---

# Estimate service costs

Produce a decision the reader can audit: which option fits, what changes its cost, and which unknowns could reverse the recommendation.
An estimate does not authorize provisioning, migration, load testing, purchases or a language rewrite.

## Establish the workload

For an existing application, identify the serving implementation and deployment revision before using repository descriptions; distinguish legacy code, deployment configuration and verified live state.
Trace representative reads, mutations, authentication, static delivery, background jobs, subscriptions and notifications.
Record requests per user action, database operations per request, payload sizes, full scans, caches, retries, retention and replicated copies.
Prefer authorized aggregate metrics over personal records; code establishes behavior, not actual traffic, latency or memory usage.
Label each input as measured, configured, supplied or assumed, with its source and date.

Translate human usage into billing units rather than treating users, page views, HTTP requests and database reads as interchangeable.
Include machine-originated traffic: probes, calendar polling, scheduled jobs, retries and per-device notification fan-out.
Separate a scheduler invocation from work found and notifications sent; an hourly check need not imply hourly messages to every user.
Use low, expected and high scenarios when observations are missing, and keep independent traffic and data-size controls.

## Compare equivalent service requirements

State required availability, outage domains, acceptable data loss, recovery time and operational ownership.
Do not compare a tiny single database with a redundant cluster as though their guarantees match.
Include the current implementation as the baseline and distinguish unchanged behavior from proposed optimization.
For self-hosting, separate marginal cash cost from hardware replacement, electricity, backups and maintenance effort; existing hardware is not automatically free capacity.
For a proposed runtime rewrite, separate CPU work from external waits and minimum billing granularity; measure before claiming a speedup, savings or lower memory tier.

## Verify the rate card

Use current primary pricing sources, recording currency, region, edition, billing mode, retrieval date and commitment term.
A region in a dropdown does not establish the displayed price is for that region; verify the selection or label a reference-region estimate explicitly.
Keep vendor rates in the task's estimate, not in this reusable skill.
Identify billing units, rounding/minimums, tier boundaries, free allowance reset periods and sharing scope.
Do not turn a daily allowance into a monthly allowance without an explicit traffic distribution, or reuse an account-wide allowance independently for every service.

Account for applicable compute, memory, storage/indexes, reads/writes, replication, backups/PITR, internet and inter-region transfer, load balancers, queues, scheduler, logs, images and build costs.
A CDN does not automatically eliminate origin egress charges.
Keep omitted, unknown and genuinely zero costs distinct; subtotals must not look like total bills.

## Calculate and check

Use executable arithmetic or a spreadsheet with explicit units and formulas.
For reset-period allowances, calculate `sum(max(0, usage_in_period - allowance) * unit_price)` over the actual periods and apply the provider's tier/rounding rules.
Storage follows billable byte-time, indexes, retention and replicas rather than a raw JSON file size alone.
Serverless compute follows billed instance time: concurrent requests share an instance, while startup, idle minimums and external waits depend on the selected billing mode.
Do not multiply request duration by request count as an exact model unless the concurrency assumptions support it.
Check peak throughput and memory feasibility separately from monthly cost; a cheap configuration unable to serve the workload is not a candidate at that price.

Vary traffic, data retained, records touched, payload size, duration and job cadence independently where they matter.
Show break-even thresholds only for comparable service levels and include one-time migration cost separately.
Check zero usage, allowance boundaries, a bursty period, and at least one independently calculated scenario.
For model checks and a synthetic worked request, read [Worked estimate](references/worked-estimate.md).

## Deliver for the reader

Lead with the recommendation and conditions that would change it.
Provide assumptions, cost components, scenario tables, provenance and the next measurement needed; distinguish a planning budget from a forecast, quote or spending cap.
For non-software readers, derive traffic from people and actions, explain each billing term, and use labeled charts with visible units and assumptions.
Interactive outputs should expose model inputs and rate provenance, support changing assumptions, and distinguish calculated values from observed facts.
Do not publish customer identifiers, credentials, private source paths or personal usage records in a reusable example or public artifact.
Deployment of a report and access changes follow the user's separate authorization, including any required security review.

Completion evidence: identified implementation, sourced rate card, reproducible calculations, sensitivity results, feasibility and reliability limits, and a recommendation with unresolved uncertainties.
