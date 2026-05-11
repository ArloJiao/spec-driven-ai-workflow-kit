# Code Review Checklist

Use this reference after implementation or during a code review.

## Mandatory Safety Gate

Before concluding any substantial refactor:
- confirm the change still fits the user's requested scope
- confirm compatibility-sensitive contracts remain intact unless the user approved a breaking change
- add or update tests for moved, split, or newly abstracted behavior
- create characterization tests first when changing legacy behavior that is not fully understood

## Design Intent

Check:
- Is the core responsibility of each changed module obvious?
- Is the likely change point isolated rather than scattered?
- Was a design pattern used because of real pressure, not habit?
- If no pattern was used, is the simpler design still easy to extend?

## Responsibilities And Boundaries

Check:
- Does each module have one dominant reason to change?
- Are domain rules separated from transport, persistence, and framework details?
- Are orchestration concerns distinct from business policy?
- Are integration details pushed toward the edges?

## Dependency Direction

Check:
- Do higher-level policies avoid depending directly on low-level details?
- Are external SDKs, ORMs, and transport contracts hidden behind adapters or ports when appropriate?
- Does the dependency graph point in a sensible direction?
- Can core logic be exercised without full integration setup?

## Local Fit

Check:
- Does the change fit the repository's existing naming, structure, and dependency style?
- Did the implementation reuse an existing seam before inventing a new one?
- If the local style is inconsistent, was the touched area improved without widening the cleanup too far?

## Readability

Check:
- Do names express intent in business terms?
- Is the happy path easy to follow?
- Are large branches, nested blocks, or noisy setup hiding the main story?
- Would a teammate understand where to add the next variant?

## Extensibility

Check:
- Can a new rule, provider, or state be added without editing many unrelated places?
- Are repeated conditionals replaced with a more local form of variation when justified?
- Are object creation details localized rather than spread across callers?
- Are cross-cutting behaviors layered cleanly instead of copied?

## Simplicity

Check:
- Is any abstraction speculative or ceremonial?
- Are there interfaces with only one implementation and no clear boundary value?
- Could a smaller construct express the same idea more clearly?
- Did the change introduce indirection without reducing complexity?

## Testability

Check:
- Were characterization tests added first when the refactor touched unclear legacy behavior?
- Were focused tests added or updated when responsibilities moved or new variation seams were introduced?
- Can the important policy be tested without excessive mocking or environment setup?
- Are edge integrations isolated enough for focused tests?
- Do seams exist where behavior varies?
- Would adding tests for a new variant be straightforward?

Do not treat this section as optional. If behavior moved, the tests should move or expand with it.

## Non-Functional Safety

Check:
- Did the change preserve important latency, throughput, or query-count expectations?
- Are concurrency, transaction, retry, and ordering semantics still safe?
- Are logs, metrics, traces, and failure diagnosis still adequate?
- Were security and data-boundary assumptions preserved?

## Review Verdict Template

When reviewing substantial work, summarize with:
- what change points were identified
- what abstractions were introduced and why
- what abstractions were intentionally avoided and why
- what contracts or legacy behaviors were protected by tests
- what non-functional or operational risks were checked
- remaining structural risks
- the next refactor to do if the area grows again
