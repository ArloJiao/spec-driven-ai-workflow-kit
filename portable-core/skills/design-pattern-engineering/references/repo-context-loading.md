# Repository Context Loading

Use this reference when the repository may already contain durable project context that should guide design choices.

## Primary Goal

Read project-specific context before applying generic architecture advice.

## Loading Order

When multiple context sources exist, read them in this order:
1. `ai-context/sync-status.md` when `ai-context/` exists, so you know how fresh the design memory is
2. `ai-context/repo-layout.json` when it exists, so you can understand declared source roots, module-to-path mappings, and design sources
3. the nearest `ai-context/modules/*.md` plus `ai-context/project.md` and `ai-context/architecture.md`
4. `ai-context/interfaces.md`, `ai-context/runtime.md`, `ai-context/hotspots.md`, and `ai-context/decisions.md` when the task touches those concerns
5. the closest maintained project context docs for the affected area
6. other local context folders or project guidance when they exist
7. architecture docs, ADRs, contributor guides, or design notes
8. tests and executable behavior that define current truth
9. inferred conventions from code structure

No dedicated context system is required. Use the relevant project memory that already exists.

If `ai-context/` exists but the sync status is old or uncertain, treat it as a high-value hint rather than as guaranteed truth.

When reading an `ai-context/` document:
- trust `High-Confidence Evidence` for direct repository facts first
- use `Heuristic Signals` to guide code inspection and pattern exploration
- do not treat `Needs Human Review` bullets as resolved design truth without checking code, tests, or user guidance

When reading `ai-context/repo-layout.json`:
- treat declared paths as topology guidance, not as proof that the paths are still current
- use it to find the right code and design evidence faster
- if the file obviously drifted from the repository, recommend `$project-design-sync` or a layout-config refresh

## What To Extract

From repo-local context docs, capture:
- project design posture
- architecture style
- repository conventions
- stable constraints
- design-memory expectations

From maintained capability or project docs, capture:
- capability boundaries
- domain vocabulary
- local seams and hotspots
- compatibility or rollout constraints
- preferred and discouraged patterns

From tests and code, capture:
- the current behavior of the capability you are changing
- the difference between current truth and proposed change
- where the actual change pressure is showing up

## Capability Matching

When the task maps to one capability:
- read the closest docs first
- do not load unrelated capability docs

When the task spans multiple capabilities:
- read only the affected docs
- note cross-capability constraints in the design intent

## Precedence Rules

Use this order when guidance conflicts:
1. observable code and tests that define current behavior
2. the closest maintained repo docs for the affected capability or constraint
3. broader project-level docs
4. inferred conventions from the touched area
5. generic skill guidance

If code and docs disagree:
- avoid assuming the docs are fully current
- confirm behavior from code and tests
- note the discrepancy in the design review
- update the closest maintained doc if the task scope permits

## Brownfield Rule

Do not require a complete context system before making safe improvements.

If maintained repo docs exist, use the relevant ones.
If project context is partial, use the useful parts only.
If no durable context exists, fall back gracefully rather than blocking the task.
