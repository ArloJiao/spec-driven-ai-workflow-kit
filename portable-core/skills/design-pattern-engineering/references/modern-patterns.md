# Modern Patterns

Use this reference for widely used post-GoF patterns common in current service, web, integration, and domain-heavy systems.

## Primary Goal

Give the agent a practical modern candidate set in addition to the classic 23 patterns.

## How To Use This File

These are not a closed canon. Treat them as common modern choices when the pressure is broader than a local OO refactor.

For each candidate, check:
- what problem it solves
- when it earns its cost
- when it is too heavy for the current task
- which classic patterns it often combines with
- what brief language note should explain its idiomatic expression in the current stack

## Composition And Construction

### Dependency Injection

- Solves: object wiring and dependency selection should stay out of business logic
- Use when: services need replaceable collaborators, test seams, or environment-specific implementations
- Avoid when: it turns simple local code into a container ceremony exercise
- Often combines with: `Factory Method`, `Abstract Factory`, `Strategy`

### Composition Root

- Solves: application object graph should be assembled in one obvious place
- Use when: wiring is scattered across modules, handlers, or framework callbacks
- Avoid when: the app is tiny and one file already provides a clear entry point
- Often combines with: `Dependency Injection`, `Ports and Adapters`

## Boundary And Module Patterns

### Ports and Adapters

- Solves: business logic should depend on stable capabilities, not SDKs, HTTP clients, ORMs, or queues
- Use when: external systems change faster than core business rules
- Avoid when: a repository or adapter seam would be enough for the current scope
- Often combines with: `Adapter`, `Facade`, `Repository`

### Clean or Onion Layering

- Solves: dependency direction should point inward toward policy and domain rules
- Use when: framework and infrastructure concerns are contaminating core logic
- Avoid when: the team will copy the diagram but not the actual dependency discipline
- Often combines with: `Ports and Adapters`, `Application Service`

### Vertical Slice or Module by Capability

- Solves: code grouped by technical layer becomes hard to change per feature
- Use when: one business capability spans route, policy, persistence, and UI concerns repeatedly
- Avoid when: the system is still small enough that a flatter structure is clearer
- Often combines with: `Application Service`, `CQRS`

### Anti-Corruption Layer

- Solves: external models, terminology, or assumptions would pollute your core domain language
- Use when: integrating with legacy systems, vendor APIs, or another bounded context
- Avoid when: a thin adapter is enough and the foreign model is not spreading inward
- Often combines with: `Adapter`, `Facade`, `Strangler Fig`

### Backend for Frontend

- Solves: one frontend or channel needs a tailored backend boundary instead of a generic shared API
- Use when: web, mobile, or partner channels need different response shaping and aggregation
- Avoid when: it only duplicates an API without real channel-specific needs
- Often combines with: `Facade`, `Application Service`

## Workflow And Application Patterns

### Application Service or Use-Case Handler

- Solves: handlers or controllers are absorbing orchestration, policy sequencing, and side effects
- Use when: one business action touches multiple collaborators in a clear workflow
- Avoid when: the action is tiny and an extra layer would only rename a function
- Often combines with: `Strategy`, `Repository`, `Specification`

### CQRS

- Solves: write-side behavior and read-side query optimization want different models
- Use when: command complexity, permissions, invariants, or scaling needs differ sharply from reads
- Avoid when: CRUD is simple and separate models would add busywork
- Often combines with: `Application Service`, `Domain Event`, `Outbox`

### Pipeline or Middleware

- Solves: ordered cross-cutting processing should remain composable and reusable
- Use when: requests, messages, or commands pass through validation, auth, logging, retries, or enrichment stages
- Avoid when: only one or two hard-coded steps exist and a direct function is clearer
- Often combines with: `Decorator`, `Chain of Responsibility`

### Saga or Process Manager

- Solves: long-running workflows span multiple services or resources and may need compensation
- Use when: no single local transaction can enforce the whole workflow
- Avoid when: a local transaction and one service boundary are enough
- Often combines with: `Command`, `Domain Event`, `Outbox`

### Outbox

- Solves: state changes and message publication must remain consistent across process boundaries
- Use when: you must avoid "saved locally but event lost" failures
- Avoid when: no cross-boundary publication exists or eventual consistency is irrelevant
- Often combines with: `Domain Event`, `Saga`, `CQRS`

## Domain And Rule Patterns

### Value Object

- Solves: business meaning and invariants are trapped in primitive values
- Use when: validation, formatting, equality, or safety rules belong to the concept itself
- Avoid when: the value carries no real business behavior
- Often combines with: `Aggregate`, `Specification`

### Aggregate

- Solves: transactional ownership and consistency boundaries are unclear
- Use when: multiple entities must change together under business invariants
- Avoid when: the model is being split only to mirror database tables
- Often combines with: `Repository`, `Domain Event`

### Specification or Policy Object

- Solves: eligibility and business rule logic keeps spreading through handlers and services
- Use when: rules must be explicit, reusable, and testable
- Avoid when: the rule is tiny, local, and unlikely to be reused
- Often combines with: `Strategy`, `Application Service`

### Domain Event

- Solves: other parts of the system need to react to a completed business fact without tight coupling
- Use when: the event represents meaningful domain language, not a technical callback
- Avoid when: a direct call is simpler and the reaction is not truly decoupled
- Often combines with: `Observer`, `Outbox`, `Saga`

### Idempotency Boundary

- Solves: retries or duplicates must not produce repeated business effects
- Use when: external calls, async jobs, or repeated commands can replay the same intent
- Avoid when: duplicate execution is impossible or harmless
- Often combines with: `Command`, `Saga`, `Outbox`

## Evolution And Extensibility Patterns

### Plugin Registry

- Solves: implementations should be added through registration instead of editing core dispatch logic
- Use when: providers, formatters, handlers, or rule packs grow over time
- Avoid when: there are only two fixed variants and no third is likely
- Often combines with: `Strategy`, `Factory Method`

### Strangler Fig

- Solves: an old system must be replaced incrementally instead of by big-bang rewrite
- Use when: new functionality can be routed around or in front of legacy behavior gradually
- Avoid when: the current task is too small to justify routing or coexistence machinery
- Often combines with: `Adapter`, `Anti-Corruption Layer`, `Facade`

### Feature Toggle Guarded Refactor

- Solves: a safer rollout path is needed while a new implementation coexists with an old one
- Use when: rollout risk or user segmentation matters during migration
- Avoid when: the team will not remove the toggle or monitor the split path
- Often combines with: `Strategy`, `Strangler Fig`, `Application Service`

## Practical Warning

Modern patterns become dangerous when they are adopted as architecture branding instead of a response to active pressure.

Always ask:
- does this pattern reduce the current change cost?
- does it fit the repository's actual style?
- can we test it within the current task?
- is a smaller classic pattern or local extraction enough?
