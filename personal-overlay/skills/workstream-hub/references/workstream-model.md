# Workstream Hub Model

## Root Layout

Default root resolution:

1. `$CODEX_HUB`
2. `$CODEX_HOME/workstream-hub`
3. `$HOME/.codex/workstream-hub`

```text
<hub-root>\
  portfolio\
    dashboard.md
    inbox.md
  workstreams\
    <workstream-id>.md
  sessions\
    YYYY-MM-DD\
      HHmm-<workstream-id>.md
  projects\
    <system>.md
```

Use the user's preferred durable storage location when they provide one.

## What Each Layer Stores

- `portfolio/dashboard.md`: the user's global action board
- `portfolio/inbox.md`: quick capture for items that are not triaged yet
- `workstreams/*.md`: one file per real delivery line
- `sessions/YYYY-MM-DD/*.md`: short interruption or handoff notes
- `projects/*.md`: optional stable system notes such as repo path, branch conventions, design doc root, or release entry points

This hub is not a substitute for repo-local design docs. Keep implementation detail, architecture detail, and interface detail in the repo itself.

## Workstream Identity Rules

Use one workstream for one meaningful delivery line. Split workstreams when any of these become independent:
- customer or tenant target
- release or acceptance path
- branch family
- blocking chain
- delivery goal
- bugfix versus feature track

Good IDs:
- `acme-mobile-checkout-feature`
- `acme-prod-login-hotfix`
- `research-app-data-sync-investigation`
- `platform-billing-api-migration`

Bad IDs:
- `project`
- `bugfix`
- `today-task`
- `branch-feature-123`

## Dashboard Rules

Keep `portfolio/dashboard.md` small and action-oriented:
- active workstreams
- paused or interrupted workstreams
- blocked or waiting items
- today's top priorities
- recent switches

Every line should either name a workstream or point to the next action. Do not turn the dashboard into a meeting log.

## Workstream File Contract

Each workstream file should use YAML front matter plus short markdown sections.

Recommended fields:

```yaml
---
id: acme-mobile-checkout-feature
system: acme-mobile
repo: /path/to/repo
customer: Acme
type: feature
status: active
priority: P1
branches:
  - feature/checkout-adjustments
envs:
  - pred
related_items:
  - req-1234
current_goal: Finish checkout delivery adjustments
current_focus: Wire the new checkout field through the edit form
next_step: Verify edit-mode replay with staging data before pushing
blockers: []
risks:
  - Parallel customer work in the same repo can cause branch bleed
last_updated: 2026-04-24 14:30
---
```

Recommended body sections:
- `Why this workstream exists`
- `Current notes`
- `Decisions`
- `Links`

Keep the body concise. Long implementation notes belong in the repo.

## Session Handoff Contract

Each handoff note should be short enough to scan in under one minute.

Template:

```text
# 2026-04-24 14:45 - acme-mobile-checkout-feature

- Done:
- Pending:
- Next:
- Blockers:
- Risk:
- Resume path / command:
```

Write a new handoff when:
- the user switches to another task
- the user leaves mid-debug
- a bugfix interrupts feature work
- a session ends before the next step is obvious from the workstream file alone

## Optional Project Notes

Use `projects/<system>.md` only for stable cross-workstream notes such as:
- repo path
- common branch naming rules
- design doc root such as `ai-context/`
- release entry points
- shared deployment caveats

Do not duplicate the same data across every workstream if it is truly system-wide and stable.
