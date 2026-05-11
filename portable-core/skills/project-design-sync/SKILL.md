---
name: project-design-sync
description: Sync repo-local detailed design documents with the current implemented system. Use when `ai-context/` already exists, after structural code changes, after accepted proposal apply work, during periodic design drift checks, or whenever `$design-pattern-engineering` needs fresher project design truth.
---

# Project Design Sync

## Overview

Sync the current implemented system design back into `ai-context/` so downstream skills can read a fresher design record instead of guessing from code alone.

This skill updates only the auto-synced sections and preserves human notes.

Treat sync as part of normal development flow:
- run it after meaningful structural, interface, workflow, or runtime changes
- use it to keep the design memory close to implementation while work is still happening
- do not wait for a big "refactor later" phase before refreshing the project design record
- read generated output in trust order: `High-Confidence Evidence` -> `Heuristic Signals` -> `Needs Human Review`
- on large repositories, treat design-source scanning as opt-in and keep the first sync narrow if script cost is unclear

## Workflow

### Step 1: Confirm The Design Record Exists

If `ai-context/` does not exist yet, run `$project-design-init` first unless the user explicitly wants a one-off temporary doc structure.

### Step 2: Choose The Sync Scope

Pick one of these modes before syncing:
- `full` for first population, major refactors, large merges, or periodic repository-wide refresh
- `local` for the changed modules after feature work or focused refactors

Prefer `local` by default when the affected modules are clear.

Then choose the sync layer:
- `architecture` for repo-level design views such as boundaries, interfaces, runtime, and hotspots
- `detail` for `ai-context/modules/*.md` detailed design docs
- `all` for both
- `auto` to choose `architecture` on first sync, `detail` for local targeted updates, and `all` for later broad refreshes

Use `references/sync-policy.md` for scope rules and drift handling.
Use `references/repo-layout-config.md` when the repository needs declared source roots, multi-path modules, or auxiliary design sources.
Use `ai-context/repo-layout.json` when it exists. Prefer this precedence:
1. explicit CLI overrides
2. declared repo layout config
3. heuristic discovery

### Step 3: Run The Sync Script

Run `scripts/sync_ai_context.py` against the repository root.

Recommended patterns:
- first sync, architecture-first: `py -3 scripts/sync_ai_context.py --root <repo> --mode full --layer auto`
- local detailed sync: `py -3 scripts/sync_ai_context.py --root <repo> --mode local --layer detail --targets billing notifications`
- manual full refresh: `py -3 scripts/sync_ai_context.py --root <repo> --mode full --layer all`
- declared layout override: `py -3 scripts/sync_ai_context.py --root <repo> --source-roots backend frontend --module-path asset-governance=backend/internal/audit,frontend/src/views/assets`
- include design sources only when needed: `py -3 scripts/sync_ai_context.py --root <repo> --mode full --include-design-sources`

The script updates:
- `ai-context/project.md`
- `ai-context/architecture.md`
- `ai-context/interfaces.md`
- `ai-context/runtime.md`
- `ai-context/hotspots.md`
- `ai-context/decisions.md`
- `ai-context/sync-status.md`
- `ai-context/modules/*.md`

It preserves all content outside the `AUTO-SYNC` markers.
It should prefer meaningful capability docs over flooding `ai-context/modules/` with every small technical folder.
It should read `ai-context/repo-layout.json` first when that file exists.
It should prune ignored directories, reuse cached scan results, and avoid rescanning design sources unless explicitly asked.

### Step 4: Review The Result

After syncing, inspect:
- whether the detected modules look credible
- whether the generated facts match the current code
- whether any large drift or uncertainty needs human notes
- whether downstream skills should trust only the high-confidence facts or can also rely on heuristic signals

If the repository is large or the first sync cost is uncertain:
- start with `local` on one or a few declared modules
- keep design sources off unless proposal or design-doc evidence is required
- expand to broader sync only after the narrower pass looks credible

If this is the repository's first sync:
- let the first pass focus on architecture views
- keep module detailed design selective
- allow detailed module docs to fill in over time through normal feature and refactor work

If the auto-synced output looks clearly wrong, correct the sync scope or add human notes instead of pretending the design record is final truth.

### Step 5: Feed The Result Back Into Engineering Skills

After a successful sync, treat `ai-context/` as preferred current-system design input for:
- `$design-pattern-engineering`
- `$design-spec`

If sync reveals unexpected drift, call that out in implementation or review output.

If `openspec/` also exists, use the refreshed `ai-context/` docs as implemented-system truth and OpenSpec artifacts as intended-change truth.

## Output Contract

For substantial sync work, report:
- `Sync mode`
- `Sync layer`
- `Layout config`
- `Scan scope`
- `Updated docs`
- `Updated modules`
- `Drift or uncertainty`
- `Recommended follow-up`

## Non-Negotiable Behaviors

- Do not overwrite human notes while syncing generated sections.
- Do not claim the synced docs are perfect truth when they are still heuristic.
- Do not run full sync by reflex when a local sync is enough.
- Do not leave stale `sync-status.md` after updating the design record.
- Do not ignore obvious code/doc drift once it is detected.
