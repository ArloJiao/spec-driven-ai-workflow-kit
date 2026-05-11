# Project Design Doc Lifecycle

Use this reference when a repository keeps `ai-context/` and you need to decide how design docs should evolve during normal coding work.

## Primary Goal

Keep architecture docs small and stable, while letting detailed module docs grow incrementally with real code changes.

## Design Layers

- `Architecture Design`
  - `project.md`
  - `architecture.md`
  - `interfaces.md`
  - `runtime.md`
  - `hotspots.md`
  - `decisions.md`
- `Detailed Design`
  - `modules/*.md`

## Default Working Rule

Prefer this lifecycle:
- first sync -> architecture-first
- feature or refactor work -> update only the touched module detailed docs
- broader boundary or workflow change -> also refresh the relevant architecture docs
- occasional repo-wide refresh -> use manual `$project-design-sync`

## New Capability Rule

If the task introduces a new meaningful capability and the matching module doc is missing or blank:
- create or fill the module detailed design doc in the same task
- record the module's purpose, boundaries, collaborators, and main flow
- add a Mermaid diagram only if it makes the new flow materially easier to understand

## Existing Capability Rule

If the task changes an existing capability:
- update the affected module detailed design doc after the code change
- keep the doc aligned with the new behavior, seams, or workflow
- avoid widening the doc update beyond the changed area unless architecture meaning also changed

## Architecture Update Rule

Update or refresh architecture-level docs when the task changes:
- repo or subsystem boundaries
- public or cross-module contracts
- runtime or deployment flow
- important hotspots or architectural decisions

## Diagram Rule

Prefer Mermaid diagrams when they save future readers time.

Good diagram candidates:
- context or container view for architecture docs
- sequence or state view for module docs
- integration or boundary view for interface-heavy changes

Do not generate diagrams by default for every small change.
