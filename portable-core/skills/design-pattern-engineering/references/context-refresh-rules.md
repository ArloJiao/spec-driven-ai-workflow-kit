# Context Refresh Rules

Use this reference when a code change may also require updating repository-local context such as `ai-context/`, `project-context/`, or maintained architecture notes.

## Primary Goal

Keep durable project context aligned with the implementation without turning every small change into documentation bureaucracy.

## Update Context When

Update the nearest relevant context doc when the task changes:
- a documented architecture boundary
- a public or cross-module contract
- the preferred extension seam for a capability
- a core domain term, invariant, or workflow rule
- a legacy migration status that the repo actively tracks
- a maintained hotspot or non-functional constraint that is no longer accurate

## Usually Do Not Update Context When

Do not widen the task just to edit docs for:
- tiny local refactors with no architectural effect
- internal renames that do not alter project-level meaning
- one-off debugging changes
- purely cosmetic cleanup

## Update The Closest Truth

Prefer updating:
- one capability note instead of the whole project guide
- one hotspot note instead of multiple summary docs
- one project-level rule only when the rule truly changed repo-wide

## If Docs Already Exist

When maintained project docs already exist:
- treat the relevant docs as part of the system
- update them when your change invalidates their current truth
- keep edits concise and factual

When `ai-context/` exists:
- prefer refreshing generated sections through `$project-design-sync`
- keep human notes human-owned
- do not manually overwrite `AUTO-SYNC` blocks unless sync tooling is unavailable and the user accepts the tradeoff
- use `project-design-sync-triggers.md` to decide whether the right scope is none, `local`, or `full`
- use `project-design-doc-lifecycle.md` to decide whether the touched work should update one detailed module doc now versus refreshing broader architecture docs

## If Docs Are Missing

If no durable context exists:
- do not create a large doc tree unless the user asks
- mention the missing context in the design review when it materially affected the task
- propose the smallest useful starting doc if repeated confusion is likely

## If Code And Docs Drifted

When you detect drift:
- rely on code and tests for immediate behavior truth
- note the drift explicitly
- update the closest maintained doc if it fits scope
- otherwise record a follow-up recommendation

If the drift is inside `ai-context/` generated sections, prefer a targeted or full `$project-design-sync` over ad hoc manual patching.
