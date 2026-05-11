# Change Budget And Safety

Use this reference before performing structural edits in an existing codebase.

## Primary Goal

Improve maintainability without silently expanding the scope, breaking compatibility, or destabilizing active workflows.

## Default Safety Posture

Unless the user explicitly asks for a redesign:
- preserve public contracts, wire formats, persistence behavior, and rollout expectations
- keep the change local to the requested feature, bug, or review target
- prefer reversible refactors over sweeping rewrites
- separate "safe implementation now" from "larger redesign later"

## What Counts As Compatibility

Treat these as compatibility-sensitive unless the user says otherwise:
- public APIs and response shapes
- event payloads and message formats
- database schemas and migration assumptions
- serialized job payloads
- plugin and extension contracts
- filenames, config keys, and operational conventions used by other modules

## Change Budget Rules

Stay inside the budget by default:
- refactor the touched path first, not the whole subsystem
- introduce the smallest seam that removes the current pain
- prefer extraction over relocation when moving code would ripple through many callers
- if a better architecture requires broad churn, implement a narrow safe step and document the next step

## Mandatory Test Gate

Before concluding a structural change:
- add or update focused tests for moved or newly isolated behavior
- create characterization tests first when touching unclear legacy behavior
- keep integration coverage for critical contracts that must not drift
- do not delete behavior-protecting tests just because the structure improved

## Safety Questions

Ask before changing structure:
- what behavior must remain unchanged?
- which callers or systems depend on this contract?
- can the refactor be performed behind a stable interface?
- what is the smallest reversible step?
- which tests prove the behavior still matches expectations?

## Safe Outcomes

Prefer outcomes like:
- one new seam that localizes variation
- one adapter that preserves the old contract while enabling the new structure
- one extracted use-case that leaves the route contract intact
- one new value object that hardens invariants without changing external behavior

Avoid outcomes like:
- renaming or moving half the subsystem during a small feature request
- changing response shapes as a side effect of "cleanup"
- breaking extension hooks because the internal model is now cleaner
- coupling the refactor to a migration plan that was never requested
