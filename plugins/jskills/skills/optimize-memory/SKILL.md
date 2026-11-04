---
name: optimize-memory
description: Diagnose and reduce a program's memory use with controlled profiling and before/after measurements; use for heap growth, high RSS, allocation pressure, leaks, or excessive GPU memory, not agent note cleanup.
---

# Program memory optimization

Preserve required behavior while reducing a measured memory cost.
A large process or a successful restart does not prove a leak.

## Define the measurement

Identify the symptom, workload, environment, and target: peak resident memory, retained heap, allocation rate, container limit, or GPU memory.
Keep these metrics distinct and state their units.
Use an established budget or measure a baseline before proposing a target.
Inspect existing diagnostics before installing a profiler, and follow the runtime's current official profiling guidance.

Use a bounded repeatable workload with controlled inputs and a recorded build and configuration.
Record warm-up, concurrency, duration, and sampling points.
Profile production only with the required access and operational authorization.
Heap snapshots and traces can contain application data; keep them in an appropriate private location.

## Diagnose the mechanism

Collect a baseline and an allocation or retention profile at the relevant code path.
Distinguish live-object growth from bounded caches, allocator retention, mapped files, shared pages, and expected buffers.
Trace a suspected retained object to its owner and lifetime before calling it a leak.
For GPU workloads, distinguish reservations from live allocations and record batch and input shape.
Rank falsifiable explanations and change one relevant variable at a time.
Report uncertainty when evidence cannot distinguish the explanations.

## Change the responsible part

Consider lifetime errors, unbounded collections, duplicate representations, batches, buffers, and unnecessary copies where the profile shows their cost.
Do not lower input limits, accuracy, cache correctness, durability, or supported concurrency without an explicit product decision.
Use the repository's tests and conventions and keep unrelated refactoring out.

## Measure and verify

Repeat the original workload on the original and changed builds under comparable conditions.
Report absolute values and differences, including peak and steady-state values when they answer different questions.
Check latency, throughput, correctness, and failure behavior for regressions.
For a suspected leak, verify the relevant repeated or long-running lifecycle.
Add a suitable regression or bounded memory check when reproducible, without a noisy universal threshold.
Distinguish direct measurements, inferences, and unverified effects.
Keep the optimization only when evidence supports its benefit and required behavior remains intact.
