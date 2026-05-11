# Domain Modeling Patterns

Use this reference when service-layer cleanup is not enough and the business model itself needs stronger structure.

## Primary Goal

Model business meaning explicitly so rules, invariants, and consistency boundaries do not stay trapped inside routes, services, DTOs, or stringly typed conditionals.

## Value Object

Use when:
- a concept has business meaning plus validation or formatting rules
- primitives like strings, numbers, or dicts keep leaking domain rules everywhere

Examples:
- Money
- EmailAddress
- OrderId
- DateRange

Good fit:
- invariants become local and reusable
- equality is based on value, not identity

Bad fit:
- the concept has no real behavior or rule beyond being a raw transport field

## Aggregate And Consistency Boundary

Use when:
- multiple entities must change together under one business invariant
- transactional boundaries are unclear or fragile

Good fit:
- one aggregate root protects consistency rules
- callers modify business state through meaningful operations

Bad fit:
- the model is split only to mirror tables without business boundaries

## Policy / Specification

Use when:
- business eligibility, approval, validation, or selection rules are reused in many places
- boolean logic is spreading across handlers and services

Good fit:
- rules become explicit, composable, and testable
- services orchestrate policies instead of re-implementing them

Bad fit:
- the rule is trivial and local to one small function

## Domain Service

Use when:
- important business behavior does not belong naturally on one entity or value object
- multiple aggregates or concepts participate in one decision

Good fit:
- the service expresses domain intent, not infrastructure detail

Bad fit:
- the "domain service" is really just application orchestration or a wrapper around persistence

## Domain Event

Use when:
- one business decision should lead to additional reactions without tight coupling
- downstream actions should depend on a meaningful domain fact, not a low-level code path

Good fit:
- events represent completed business facts
- side effects stay decoupled from the deciding model

Bad fit:
- events are used to hide a simple direct call

## Idempotency And Retry Boundary

Use when:
- workflows may be retried, replayed, or called more than once
- external integrations or async jobs can duplicate requests

Good fit:
- the domain defines what "same action" means
- repeated execution stays safe

Bad fit:
- idempotency is treated only as an infrastructure concern while business duplication remains possible

## Ubiquitous Language Check

Ask:
- are names written in business language or transport jargon?
- do core concepts exist as first-class types or only as comments and conventions?
- do invariants live near the concepts they protect?

## Decision Shortcuts

Choose the lightest useful model:
- repeated primitive validation -> `Value Object`
- unclear transactional ownership -> `Aggregate`
- duplicated rule logic -> `Policy` or `Specification`
- cross-entity business decision -> `Domain Service`
- decoupled reaction to a business fact -> `Domain Event`
- retried or replayed workflow -> `Idempotency Boundary`

## Warning

Do not force full DDD ceremony into every task. The goal is to make business rules more explicit where the code is already suffering from vague models, duplicated logic, or broken invariants.
