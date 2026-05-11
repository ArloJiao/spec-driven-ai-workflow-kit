# Usage Examples

## Initialize Design Memory

```text
Use $project-design-init for this repository. Create ai-context with current implementation facts. Keep it concise and mark uncertain areas as needing review.
```

## Work In An OpenSpec Repository

```text
Use $design-spec.
Phase: proposal.
Change: openspec/changes/<change-id>

Read only:
- openspec/project.md
- openspec/changes/<change-id>/proposal.md
- openspec/changes/<change-id>/design.md if present
- ai-context modules relevant to the touched area
- code and tests in the touched area

Produce:
- chosen design
- compatibility boundary
- test plan
- rejected alternatives
```

## Apply An OpenSpec Change

```text
Use $design-spec.
Phase: apply.
Change: openspec/changes/<change-id>

Implement tasks.md in order. If code differs from proposal assumptions, report drift before broadening scope. Update tasks.md and recommend $project-design-sync if module boundaries changed.
```

## Maintainability Review

```text
Use $design-pattern-engineering in review mode.
Focus on bugs, maintainability risks, compatibility risks, and missing tests. Findings first, ordered by severity, with file/line references.
```

## Refresh Design Memory After A Refactor

```text
Use $project-design-sync. Refresh ai-context for the modules changed in the last commit. Preserve high-confidence evidence and mark heuristic conclusions separately.
```

## Record A Skill Behavior Lesson

```text
Use $skill-evolution-governor.
Classify this agent failure, update the skill lab if appropriate, and suggest the smallest skill patch or experiment.
```

## Optional Preflight Context

Before using `preflight-dev-context`, edit:

```text
<CodexHome>/skills/preflight-dev-context/references/environment-profile.md
```

You can ask Codex to do the initialization:

```text
Use $preflight-dev-context to initialize my environment profile. Inspect common toolchains, network/proxy state, storage preferences, and remote-host conventions. Ask before recording any uncertain or sensitive information.
```

Then prompt:

```text
Use $preflight-dev-context before starting this toolchain/server/debugging task. Build a 5-10 bullet working summary, then proceed.
```

## Optional Workstream Hub

Set a hub root if desired:

```powershell
$env:CODEX_HUB = "<path-to-your-workstream-root>"
```

Then prompt:

```text
Use $workstream-hub to resume the relevant workstream, update the handoff notes, and then continue the repo task.
```
