---
name: skill-evolution-governor
description: Use this skill when the user wants to improve, review, evolve, or govern their personal Codex skills, especially when deriving better skill behavior from real project experience, failed agent behavior, repeated workflow friction, or plans to later extract a mature framework such as OpenDesign from proven skills.
---

# Skill Evolution Governor

## Overview

Use this skill to turn real project friction into better personal Codex skills without forcing the user to manually maintain a process.

This is a meta-skill. It does not replace domain skills such as `design-pattern-engineering`, `project-design-init`, `project-design-sync`, `workstream-hub`, or `preflight-dev-context`. It governs how those skills improve over time.

The current strategic posture is:
- pure skills are the active experimental runtime
- OpenDesign is the future framework extracted from validated skill behavior
- do not prematurely force active skill lessons back into OpenDesign
- record enough evidence that future framework extraction is based on repeated real cases, not taste

## When To Use

Use this skill when the user asks to:
- improve a personal skill after a project failure or awkward agent behavior
- analyze whether a skill should change
- compare several skill behaviors and find overlap or gaps
- reduce skill bloat, trigger mistakes, or context overload
- create a high-level process for evolving skills efficiently
- decide what should remain in pure skills versus later become OpenDesign
- periodically review the user's skill ecosystem

Do not use this skill for normal project implementation unless the user explicitly asks to improve the skills themselves.

## Operating Principle

Do the governance work for the user.

Prefer making a small, concrete improvement to the skill ecosystem over giving the user a list of chores. If a lesson is clear and low-risk, update the relevant skill or evolution ledger directly. If the lesson is uncertain, record it as an experiment instead of turning it into a rule.

## Canonical Storage

Use a configurable durable evolution workspace:

1. `$CODEX_SKILL_LAB` when set.
2. `$CODEX_HOME/skill-lab` when `$CODEX_HOME` is set.
3. Otherwise, the user's home directory under `.codex/skill-lab`.

Do not assume a particular drive, username, or machine layout.

Expected layout:
- `ledger\cases.md` for real success and failure cases
- `ledger\experiments.md` for rules being tested
- `ledger\decisions.md` for accepted meta-decisions about the skill system
- `ledger\framework-extraction.md` for lessons that may later become OpenDesign
- `scorecards\skill-ecosystem.md` for periodic assessment
- `snapshots\` for optional dated summaries of skill state

If the lab does not exist, create it from `assets/templates/` or by running `scripts/ensure-skill-lab.ps1`. Pass `-Root <path>` when the user wants a specific location.

## Default Workflow

### Step 1: Classify The Signal

Classify the user's issue or observed behavior as one or more failure types:
- `trigger-miss`: the right skill did not activate, or the wrong one did
- `coordination-gap`: multiple skills lacked a clear order or boundary
- `context-miss`: the agent missed important project facts
- `context-overload`: the skill caused too much reading or ceremony
- `scope-creep`: the agent widened the task without enough reason
- `over-abstraction`: the agent introduced structure before pressure justified it
- `under-design`: the agent kept patching when a small seam was needed
- `compat-break`: compatibility, rollout, or public contract risk was missed
- `test-gap`: verification expectations were too weak or unclear
- `sync-gap`: project design memory was not initialized or updated correctly
- `handoff-gap`: cross-session or cross-project continuity failed
- `output-gap`: the final response did not expose the useful decision trail
- `framework-candidate`: repeated behavior looks mature enough for future OpenDesign

### Step 2: Decide The Action Level

Choose the smallest useful action:
- `log`: record one case only
- `experiment`: add a tentative rule to test in future work
- `patch`: update one skill with a clear low-risk behavior improvement
- `coordinate`: clarify boundaries or order between two or more skills
- `extract-candidate`: mark a repeated proven rule for future OpenDesign
- `defer`: record why no change should be made yet

Do not patch a skill from a single ambiguous case unless the risk of the patch is low.

### Step 3: Inspect Only Relevant Skills

Read only the SKILL.md files and references needed for the signal. Common targets:
- trigger or maintainability behavior: `design-pattern-engineering`
- OpenSpec coordination: `design-spec`
- repo-local design memory creation: `project-design-init`
- repo-local design memory refresh: `project-design-sync`
- cross-project continuity: `workstream-hub`
- environment and machine context: `preflight-dev-context`

### Step 4: Update The Lab

Always leave a durable trace for meaningful governance work:
- append a short case to `ledger\cases.md` when the signal came from a real task
- append or update `ledger\experiments.md` when testing a new rule
- append `ledger\decisions.md` when accepting a durable meta-rule
- append `ledger\framework-extraction.md` only when the lesson looks stable across cases

Keep entries short. The lab is an evidence trail, not a second documentation system.

### Step 5: Patch Skills When Worth It

When editing skills:
- preserve concise skill bodies and progressive disclosure
- prefer changing trigger descriptions, decision rules, stop conditions, and output contracts over adding long explanations
- move detailed taxonomies or examples into references
- avoid duplicating the same rule across many skills; put orchestration rules here when possible
- keep OpenDesign references as future extraction candidates, not active authority, unless the user explicitly requests framework work

### Step 6: Report The Result

For substantial work, report:
- signal classified
- action taken
- files changed
- framework extraction candidate, if any
- next automatic trigger to watch

## Periodic Review Mode

When the user asks for a high-level review of the skill system:
1. read current personal skill names and descriptions
2. read the latest lab ledgers and scorecard
3. identify repeated failure clusters
4. propose or apply the smallest set of skill patches
5. update `scorecards\skill-ecosystem.md`

Default review cadence is case-driven, not calendar-driven. Do not create automation unless the user asks.

## Output Contract

Use this concise shape when applicable:

```text
Skill evolution update:
- Signal: <failure types>
- Action: <log|experiment|patch|coordinate|extract-candidate|defer>
- Updated: <files or none>
- OpenDesign candidate: <yes/no + reason>
- Watch next: <what future project behavior should confirm or reject>
```
