# Architecture Patterns

Use this reference when the task touches more than one module, integration boundary, or application layer.

## Layering Model

For most business applications, prefer this split:
- Interface layer: controllers, routes, resolvers, CLI handlers, UI actions
- Application layer: use-cases, orchestration, transactions, policy sequencing
- Domain layer: core business concepts and rules
- Infrastructure layer: databases, queues, external APIs, filesystems, framework adapters

Guideline:
- outer layers may depend inward
- inner layers should not depend on outer implementation details

## Ports And Adapters

Use when external systems change more often than business rules.

Apply it by:
- defining the business-facing capability in core code
- implementing the capability with adapters at the edge
- keeping SDK- or transport-specific contracts out of the domain model

Best for:
- payment providers
- messaging providers
- file storage backends
- search engines
- third-party APIs

## Application Service / Use-Case Pattern

Use when transport handlers are becoming orchestration centers.

Responsibilities:
- coordinate dependencies
- manage workflow order
- handle transactions or unit-of-work boundaries
- call domain logic
- trigger side effects through ports

Avoid putting raw framework concerns or domain policy in the same place.

## Repository Pattern

Use when business code needs collection-like access to aggregates or meaningful persistence operations.

Good repository signs:
- method names reflect domain meaning
- callers do not care which database or ORM is behind the boundary
- business logic is simpler because persistence concerns are out of the way

Bad repository signs:
- it only mirrors CRUD mechanically
- query details still leak everywhere
- it adds no semantic boundary

## Module By Capability

When a system grows, consider grouping by business capability rather than technical type.

Example direction:
- billing/
- orders/
- customer-notifications/

Inside each capability, apply local layering only as needed.

This often preserves cohesion better than one global `controllers/`, `services/`, and `repositories/` tree.

## Extension Point Design

When future variants are likely, design the extension point where variation originates.

Examples:
- payment method variation starts near payment policy, not near UI rendering
- export format variation starts near document rendering, not in route handlers
- provider variation starts near the integration port, not deep inside domain logic

Keep extension points narrow and explicit.

## Boundary Questions

Before finalizing architecture, ask:
- Which part of this change is stable business policy?
- Which part is transport or infrastructure noise?
- Where will the next variant most likely appear?
- What should callers know, and what should remain hidden?
- If the external dependency changes, which modules should stay untouched?
