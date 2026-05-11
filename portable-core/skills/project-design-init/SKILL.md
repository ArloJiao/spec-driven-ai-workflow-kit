---
name: project-design-init
description: Initialize repo-local detailed design documents for the current project. Use when a repository needs an `ai-context/` design-memory folder for the first time, when the team wants a durable record of the implemented system design, or before using `$design-pattern-engineering` against a codebase that lacks current design docs.
---

# Project Design Init

## Overview

Bootstrap a repo-local detailed design record under `ai-context/` so later skills can read the current implemented system shape instead of inferring everything from code every time.

This skill creates the document structure, seeds module design files, and keeps human notes separate from future auto-synced sections.

Treat `ai-context/` as working design memory for ongoing development, not as a post-hoc refactor artifact:
- `$design-pattern-engineering` should read it before making structural decisions
- `$project-design-sync` should refresh it after meaningful boundary, interface, or runtime changes
- if `openspec/` also exists, `ai-context/` records implemented design truth while OpenSpec records proposal or phase truth
- generated sections should be read in trust order: `High-Confidence Evidence`, then `Heuristic Signals`, then `Needs Human Review`
- architecture-level docs should form the small stable baseline, while detailed module docs are expected to grow incrementally during normal coding work

## Workflow

### Step 1: Confirm The Target Root

Run this skill from the project root whenever possible.

If the request is ambiguous, infer the current repository root from the working directory and initialize there.

### Step 2: Inspect The Existing Project Shape

Before creating files:
- inspect the main source roots
- identify likely capability or module folders
- note whether `ai-context/` already exists
- avoid overwriting existing design notes unless the user explicitly wants a reset

Use `references/ai-context-layout.md` for the canonical document structure.
Use `references/repo-layout-config.md` when the repository needs explicit source roots, multi-path modules, or auxiliary design sources.

### Step 3: Initialize The Design Record

Run `scripts/init_ai_context.py` to create:
- `ai-context/project.md`
- `ai-context/architecture.md`
- `ai-context/interfaces.md`
- `ai-context/runtime.md`
- `ai-context/hotspots.md`
- `ai-context/decisions.md`
- `ai-context/sync-status.md`
- `ai-context/repo-layout.json`
- `ai-context/modules/*.md`

The script uses templates from `assets/templates/ai-context/` and creates a declarative repo layout config so later syncs do not have to re-guess the whole repository shape.

Default behavior:
- keep existing files intact unless `--force` is justified
- create module docs only for likely capability folders, not every technical subdirectory
- declare detected source roots, design sources, ignored paths, and module-path mappings in `ai-context/repo-layout.json`
- preserve room for human notes from day one
- prepare the repo for an architecture-first first sync instead of trying to fully reverse-engineer every detailed module upfront

### Step 4: Explain What Was Created

After initialization, summarize:
- which docs were created
- which module docs were seeded
- which parts are only placeholders
- whether the next step should be `$project-design-sync`
- how `$design-pattern-engineering` should use the new `ai-context/` docs

### Step 5: Recommend The Follow-Up

After init, recommend `$project-design-sync` when:
- the repo already has substantial code
- the seeded docs are mostly empty shells
- the user wants the detailed design record populated immediately

If the user is about to start feature or refactor work, explicitly note that the initialized docs are only scaffolding until the first sync happens.

## Output Contract

For substantial initialization work, report:
- `Target root`
- `Layout config`
- `Created files`
- `Seeded modules`
- `Skipped existing files`
- `Next step`

## Non-Negotiable Behaviors

- Do not wipe human-written design notes unless the user explicitly asks.
- Do not overwrite existing `ai-context/` files casually.
- Do not create an oversized document tree that the repo is unlikely to maintain.
- Do not invent module boundaries that obviously conflict with the repository layout.
- Do not mix future auto-synced content and human notes in the same unmarked block.
