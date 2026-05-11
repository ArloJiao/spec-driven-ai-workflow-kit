# Non-Functional Guardrails

Use this reference when a design change touches performance-sensitive, concurrent, security-sensitive, or operationally important code.

## Primary Goal

Improve structure without silently harming latency, throughput, safety, observability, or rollout reliability.

## Performance And Scalability

Check:
- Will the new abstraction add extra database queries, network calls, serialization, or allocations?
- Does moving logic introduce new loops, fan-out, or repeated lookups?
- Is this code on a hot path, batch path, or user-facing latency path?

Prefer:
- localized abstractions with predictable cost
- explicit caching, batching, or memoization only when the current system already needs it
- preserving proven fast paths while improving boundaries around them

Avoid:
- elegant layering that multiplies round trips
- generic abstractions that hide expensive work

## Concurrency, Ordering, And Retry Semantics

Check:
- Can this workflow run concurrently?
- Are locks, transactions, retries, or queues involved?
- Does the system depend on ordering, idempotency, or exactly-once assumptions?

Prefer:
- explicit idempotency boundaries
- clear ownership of transaction or lock scope
- preserving existing ordering semantics unless the user approves a change

Avoid:
- splitting one coherent operation across modules in a way that breaks atomicity
- moving retry logic without preserving safety guarantees

## Observability

Check:
- Will failures still be diagnosable after the refactor?
- Do logs, metrics, and traces still appear at the right boundaries?
- Will operators understand where the new seam begins and ends?

Prefer:
- keeping instrumentation near important boundaries
- preserving correlation IDs, request context, and error reporting paths
- adding observability when a new seam makes failures less obvious

## Security And Data Boundaries

Check:
- Does the change alter auth, authorization, secret handling, or trust boundaries?
- Are PII, financial data, or sensitive payloads now flowing through new modules?
- Does an adapter or facade hide a security-sensitive contract?

Prefer:
- explicit validation and auth checks at boundary layers
- minimizing the spread of sensitive data through new abstractions
- preserving audit-relevant behavior

Avoid:
- moving security decisions into utility layers where they become invisible
- simplifying structure by broadening data access

## Operability And Rollout

Check:
- Can this change be rolled back easily?
- Does it need a feature flag, phased rollout, or compatibility shim?
- Will on-call engineers understand the new behavior path?

Prefer:
- reversible seams
- narrow rollouts for risky structure changes
- clear operational ownership for new extension points

## Decision Rule

If the cleanest design increases non-functional risk, prefer the safest maintainable step, then propose the cleaner next step separately.

## Common Trap

Do not assume that a cleaner call graph is automatically safer in production. In real systems, the safest design is the one that preserves behavior, diagnostics, and operational control while making the next change easier.
