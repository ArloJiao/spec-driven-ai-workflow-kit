# Refactor Now Vs Defer Matrix

Use this reference when you see a structural problem and need to decide whether to reshape it now, take a narrower step, or only record it.

## Primary Goal

Prevent two opposite failures:
- ignoring a design problem that is actively making the current task worse
- turning a local task into a stealth redesign

## The Three Outcomes

- `Refactor now` -> reshape during the current task because the safer outcome depends on it
- `Take a narrow step` -> add one seam, adapter, or extraction now, then record broader cleanup separately
- `Record only` -> leave the structure mostly as-is and document the follow-up

## Refactor Now

Prefer `Refactor now` when most of these are true:
- the task already touches the area deeply
- the second or third variation is arriving now, not hypothetically later
- duplication or branching is already increasing inside the changed path
- a local seam can remove the pressure without breaking callers
- tests exist or can be added within the current budget
- the move is reversible or compatibility-preserving

Typical examples:
- extracting a strategy seam before adding a second provider
- splitting validation from transport before a route gains more business rules
- introducing a value object when invariants are already duplicated in the touched code

## Take A Narrow Step

Prefer `Take a narrow step` when the direction is clear but full cleanup is too expensive right now.

Signals:
- the best design would touch many callers or files outside the requested scope
- the module is shared, legacy-heavy, or currently unstable in production
- compatibility is sensitive and the safest move is an adapter or shim
- ownership or repository conventions are still partly unclear

Typical examples:
- add a compatibility adapter instead of moving every caller today
- introduce branch-by-abstraction before a broader service split
- extract one use-case or policy object, but leave neighboring legacy code in place for now

## Record Only

Prefer `Record only` when refactoring would be speculative or unsafe in the current task.

Signals:
- the code path is unlikely to grow again soon
- the issue is mostly stylistic and does not block the change
- there is not enough understanding or test coverage to move behavior safely
- the request is an urgent hotfix and extra structure is not required for safety
- the better design depends on product or architecture decisions that have not been made yet

Typical examples:
- a one-off admin script with no likely reuse
- a messy module discovered during incident response where the fix is one isolated guard
- a subsystem-wide naming cleanup during a small feature request

## Escalation Rules

Upgrade from `Record only` to `Take a narrow step` or `Refactor now` when:
- the same pressure appears again in the same area
- the current task would otherwise duplicate logic or add another branch layer
- a safe seam has become obvious and cheap
- new tests now make the change low-risk

## Output Reminder

State the decision plainly:
- `Refactor now because ...`
- `Take a narrow step now and defer ...`
- `Record follow-up only because ...`
