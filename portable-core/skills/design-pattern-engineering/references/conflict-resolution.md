# Conflict Resolution

Use this reference when different sources of guidance point in different directions.

## Primary Goal

Resolve tradeoffs consistently without falling back to arbitrary architectural taste.

## Precedence Order

When rules conflict, prefer this order:
1. explicit user request and approved scope
2. repository-local docs and stable project conventions
3. compatibility-sensitive contracts and runtime safety constraints
4. framework or language idioms that the local team clearly follows
5. this skill's generic heuristics and pattern guidance

Generic pattern advice should not override stronger local evidence.

## Tie-Breakers

If two options are both reasonable, prefer the one that is:
- narrower in scope
- easier to reverse
- easier to test
- easier for the local team to recognize and maintain

## Common Conflict Cases

### Better Architecture Vs Requested Scope

- ship the smallest safe slice now
- keep refactors local by default
- record the broader redesign separately

### Repo Convention Vs Cleaner Greenfield Pattern

- fit the touched area to the local repo unless the local pattern is actively harmful
- if the local pattern is harmful, improve only the touched path unless the user asked for a broader reset

### Framework Idiom Vs Textbook Design Pattern

- keep the framework-idiomatic surface
- move the real seam to policy, orchestration, or boundary code underneath

### Missing Tests Vs Desire To Move Fast

- add the smallest test that protects the risky move
- for unclear legacy behavior, characterization tests come before structure changes

### Hotfix Urgency Vs Design Cleanup

- contain the bug first
- take only the extra structural move required to avoid making the area worse
- capture deeper cleanup as follow-up

## Output Reminder

When you make a tradeoff, say it plainly. Example:
- `Keeping the public contract unchanged and extracting only the policy seam in this task.`
- `Deferring the broader module split because the current scope is a hotfix and tests are still thin.`
