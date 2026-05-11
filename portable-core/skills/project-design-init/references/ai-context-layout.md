# AI Context Layout

Use this reference when initializing repo-local detailed design documents.

## Primary Goal

Create a small but durable design-memory structure that records the implemented system shape and stays maintainable over time.

## Default Layout

Prefer this structure:

```text
ai-context/
  project.md
  architecture.md
  interfaces.md
  runtime.md
  hotspots.md
  decisions.md
  sync-status.md
  repo-layout.json
  modules/
    <module>.md
```

## Auto-Synced Vs Human Notes

Every file should keep these concerns separate:
- `Auto-Synced`: facts regenerated from code, tests, and config
- `Human Notes`: rationale, tradeoffs, future concerns, and reviewer annotations

Use explicit markers so sync tooling can replace only the generated section.

Inside `Auto-Synced`, prefer this evidence order:
- `High-Confidence Evidence`: direct file, path, config, test, and entrypoint facts
- `Heuristic Signals`: naming, layout, and lightweight inference clues
- `Needs Human Review`: boundaries, contracts, and design judgments that should not be trusted blindly

This keeps downstream skills from treating every generated bullet as equally trustworthy.

## File Purposes

- `project.md`: project-wide identity, stack, repo profile, main entrypoints, design posture
- `architecture.md`: system shape, dependency direction, major module map, extension seams
- `interfaces.md`: API or messaging boundaries, public contracts, external integrations
- `runtime.md`: startup flow, workers, async behavior, schedulers, jobs, observability signals
- `hotspots.md`: fragile or high-churn areas, large files, risky modules, migration zones
- `decisions.md`: important current design choices and deliberate tradeoffs
- `sync-status.md`: last sync time, mode, evidence sources, confidence model, drift warnings
- `repo-layout.json`: machine-readable declaration of source roots, design sources, ignored paths, and module-to-path mappings
- `modules/*.md`: detailed design record for each meaningful capability or subsystem

## Design Layers

Treat the docs as two layers:

- `Architecture Design`
  - `project.md`
  - `architecture.md`
  - `interfaces.md`
  - `runtime.md`
  - `hotspots.md`
  - `decisions.md`
- `Detailed Design`
  - `modules/*.md`

Prefer an architecture-first first sync, then let detailed module docs grow incrementally as features and refactors touch them.

## Diagram Guidance

Prefer Mermaid diagrams in human-owned sections when they materially improve readability.

Good diagram candidates:
- system context or container view in `architecture.md`
- key request or job sequence in `runtime.md`
- contract or boundary overview in `interfaces.md`
- sequence, component, or state view in `modules/*.md`

Do not generate diagrams just to decorate the doc. Add them when they make a future change easier to reason about.

## Module Doc Rule

Create module docs for meaningful capabilities, not every utility folder.

Good candidates:
- `billing`
- `orders`
- `auth`
- `notifications`

Usually skip:
- `utils`
- `shared`
- `types`
- `common`

unless they are genuine design hotspots worth tracking separately.

Also usually skip folders that are mainly:
- generated output
- static assets or public files
- migrations or fixtures
- localization-only content
- tiny implementation details that do not own a business boundary

Prefer a module doc when the folder represents a capability, subsystem, or stable seam that future feature work is likely to revisit.
