# TypeScript Node Service Patterns

Use this reference when implementing or refactoring TypeScript or JavaScript backend code, service layers, or integration modules.

## Primary Goal

Keep business intent obvious while preventing framework handlers, SDK clients, and type noise from taking over the design.

## Recommended Shape

For most backend features, separate code into:
- transport or entry layer: route handlers, controllers, resolvers, CLI entrypoints
- application layer: use-cases, orchestration, workflow coordination
- domain layer: policies, rules, business concepts, invariants
- infrastructure layer: database adapters, HTTP clients, queues, files, caches

Do not let Express, NestJS, or framework decorators become the true home of business logic.

## Pattern Guidance

### Strategy

Use when:
- behavior varies by provider, channel, tenant, or rule set
- pricing, eligibility, mapping, or export behavior changes by mode

Prefer:
- a small interface or callable contract
- dependency injection through constructors or explicit parameters
- strategy registration near the application layer, not scattered across route handlers

Avoid:
- giant unions with central `switch` logic when each branch owns meaningful behavior

### Factory And Builder

Use when:
- construction depends on environment, feature flags, tenant config, or selected provider
- objects require staged setup or a readable configuration flow

Prefer:
- one narrow factory per concept
- builders only when readability or staged validation clearly improves

Avoid:
- global factory registries for simple one-off creation

### Adapter And Facade

Use when:
- a third-party SDK returns awkward types or nested response shapes
- low-level integration sequences keep leaking into business code

Prefer:
- adapters that translate external contracts into internal types
- facades for multi-step SDK orchestration
- keeping retry, timeout, and mapping logic near the edge

Avoid:
- directly returning raw SDK objects from domain-facing services

## Module Boundary Rules

Favor feature-based grouping when the codebase is growing:
- `billing/`
- `orders/`
- `notifications/`

Inside each feature, keep local layering light and explicit.

Avoid a flat global structure where every domain concept is split across distant `controllers/`, `services/`, `repositories/`, and `utils/` folders unless the codebase already relies on that convention effectively.

## Type Design Rules

Prefer:
- explicit domain types for meaningful concepts
- `type` or `interface` names that reflect business language
- narrow DTOs at the transport boundary
- transformation between external DTOs and internal models at the edges

Avoid:
- passing unvalidated request objects deep into application services
- using `any`, sprawling optional property bags, or config objects as hidden logic containers
- shared catch-all `types.ts` files for unrelated concepts

## Common Refactor Moves

If a route handler grows too much:
- keep parsing and auth in the entry layer
- move orchestration into an application service
- move policy into domain helpers, value objects, or strategies

If a service becomes a branch hub:
- extract one collaborator per varying behavior
- replace `switch` chains with strategy lookup where growth is likely

If SDK calls spread across the codebase:
- wrap them in one adapter or facade
- return internal models instead of raw response shapes

## Testing Implications

Aim for:
- route tests that verify transport behavior only
- application service tests that cover orchestration
- focused domain tests for policy-heavy code
- adapter tests for external contract translation

If every test needs the framework bootstrapped, the boundaries are probably too blurred.
