# Repo Layout Config

Use this reference when a repository is too complex to trust source-root guessing alone.

## Primary Goal

Prefer a small repo-local declaration of repository shape over piling on more one-off project-structure heuristics.

## Default File

Prefer `ai-context/repo-layout.json`.

This file is not another design document. It is a machine-readable layout contract that helps `project-design-init` and `project-design-sync` stay aligned with the repository's real topology.

## Precedence

When both config and heuristics exist, use this order:
1. explicit CLI overrides
2. `ai-context/repo-layout.json`
3. heuristic discovery

## Suggested Shape

```json
{
  "version": 1,
  "source_roots": ["casper-backend", "casper-frontend"],
  "design_sources": ["openspec", "docs"],
  "ignore_paths": ["node_modules", "dist"],
  "modules": {
    "task-runtime": {
      "paths": ["casper-backend/internal/runtime", "casper-frontend/src/views/tasks"]
    },
    "deployment-cicd": {
      "paths": [".gitlab-ci.yml", "deploy"]
    }
  }
}
```

## Field Meaning

- `source_roots`: the repo-relative roots that should be treated as primary implementation roots
- `design_sources`: proposal, architecture, or other design-oriented sources that should be treated as auxiliary evidence
- `ignore_paths`: paths that sync should ignore when scanning
- `modules`: explicit module-to-path mappings, including multi-path or cross-cutting modules

## When To Add This File

Prefer a layout config when:
- the repo has multiple subprojects or nested app roots
- meaningful modules do not match one folder one-to-one
- design sources such as specs or docs matter to architecture understanding
- heuristic source-root detection would otherwise be noisy or misleading

## Keep It Small

Do not turn this file into a second architecture specification.

It should declare:
- where implementation lives
- where design evidence lives
- what to ignore
- how named modules map to real paths

Everything else belongs in the normal `ai-context/*.md` documents.
