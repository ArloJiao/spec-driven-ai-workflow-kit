---
name: workstream-hub
description: Manage the user's cross-project workstreams, interruptions, branch context, and session handoffs from a personal delivery view. Use when the user needs continuity across projects, customers, bugfixes, feature lines, or interrupted coding sessions.
---

# Workstream Hub

## Overview

Use a global workstream hub to track the user's active delivery lines from the user's point of view, not from a single repository's point of view.

The canonical object is a `workstream`, not a repo and not a branch:
- one repo can contain several concurrent customer deliveries, bugfixes, and feature lines
- a branch is only one attribute of a workstream and can change over time
- repo-local design docs still belong in the repo; this hub only stores macro execution context and short recovery notes

By default, keep durable hub data in a configurable location:

1. `$CODEX_HUB` when set.
2. `$CODEX_HOME/workstream-hub` when `$CODEX_HOME` is set.
3. Otherwise, the user's home directory under `.codex/workstream-hub`.

Do not assume a particular drive, username, or machine layout.

## Quick Start

1. If the hub does not exist, run `scripts/ensure-workstream-hub.ps1`.
2. Read `portfolio/dashboard.md` first.
3. Identify the target `workstreams/<id>.md` file, or create it from `assets/templates/hub/workstream-template.md`.
4. Before switching away from a task, update the workstream and add a short handoff note under `sessions/YYYY-MM-DD/`.
5. After the work is done, refresh the touched workstream and the dashboard.

Use `references/workstream-model.md` for the directory layout, naming rules, and field meanings.

## Workflow

### Step 1: Confirm The Hub Root

- Default to `$CODEX_HUB` when set.
- If the user has a storage preference, honor it.
- If the selected root is constrained or low on space, state that before creating large local state there.

### Step 2: Identify The Target Workstream

Infer the workstream from the user request using the smallest stable identity that matches the real delivery line:
- system or repo
- customer or delivery target
- work type such as `feature`, `bugfix`, `hotfix`, `delivery`, or `investigation`
- release line, branch family, or ticket when that is what separates the work from another concurrent stream

Create a new workstream when the user is effectively asking for a different delivery line. Typical triggers:
- the same repo now serves a different customer or acceptance path
- a production or pre-prod bug becomes urgent and interrupts feature delivery
- a new branch must stay isolated from the current branch family
- the user is now tracking a different goal, owner, or blocking chain

### Step 3: Load Only The Needed Global Context

Read the minimum set of files needed to restore context:
- `portfolio/dashboard.md`
- the target `workstreams/<id>.md`
- the most recent handoff note for that workstream if the previous session was interrupted
- an optional `projects/<system>.md` file if stable system-level notes exist

Do not bulk-load every workstream or every session note.

### Step 4: Work With Clear Separation Of Concerns

- Keep macro execution state in the global hub.
- Keep environment and server facts in `$preflight-dev-context` resources.
- Keep repo-local architecture and design truth inside the repository, for example `ai-context/`.
- When a technical task needs both macro context and repo design context, read the workstream first, then load the repo-local design docs that are actually relevant.

### Step 5: Update On Interruptions

Before switching to another task:
- update `current_focus`, `next_step`, `blockers`, `risks`, `branches`, and `last_updated` in the active workstream
- append a short handoff note under `sessions/YYYY-MM-DD/`
- move the old workstream to `paused`, `blocked`, or `waiting` in the dashboard as appropriate
- add or activate the new workstream in the dashboard

Keep handoff notes short. Their job is to restore action quickly, not to become a second design doc set.

### Step 6: Close The Loop After Work

After analysis, coding, debugging, or branch planning:
- update the touched workstream with the new focus and next step
- remove blockers that are no longer real
- record branch or environment changes if they matter to future recovery
- refresh the dashboard lists so the current state is visible at a glance
- if the repo design materially changed, update the repo-local design docs separately instead of stuffing detail into the global hub

## Output Contract

For substantial use of this skill, report:
- `Hub root`
- `Selected workstream`
- `Context loaded`
- `Updates made`
- `Next step`

## Non-Negotiable Behaviors

- Do not treat a branch as the primary identity of the work.
- Do not store passwords, tokens, or other secrets in the hub.
- Do not copy whole design documents, long logs, or large command outputs into the hub.
- Do not let `portfolio/dashboard.md` become a long narrative; keep it as an action board.
- Do not create a new workstream when the task is just the next step of the same delivery line.
- Do not leave a session without writing `next_step` when meaningful work was performed.

## Resource Guide

- `scripts/ensure-workstream-hub.ps1`: scaffold the hub root on a non-`C:` drive.
- `references/workstream-model.md`: canonical layout, naming, and update rules.
- `assets/templates/hub/workstream-template.md`: template for a new workstream.
- `assets/templates/hub/session-handoff-template.md`: template for a short interruption handoff.
- `assets/templates/hub/project-template.md`: optional stable system-level note template.
