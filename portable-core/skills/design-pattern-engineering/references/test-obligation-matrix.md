# Test Obligation Matrix

Use this reference to decide the minimum testing work required before concluding a change.

## Primary Goal

Make test protection proportional to the structural risk of the change.

## Baseline Rule

If behavior moved, variation seams changed, or compatibility-sensitive code was reshaped, tests must move or grow with it.

## Change Type To Minimum Test Obligation

### Behavior Moved Or Split Across New Modules

Minimum:
- add or update focused tests around the moved behavior
- keep at least one higher-level test for the stable contract

### New Strategy, Policy, Provider, Or Pluggable Seam

Minimum:
- one test for existing behavior through the new seam
- one test for the new variant
- contract-oriented tests if multiple implementations must behave consistently

### Legacy Refactor With Unclear Behavior

Minimum:
- create characterization tests first
- then perform the structural change
- then keep or adjust focused tests around the extracted seam

### Hotfix Or Regression Repair

Minimum:
- add a regression test that fails before the fix and passes after it
- add a narrow integration or contract test if the bug crossed a boundary

### Compatibility Adapter, Shim, Or Migration Seam

Minimum:
- test the old contract still works
- test the new path or seam works
- test routing or selection logic if both paths can exist temporarily

### Domain Invariant, Value Object, Or Policy Extraction

Minimum:
- add focused invariant or rule tests at the extracted boundary
- keep one higher-level workflow test if the rule matters to user-visible behavior

### Concurrency, Retry, Ordering, Or Idempotency Change

Minimum:
- add tests that exercise the specific non-functional behavior being preserved
- do not rely only on happy-path tests

### Pure Rename Or Mechanical Relocation With Strong Existing Coverage

Minimum:
- keep relevant existing tests passing
- add new tests only if the move created a new seam whose behavior is not otherwise covered

## Review Questions

Ask before concluding:
- what behavior did this change make easier to break?
- which test now proves the old contract still holds?
- which test proves the new seam is real and not just cosmetic?
- if the code was hard to understand, did we add characterization tests before editing it?

## Anti-Patterns

Do not claim a structural change is safe when:
- only unrelated tests ran
- integration-sensitive behavior moved with no contract test remaining
- legacy behavior changed but no characterization test was added
- a new abstraction was introduced but every implementation is still effectively untested
