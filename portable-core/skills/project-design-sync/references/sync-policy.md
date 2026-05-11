# Sync Policy

Use this reference before syncing repo-local detailed design documents.

## Primary Goal

Keep `ai-context/` useful enough for engineering decisions without turning sync into a heavyweight reverse-engineering exercise on every task.

## Layout Resolution

When the repository keeps `ai-context/repo-layout.json`, prefer this order:
1. explicit CLI overrides
2. declared layout config
3. heuristic discovery

This keeps the sync logic generic across monorepos, nested app roots, and cross-cutting module maps.

When `design_sources` are declared, treat them as auxiliary evidence:
- useful for understanding intended boundaries and proposal truth
- not a replacement for code and test truth
- best surfaced in heuristic signals or review-needed guidance

For performance-sensitive repositories:
- keep design-source scanning opt-in
- start with code-only sync unless design evidence is necessary for the current question
- use declared layout config to reduce repository guessing before widening the scan

## Modes

### Local Sync

Prefer `local` when:
- the changed modules are known
- a feature or refactor touched a bounded area
- the broader repository shape is unchanged

Use `--targets` to specify module names.
If `local` is chosen without explicit targets, the sync may need to fall back to all detected modules to avoid leaving module docs stale.
If scan cost is uncertain, use `local` first as a probe before attempting a broader repository-wide refresh.

### Full Sync

Use `full` when:
- the repo was just initialized
- architecture changed broadly
- a large merge landed
- drift has accumulated for a long time
- the user explicitly asks for a repository-wide refresh

For larger repos, prefer a cached, declaration-first full sync over blindly adding more timeout budget.

## Layers

Prefer these layers:
- `architecture`: repo-level design views only
- `detail`: module-level detailed design only
- `all`: both layers

Default posture:
- first sync -> start with `architecture`
- feature or refactor follow-up -> use `detail` on touched modules
- periodic or explicit broad refresh -> use `all`

## Auto-Synced Sections

Sync tooling should only replace content between:
- `<!-- AUTO-SYNC:BEGIN -->`
- `<!-- AUTO-SYNC:END -->`

Everything else is human-owned.

Inside the generated block, prefer three trust bands:
- `High-Confidence Evidence` for direct file-system or config facts
- `Heuristic Signals` for naming- and layout-based inference
- `Needs Human Review` for architectural conclusions or compatibility-sensitive judgments

Do not flatten these into one undifferentiated bullet list.

## Drift Handling

When code and docs disagree:
- trust code and tests for current behavior
- update generated sections to match current evidence
- preserve human notes describing why the drift happened
- mention unresolved ambiguity in `sync-status.md`

## Human Review Rule

The synced docs are design memory, not legal proof.

After important syncs, it is normal to review:
- module names
- major boundaries
- hotspot lists
- generated dependency clues
- whether the refreshed docs are now trustworthy enough for `$design-pattern-engineering`

## Module Doc Scope

Prefer `ai-context/modules/*.md` for:
- business capabilities
- integration-heavy subsystems
- shared policy or workflow seams
- hotspots that future design work will revisit

Usually do not create or keep separate module docs for:
- asset-only folders
- generated clients or build output
- migrations, fixtures, or test-only directories
- tiny leaf folders that are only implementation details

If the repo shape is ambiguous, keep fewer module docs and let human notes call out the uncertainty.
