# Pattern Selection

Use this reference when deciding whether a design pattern improves the current task.

## Primary Goal

Move from problem pressure to a concrete pattern decision instead of stopping at vague principles.

## Selection Workflow

Follow this sequence:
1. identify the real pressure in the changed code
2. classify it as creation, structure, behavior, orchestration, domain, cross-cutting, or migration pressure
3. shortlist one to three pattern candidates
4. choose one pattern, one small combination, or no named pattern
5. add a short language note describing the idiomatic shape in the current language
6. explain why the rejected alternatives are weaker fits

Use `classic-gof-patterns.md` for the 23 GoF patterns, `modern-patterns.md` for current architecture, integration, and application patterns, and `language-mapping.md` for language-specific expression notes.

## Step 1: Confirm The Pressure

Start from the code shape, not from pattern names.

Typical pressure signals:
- repeated `if/else` or `switch` growth
- complicated or environment-dependent object construction
- external SDKs or transport contracts leaking inward
- orchestration mixed with business rules
- cross-cutting concerns copied into many code paths
- shared legacy logic that needs a safe seam
- business invariants scattered across primitive values or handlers

## Step 2: Shortlist Candidates By Pressure

### Creation Pressure

Signals:
- object construction varies by provider, tenant, runtime, or environment
- construction has many optional steps or invalid combinations

Start with:
- classic: `Factory Method`, `Abstract Factory`, `Builder`, `Prototype`
- modern: `Dependency Injection`, `Composition Root`

### Structure And Boundary Pressure

Signals:
- external contracts mismatch your internal model
- callers repeat subsystem choreography
- module boundaries are leaking framework or SDK detail

Start with:
- classic: `Adapter`, `Facade`, `Bridge`, `Proxy`, `Composite`
- modern: `Ports and Adapters`, `Anti-Corruption Layer`, `Vertical Slice`, `Module by Capability`

### Behavior And Variation Pressure

Signals:
- behavior changes by rule, state, provider, or mode
- new variants keep extending a conditional tree

Start with:
- classic: `Strategy`, `State`, `Template Method`, `Command`, `Chain of Responsibility`
- modern: `Specification`, `Policy Object`, `Plugin Registry`

### Orchestration And Workflow Pressure

Signals:
- handlers or services coordinate many steps and dependencies
- actions need queueing, retries, compensation, or explicit sequencing

Start with:
- classic: `Command`, `Mediator`, `Observer`
- modern: `Application Service`, `CQRS`, `Saga`, `Outbox`, `Pipeline or Middleware`

### Domain Pressure

Signals:
- business rules are duplicated in handlers, DTOs, or persistence code
- invariants and consistency boundaries are unclear

Start with:
- classic: `Strategy`, `State`, `Visitor` only if object-structure variation is real
- modern: `Value Object`, `Aggregate`, `Domain Event`, `Specification`, `Idempotency Boundary`

Read `domain-modeling-patterns.md` when domain pressure is the real problem.

### Cross-Cutting Pressure

Signals:
- logging, authorization, metrics, retries, caching, or enrichment keep getting copied

Start with:
- classic: `Decorator`, `Proxy`
- modern: `Pipeline or Middleware`

### Migration And Legacy Pressure

Signals:
- the better shape is clear but direct rewrite is too risky
- old and new paths must coexist for a while

Start with:
- classic: `Adapter`, `Facade`
- modern: `Strangler Fig`, `Anti-Corruption Layer`, `Outbox`, `Saga`

Also read `legacy-migration-playbook.md`.

## Step 3: Choose One Pattern Or None

Prefer the lightest option that solves the active pressure.

Choose no named pattern when:
- one small function or extracted module removes the pressure cleanly
- the variation is still too small to justify a named seam
- the repo's existing style strongly prefers a simpler local construct
- a hotfix only needs a narrow guard plus a regression test

Small combinations are acceptable when they address different concerns. Examples:
- `Strategy` plus `Factory Method`
- `Adapter` plus `Ports and Adapters`
- `Application Service` plus `Specification`
- `Decorator` plus `Pipeline or Middleware`

Avoid stacking multiple patterns that solve the same problem.

## Confusion Pairs

Check these before finalizing:

### Strategy Vs State Vs Template Method

- choose `Strategy` when algorithms or policies vary independently
- choose `State` when behavior changes because the object's lifecycle state changes
- choose `Template Method` only when the workflow skeleton is stable and inheritance is already natural in the codebase

### Adapter Vs Facade Vs Anti-Corruption Layer

- choose `Adapter` for one contract mismatch
- choose `Facade` for a simpler front door over a noisy subsystem
- choose `Anti-Corruption Layer` when an external model would otherwise contaminate your core domain language

### Decorator Vs Proxy Vs Pipeline

- choose `Decorator` for composable behavior around a stable core action
- choose `Proxy` when access control, lazy loading, or indirection is the point
- choose `Pipeline or Middleware` when requests or messages pass through ordered processing stages

### Factory Method Vs Abstract Factory Vs Builder Vs Dependency Injection

- choose `Factory Method` for one varying product creation path
- choose `Abstract Factory` when several related products vary together
- choose `Builder` when staged assembly and readability are the real problem
- choose `Dependency Injection` when object wiring should move out of business code entirely

### Observer Vs Domain Event Vs Saga

- choose `Observer` for in-process decoupled listeners
- choose `Domain Event` for a meaningful business fact that other parts of the system react to
- choose `Saga` when a long-running cross-boundary workflow needs coordination or compensation

## Required Output

When the pattern decision is important, say it explicitly:
- `Pressure:` what structural problem is active
- `Pattern candidates:` one to three candidates
- `Chosen pattern:` one pattern, one small combination, or `No named pattern`
- `Why chosen:` why it fits the current repo and change budget
- `Language note:` how the same pattern should look idiomatically in the current language
- `Why not others:` why the rejected candidates were weaker fits

## When Not To Use A Pattern

Do not introduce a pattern when:
- the code has one stable path and low expected variation
- a small function can express the idea clearly
- the abstraction would be larger than the duplication it removes
- the "future extension" is hypothetical rather than plausible
- the codebase's existing style would make the new abstraction inconsistent or harder to read
