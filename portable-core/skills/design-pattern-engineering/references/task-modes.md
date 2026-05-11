# Task Modes

Use this reference first. It tells you how much design movement is appropriate for the current task.

## Primary Goal

Match the design effort to the user's real need instead of applying the same intensity to every task.

## Mode Selection

Infer the mode from the request:
- `feature` -> adding new behavior, a new endpoint, a new UI flow, or another supported variant
- `refactor` -> improving structure while preserving current behavior
- `hotfix` -> restoring correctness, reducing risk, or containing a production issue quickly
- `review` -> evaluating quality, maintainability, or readiness without necessarily changing code

If the task mixes modes, choose the riskiest dominant mode first. Example: an urgent production bug inside messy legacy code starts in `hotfix`, not `refactor`.

## Feature Mode

Use when the task introduces new capability or an additional rule, provider, or state.

Default focus:
- identify the likely next variation, not every imagined future one
- choose the lightest seam that makes the next variant cheaper
- fit the new shape into the existing module style
- shortlist concrete pattern candidates only if the pressure is real

Load first:
- `pattern-selection.md`
- `test-obligation-matrix.md`
- one relevant framework reference if needed

Minimum output:
- core responsibility
- pattern candidates or explicit no-pattern decision
- selected seam or chosen pattern
- language note if a named pattern is chosen
- compatibility boundary
- tests added or updated

## Refactor Mode

Use when behavior should remain stable but the structure is the real problem.

Default focus:
- keep the move local
- preserve public contracts and calling shape
- use characterization tests before changing unclear legacy behavior
- choose between refactor now, defer, or record only
- name a pattern only when it improves the touched area now

Load first:
- `change-budget-and-safety.md`
- `refactor-defer-matrix.md`
- `test-obligation-matrix.md`

Add `legacy-migration-playbook.md` when the area is shared, old, or high-risk.

## Hotfix Mode

Use when correctness, stability, or production safety matters more than structural elegance.

Default focus:
- contain the failure with the smallest safe step
- add the narrowest regression test that proves the fix
- avoid opportunistic subsystem rewrites
- record design debt instead of hiding it inside the hotfix
- allow a pattern move only when it directly reduces risk in the current fix

Load first:
- `test-obligation-matrix.md`
- `change-budget-and-safety.md`
- `conflict-resolution.md`

If the hotfix uncovers repeated structural pressure, take only the smallest extra seam needed to keep the fix from making the area worse.

## Review Mode

Use when the task is primarily judgment, critique, or readiness assessment.

Default focus:
- findings first
- explain the design pressure, not just the pattern name
- separate must-fix issues from optional cleanup
- recommend the smallest next move with the best risk reduction
- mention concrete pattern candidates when they clarify the recommendation
- add a brief language note when the same recommendation would look different across stacks

Load first:
- `code-review-checklist.md`
- `self-evaluation-scorecard.md`
- `conflict-resolution.md` if tradeoffs are unclear

## Mode Shift Rules

Shift modes only when the evidence changes:
- `feature -> refactor` when structural work becomes necessary to land the feature safely
- `refactor -> hotfix` when correctness or incident response becomes the real priority
- `feature/refactor -> review` when the user mainly wants judgment, not implementation

When a shift happens, state it briefly and tighten the scope again before continuing.
