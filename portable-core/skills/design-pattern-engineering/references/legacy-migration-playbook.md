# Legacy Migration Playbook

Use this reference when the best maintainable design cannot be reached safely in one step.

## Primary Goal

Improve structure in active or fragile systems through incremental migration, not big-bang replacement.

## Migration Tactics

## 1. Branch By Abstraction

Use when:
- old and new implementations must coexist temporarily
- callers cannot all switch at once

How:
- define or reuse a stable seam
- route callers through the seam
- move callers gradually from old to new implementation
- remove the old path only after coverage and usage are clear

## 2. Compatibility Adapter

Use when:
- the new internal model is better, but external callers still expect the old contract

How:
- keep the external contract stable
- translate between old and new shapes at the boundary
- retire the adapter only when callers are migrated

## 3. Deprecation Shim

Use when:
- a method, class, endpoint, or module should be phased out but cannot disappear immediately

How:
- keep a thin compatibility wrapper
- delegate to the new implementation
- mark the old entrypoint as deprecated in comments or docs when appropriate
- avoid adding new behavior to the deprecated surface

## 4. Strangler Seam

Use when:
- a large legacy module needs gradual replacement around a stable boundary

How:
- choose one high-value slice
- route only that slice to the new implementation
- keep expanding the new path slice by slice
- leave untouched behavior on the legacy path until it is safe to migrate

## 5. Feature-Flagged Cutover

Use when:
- the migration risk is operational, not just structural
- rollback needs to stay simple

How:
- isolate the new behavior behind a narrow flag
- keep both paths observable
- ensure the old path still works before rollout
- remove the flag after the new path is trusted

## 6. Dual Read / Dual Write

Use sparingly when:
- data or integration migration cannot be validated by code structure alone

Rules:
- use only with a clear reason
- keep the dual-write window short
- add validation and observability
- avoid making this the default refactor tactic

## Migration Sequence

For risky legacy refactors, prefer this order:
1. characterize existing behavior with tests
2. create a seam
3. move one slice behind the seam
4. validate compatibility
5. migrate callers gradually
6. remove dead paths only after confidence is high

## Choosing The Smallest Tactic

Prefer:
- branch-by-abstraction for behavior replacement
- adapters for contract preservation
- shims for phased retirement
- strangler seams for oversized legacy modules
- feature flags for risky operational cutovers

Do not combine all tactics unless the system truly needs them.

## Warning Signs

Pause and reassess if:
- the migration plan requires too many simultaneous changes
- the new design cannot coexist with the old one at all
- tests do not yet capture the critical behavior
- the change starts depending on undocumented operational assumptions
