# Project Design Sync Triggers

Use this reference when deciding whether a task should refresh `ai-context/` through `$project-design-sync`.

## Primary Goal

Refresh project design memory when implementation meaning changed, not on every tiny edit.

## No Sync Usually Needed

Usually do not recommend sync for:
- typo fixes, formatting cleanup, or comment-only edits
- tiny local bug fixes that do not change boundaries, contracts, or runtime flow
- internal renames that do not change design meaning
- test-only changes that do not reveal new system structure

## Recommend Local Sync

Recommend `local` sync when the task changed one bounded area such as:
- one module gained a new variant, provider, or policy seam
- one capability's internal workflow or dependency wiring changed
- one module's interface surface, module ownership, or hotspot status clearly changed
- a focused refactor extracted a strategy, adapter, repository, policy, or similar seam in one area

Typical posture:
- update the affected `ai-context/modules/*.md`
- refresh project-level docs only as generated context, without treating the whole repo as re-mapped
- prefer this as the normal detailed-design maintenance path during feature and refactor work

## Recommend Full Sync

Recommend `full` sync when the task changed repository-wide meaning such as:
- major architecture or dependency direction changed
- new top-level capabilities or source roots appeared
- interface, runtime, or workflow changes cut across multiple modules
- a large merge, migration, or proposal apply phase changed broad system shape
- existing `ai-context/` drift looks too large for a targeted refresh

## Strong Sync Signal

Treat sync as strongly recommended before concluding if:
- `ai-context/sync-status.md` is clearly stale relative to the current task
- the task changed boundaries that future design decisions are likely to rely on
- the task introduced or removed a tracked hotspot
- the task changed contracts or runtime flow that other teams or modules depend on

## Decision Rule

If unsure:
- choose no sync for cosmetic or hyper-local edits
- choose `local` when one capability clearly changed meaning
- choose `full` when the repo map itself may now be misleading

If the architecture docs are already good enough and only one capability changed, do not force a broad full sync just to keep detailed design current.

Do not hand-edit generated blocks as a substitute for the proper sync unless tooling is unavailable and the user accepts the tradeoff.
