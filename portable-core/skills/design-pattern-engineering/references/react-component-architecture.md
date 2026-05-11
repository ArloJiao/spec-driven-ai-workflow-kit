# React Component Architecture

Use this reference when implementing or refactoring React, Next.js, or component-driven frontend features.

## Primary Goal

Preserve readable component boundaries, localize state decisions, and avoid turning UI files into mixed piles of rendering, fetching, business policy, and transformation logic.

## Component Boundary Model

Split concerns deliberately:
- page or feature shell: layout, route-level composition, loading and error boundaries
- container or feature coordinator: data fetching, orchestration, state wiring
- presentational component: rendering-focused logic and interaction callbacks
- hook or service module: reusable stateful logic or integration logic
- domain helper or mapper: policy, formatting, eligibility, transformation rules

Not every feature needs all five layers, but avoid collapsing them blindly into one giant component.

## Pattern Guidance

### Strategy

Use when:
- the UI behavior differs by mode, role, variant, content type, or product configuration
- rendering or action policy keeps growing conditional branches

Prefer:
- variant objects, feature-specific hooks, or strategy maps close to the feature
- one clear seam where variant behavior is selected

Avoid:
- pushing all variants into one JSX tree with nested ternaries and boolean flags

### Facade

Use when:
- multiple hooks or async calls must be coordinated before the UI can act
- components keep repeating loading, caching, retry, and error-handling choreography

Prefer:
- a feature hook or view-model style facade that presents one coherent contract to the component tree

Avoid:
- hiding every tiny hook behind facades; only use them when orchestration noise is real

### Adapter

Use when:
- backend DTOs do not fit UI needs
- CMS, analytics, or search results arrive in awkward structures

Prefer:
- mapping external data into UI-focused view models at the boundary
- keeping JSX free of defensive property digging and fallback chains

## State Placement Rules

Put state:
- as low as possible when it only affects one local interaction
- at the feature boundary when multiple child components must coordinate
- outside the UI tree only when it is shared across routes or is genuinely app-wide

Do not lift state just because it might be needed later.

## Hook Rules

Good custom hooks:
- own one coherent stateful concern
- expose a clear API
- isolate async orchestration or repeated behavior

Bad custom hooks:
- become mini-frameworks with too many flags
- hide business rules, navigation, analytics, and rendering decisions all at once

If a hook starts returning many booleans and handlers, split by responsibility.

## Common Refactor Moves

When a component becomes too large:
- extract pure rendering subcomponents
- move derived data calculation into named helpers
- move async orchestration into a feature hook
- move branching business rules into explicit strategy objects or functions

When prop drilling becomes noisy:
- first reconsider component boundaries
- then consider feature context only if the state is truly shared and stable

When JSX becomes unreadable:
- extract named render steps sparingly
- replace nested ternaries with explicit variant selection before rendering

## Frontend Code Review Questions

Check:
- can a teammate identify where to add a new UI variant?
- is business policy trapped in JSX conditions?
- are API response quirks handled at the boundary?
- is state owned by the smallest responsible scope?
- would adding tests for a new interaction be straightforward?
