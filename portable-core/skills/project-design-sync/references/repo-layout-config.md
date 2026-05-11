# Repo Layout Config

Use this reference when sync should prefer a declared repository layout over pure heuristic discovery.

## Primary Goal

Make sync declaration-first without hardcoding every repository shape into the script.

## Default File

Prefer `ai-context/repo-layout.json`.

## Precedence

Use this order:
1. explicit CLI overrides
2. `ai-context/repo-layout.json`
3. heuristic discovery

## What The Config Should Declare

- `source_roots`
- `design_sources`
- `ignore_paths`
- `modules.<name>.paths`

## Why This Helps

This keeps the sync workflow generic:
- multi-root repos can declare their real implementation roots
- cross-cutting modules can span multiple paths
- design-oriented sources can be included as auxiliary evidence
- noisy folders can be ignored without adding project-specific code branches

## Design Rule

Use the config to describe repository topology, not to restate every design decision.
