# Self-Evaluation Scorecard

Use this reference before concluding substantial implementation, refactor, or review work.

## Primary Goal

Turn "this feels cleaner" into a disciplined ship, defer, or fix-now decision.

## Scoring Method

Score each dimension from 0 to 2:
- `0` = unacceptable, missing, or unverified
- `1` = acceptable but still risky or incomplete
- `2` = strong and clearly supported by the change

## Dimensions

### Local Fit

- Does the change fit the repository's existing structure, naming, and dependency rules?

### Simplicity

- Did the change reduce complexity instead of merely redistributing it?

### Separation Of Concerns

- Are responsibilities clearer and more localized than before?

### Extensibility

- Can the next likely variant be added with less branching or duplication?

### Compatibility Safety

- Were public contracts, schemas, and operational assumptions preserved?

### Test Protection

- Are moved behaviors, legacy assumptions, and new seams protected by tests?

### Non-Functional Safety

- Were performance, concurrency, security, and observability constraints preserved?

### Readability

- Would a teammate understand where to make the next change?

## Hard Gates

Treat these as fix-now items, not optional follow-ups:
- `Compatibility Safety = 0`
- `Test Protection = 0`
- `Non-Functional Safety = 0` on sensitive code

If any hard gate is `0`, do not conclude confidently.

## Decision Rules

Use the scorecard to pick the ending:
- `13-16` with no hard-gate failures -> ready to conclude normally
- `10-12` with no hard-gate failures -> acceptable to conclude, but name the follow-up risks clearly
- `0-9` -> reduce scope, fix the biggest design or safety gap, or conclude only as a constrained partial step

Additional interpretation:
- if `Local Fit = 0`, the change likely imposed the wrong shape on the repository
- if `Simplicity = 0`, remove indirection before adding more polish
- if `Extensibility = 0` on a variation-heavy task, the seam is probably still in the wrong place

## Output Format

Keep the output short. For example:
- `Local fit: 2`
- `Compatibility safety: 2`
- `Test protection: 1`
- `Decision: conclude with follow-up to tighten retry-path tests`
