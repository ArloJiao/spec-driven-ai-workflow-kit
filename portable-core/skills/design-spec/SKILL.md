---
name: design-spec
description: Use this skill when a repository already uses OpenSpec and you want one joint workflow that combines OpenSpec phase context with the core design-pattern-engineering skill. This skill is a collaboration layer, not a second design-pattern system.
---

# Design Spec

## Overview

Use this skill when the repository already works with `openspec/` and the task should follow OpenSpec's phase flow while still using the core `design-pattern-engineering` skill for design-pattern decisions, scope control, test protection, and in-loop code-shape correction.

This is a joint-work skill, not a separate design-pattern variant.

Treat responsibilities like this:
- `OpenSpec` provides change context, phase, proposal truth, and spec constraints
- `ai-context/` provides current implemented-system design truth when the repo keeps it
- `design-pattern-engineering` provides pattern selection, refactor discipline, compatibility safety, test obligations, and code review standards
- this skill coordinates both so the right design work happens at the right phase

## When To Use This Skill

Use this skill when:
- the repository maintains `openspec/`
- the task is explicitly in `explore`, `proposal`, `apply`, or `archive`
- you want one skill to combine OpenSpec context with design-pattern-guided engineering behavior

Do not use this as the default in repositories without OpenSpec. Use `$design-pattern-engineering` instead.

## Core Contract

Always follow these rules:
- `design-pattern-engineering` remains the single source of truth for actual pattern and code-quality judgment
- this skill adds phase behavior and spec-awareness only
- code and tests still outrank stale specs
- if implementation reality diverges from proposal truth, make the divergence explicit
- `archive` is passive by default unless the user asks for retrospective or follow-up design notes

## Step 1: Read Relevant OpenSpec Context

Read only the OpenSpec material relevant to the current change:
- `ai-context/repo-layout.json` when it exists, to understand declared source roots, module mappings, and design sources
- `ai-context/sync-status.md`, the nearest `ai-context/modules/*.md`, and other `ai-context/*.md` files when they exist
- `openspec/project.md`
- `openspec/config.yaml` when it shapes workflow or constraints
- the closest docs under `openspec/specs/`
- the active explore, proposal, or apply artifacts if they exist
- code and tests in the touched area

Use `references/openspec-phase-guide.md` to map the current phase to the correct type of design work.

Treat `ai-context/` as implemented-design memory and OpenSpec artifacts as proposal or phase memory. If they disagree, verify against code and tests, then call out the drift explicitly.

When `ai-context/` is present, read it in trust order:
- `High-Confidence Evidence` for current implementation facts
- `Heuristic Signals` for inspection leads
- `Needs Human Review` for unresolved boundaries or compatibility questions

## Step 2: Use The Core Design-Pattern Skill As The Engine

After reading OpenSpec context, reuse the core design-pattern-engineering guidance for actual design judgment:
- `../design-pattern-engineering/references/pattern-selection.md`
- `../design-pattern-engineering/references/classic-gof-patterns.md`
- `../design-pattern-engineering/references/modern-patterns.md`
- `../design-pattern-engineering/references/change-budget-and-safety.md`
- `../design-pattern-engineering/references/test-obligation-matrix.md`
- `../design-pattern-engineering/references/refactor-triggers.md`
- `../design-pattern-engineering/references/code-review-checklist.md`
- `../design-pattern-engineering/references/self-evaluation-scorecard.md`
- `../design-pattern-engineering/references/language-mapping.md`
- `../design-pattern-engineering/references/project-design-doc-lifecycle.md`

Keep the same quality bar as the core skill:
- explicit pattern candidates when the decision matters
- compatibility-safe and scope-aware refactors
- tests that move with behavior
- in-loop structural correction during implementation

## Phase Behavior

### Explore

In `explore`, do key design analysis before locking a proposal.

Required work:
- identify the changed capability and active code pressure
- map stable contracts, likely change points, and compatibility boundaries
- compare current implemented design hints from `ai-context/` with proposal assumptions from `openspec/`
- shortlist pattern candidates or state clearly that no named pattern is needed
- identify risks, unknowns, and test obligations
- decide whether the safe next step is simple implementation, narrow refactor, or explicit proposal design

### Proposal

In `proposal`, do the actual design.

Required work:
- convert explore findings into a concrete design choice
- name the chosen pattern, seam, or simpler alternative
- define boundaries, dependency direction, and migration strategy if needed
- specify compatibility rules, test plan, and non-functional guardrails
- record rejected alternatives and why

### Apply

In `apply`, implement the chosen design and keep watching code shape while coding.

Required work:
- implement or refactor in the agreed direction
- keep `refactor-triggers.md` active during coding
- protect moved behavior with tests
- surface code-shape issues discovered during apply, especially when a narrow correction is needed
- update the relevant spec or proposal truth if implementation reality changed within approved scope
- if implemented structure or tracked boundaries changed materially and `ai-context/` exists, use `../design-pattern-engineering/references/project-design-sync-triggers.md` to choose whether to recommend or perform `$project-design-sync`
- if the change is module-local and the matching detailed design doc is missing or stale, update that module doc in the same task

### Archive

In `archive`, take no special design action by default.

Only add work when the user asks for:
- retrospective notes
- final design summary
- explicit follow-up design debt recording

## Output Contract By Phase

- `explore`: context read, change pressure, pattern candidates, compatibility constraints, test obligations, open questions
- `proposal`: chosen design, boundaries and seams, compatibility plan, test plan, migration plan, rejected alternatives
- `apply`: design intent, implementation notes, issues observed in code, local corrections made, tests added or updated, spec sync notes
- `archive`: no extra section unless requested

When pattern choice matters, keep the same explicit fields as the core skill:
- `Pattern candidates`
- `Chosen pattern` or `No named pattern`
- `Why this fits`
- `Language note`
- `Why simpler or heavier alternatives were rejected`

## Non-Negotiable Behaviors

- Do not duplicate a second design-pattern rule system here.
- Do not skip design analysis during `explore`.
- Do not let `proposal` stay abstract when the real design choice is already knowable.
- Do not let `apply` devolve into feature-only coding that ignores structure problems.
- Do not broaden implementation beyond accepted proposal truth without making that explicit.
- Do not silently let code and OpenSpec drift apart.
- Do not invent extra `archive` work when no design action is needed.
