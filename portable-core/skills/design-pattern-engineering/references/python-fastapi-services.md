# Python FastAPI Service Patterns

Use this reference when implementing or refactoring Python services, FastAPI applications, background jobs, or integration-heavy workflows.

## Primary Goal

Keep route functions thin, isolate side effects, and express business rules in modules that remain readable and testable without booting the whole web stack.

## Recommended Shape

For most service features, separate:
- API layer: FastAPI routes, request parsing, response models, auth wiring
- application layer: use-cases, workflow orchestration, side-effect sequencing
- domain layer: business rules, validation policies, value objects, decisions
- infrastructure layer: database access, external clients, queues, storage, email

FastAPI dependency injection is useful, but it should not become the architecture.

## Pattern Guidance

### Strategy

Use when:
- behavior changes by provider, marketplace, scoring policy, export format, or workflow mode
- route or service modules accumulate mode-based `if` branches

Prefer:
- callables, protocols, or small classes for replaceable behavior
- selecting the strategy in the application layer

Avoid:
- central registries with magic strings if a simple mapping or constructor injection is enough

### Adapter And Facade

Use when:
- external clients have awkward payloads or multi-step calls
- endpoint code is filled with SDK specifics, retries, and response normalization

Prefer:
- one adapter per external capability
- facades for multi-call workflows such as payment capture, search sync, or media processing

Avoid:
- leaking raw client responses past the integration boundary

### Repository Or Port

Use when:
- business code depends directly on ORM sessions, query builders, or storage APIs
- tests for business rules require database setup just to execute simple policy

Prefer:
- domain-meaningful methods
- repositories owned by the use-case or domain need, not the ORM model shape

Avoid:
- repositories that only mirror CRUD without improving boundaries

## FastAPI-Specific Rules

Keep route functions responsible for:
- input parsing
- auth or permission hooks
- calling one application service or use-case
- returning transport responses

Move out of routes:
- policy decisions
- external call choreography
- large transformations
- persistence details

Keep Pydantic models at the boundary unless a domain model truly aligns with them.

## Pythonic Expression Rules

Prefer:
- modules and functions for simple policies
- small classes only when state, invariants, or lifecycle matter
- explicit dataclasses or value objects for meaningful concepts

Avoid:
- giant service modules with mixed concerns
- global utility files for domain behavior
- dict-shaped hidden protocols instead of explicit models

## Common Refactor Moves

If a route grows:
- move the business path into a use-case function or class
- keep route logic focused on HTTP concerns

If a service becomes a mixed bag:
- split orchestration from policy
- isolate external dependencies behind adapters
- name modules after domain concepts, not generic technical roles

If background jobs duplicate API workflows:
- move shared application logic into one use-case
- keep the route and worker as thin entrypoints

## Testing Implications

Aim for:
- route tests for HTTP contracts
- application tests for workflow sequencing
- domain tests for policy logic
- adapter tests for client translation

If policy tests keep needing `TestClient`, the architecture is too route-centric.
