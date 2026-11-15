# Worked estimate with synthetic prices

Request: "Compare managed document storage and a fixed-cost database for a small team app, including hourly versus daily reminders. Could a faster runtime reduce the bill?"
These inputs and prices are fictional arithmetic fixtures, not vendor quotes or measured performance.

## Inputs and derivation

Assume 60 daily active people, two visits each day, three database-backed API requests per visit, and 30 days.
That yields 360 API requests/day and 10,800/month, excluding static assets and other endpoints.
At 25 documents per request, reads are 9,000/day; at a 2,000-document full scan, reads are 720,000/day.
Assume a separate 100 document writes/day, including receipts, with no write allowance and a fictional $0.20 per 100,000 writes.

A fictional read price of $0.10 per 100,000 documents with 10,000 free reads/day yields:

- Bounded queries: $0/month for reads, plus $0.006/month for writes.
- Full scans: `(720,000 - 10,000) * 30 / 100,000 * $0.10 = $21.30/month` for reads, plus $0.006 for writes.
- An otherwise equivalent $15/month fixed database crosses this read-only comparison at 510,000 reads/day, or about 1,417 documents/request at 360 requests/day.

These are operation subtotals: add compute, storage, backup and transfer before comparing total bills.
A fixed database also needs evidence that it can handle the same peak workload and required reliability.

## Cadence and retention

One daily scheduler job makes 30 invocations/month; hourly makes 720.
Neither implies 60 messages per invocation: query due, unsent notifications and count actual recipient devices.
A daily digest limit belongs in persistent application state keyed by recipient and local date, not only in a cron expression.
Describe retries and ambiguous send outcomes; a database marker alone cannot promise exactly-once delivery through an external push service.

At 100 mutations/day, retaining one 2 KiB receipt per mutation for 365 days adds 71.29 MiB of payload before metadata and indexes.
At 10,000 mutations/day the same policy adds approximately 6.96 GiB.
Changing retention must preserve the required replay/deduplication contract rather than being treated as a free optimization.

## Boundary checks

- Zero reads costs zero when there is no minimum fee; 10,000 reads/day also costs zero.
- 10,001 reads on one day costs $0.000001 under the fictional fractional pricing model.
- 300,000 reads spread evenly across 30 days cost zero; all on one day cost $0.29.
- Halving 20 ms of CPU work within a request containing 180 ms of external wait changes 200 ms to 190 ms, before billing granularity; it does not halve the request bill.

A completed answer identifies the full scan as a cost driver, preserves the distinction between checks and sends, reports the synthetic calculation separately from current vendor prices, and asks for duration profiles before recommending a runtime rewrite.
