# Java Spring Modularity

Use this reference when implementing or refactoring Java or Spring applications with controllers, services, repositories, transactions, and integration-heavy business flows.

## Primary Goal

Keep Spring as the delivery mechanism, not the definition of your architecture. Business policy should stay readable even if annotations, repositories, and integrations change.

## Recommended Shape

For most Spring applications, organize around:
- entry layer: controllers, message listeners, scheduled jobs
- application layer: use-case services, orchestration, transactional workflows
- domain layer: business rules, entities, value objects, policy services
- infrastructure layer: JPA repositories, HTTP clients, Kafka producers, storage adapters

Where practical, prefer packaging by business capability first and technical role second.

## Pattern Guidance

### Strategy

Use when:
- pricing, approval, fulfillment, notification, or mapping rules vary by channel, product, partner, or state
- service classes gain branching behavior for every variant

Prefer:
- a narrow interface with explicit implementations
- selection at the application layer
- constructor injection of collaborators

Avoid:
- huge enum-driven `switch` statements inside one service when behavior is expected to grow

### Factory And Builder

Use when:
- aggregate creation depends on context or staged validation
- a workflow assembles multiple related objects with constraints

Prefer:
- factories for domain-valid creation
- builders where object assembly is genuinely complex and readability benefits

Avoid:
- builders generated for every DTO without a design reason

### Facade And Adapter

Use when:
- external systems or internal subsystems require repeated orchestration
- service methods are cluttered with mapping, retry, and transport details

Prefer:
- adapters that hide external contracts
- facades that present one workflow-oriented entry point

Avoid:
- exposing Feign, RestTemplate, WebClient, or raw entity manager details to business policy code

## Spring-Specific Rules

Controllers should:
- parse requests
- delegate quickly
- return transport responses

Application services should:
- coordinate workflow steps
- define transaction boundaries when needed
- call domain logic and ports

Domain code should:
- express invariants and business decisions
- avoid Spring-specific annotations unless there is a strong local convention that justifies it

Repositories should:
- expose domain-meaningful access patterns
- avoid leaking query mechanics into upper layers

## Common Refactor Moves

If a `@Service` class becomes too broad:
- split orchestration from policy
- move rules into domain services or strategy implementations
- isolate integration calls behind ports or adapters

If transactions spread unpredictably:
- consolidate workflow ownership in one application service
- keep nested transactional logic explicit and minimal

If packages are purely technical and the feature is hard to trace:
- group related controller, use-case, domain, and infrastructure code by capability

## Review Questions

Check:
- would a new variant require editing one crowded service or adding one focused collaborator?
- are transaction boundaries obvious?
- is domain logic hidden inside repository queries or controller methods?
- do annotations clarify behavior, or are they masking poor structure?
- can the important policy be tested without spinning up the whole container?
