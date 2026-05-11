# Quick Routing

Use this reference when context is limited and you need the fastest safe path through the skill.

## Primary Goal

Identify the task mode first, then load only the minimum guidance needed to act safely.

## Short-Context Rule

Start with `task-modes.md`, then load at most two more references unless the task clearly spans multiple concerns.

## Step 1: Pick The Mode

- new feature or new variant -> `task-modes.md` section `feature`
- structural cleanup while preserving behavior -> `task-modes.md` section `refactor`
- urgent correctness or production fix -> `task-modes.md` section `hotfix`
- design review or readiness judgment -> `task-modes.md` section `review`

## Step 2: Add The Next One Or Two References

If the main problem is:

- understanding project-specific rules before coding
  - read `repo-context-loading.md`
  - if `ai-context/` exists, start with `ai-context/sync-status.md` and the nearest module doc
  - if `ai-context/repo-layout.json` exists, use it to find declared source roots and multi-path modules before guessing from folders
  - trust the `High-Confidence Evidence` section first, then decide which heuristic clues deserve code inspection
  - then `repo-local-context-fallback.md` only if repo-local docs are absent

- deciding whether to reshape now or defer
  - read `refactor-defer-matrix.md`

- figuring out mandatory tests for the current structural move
  - read `test-obligation-matrix.md`

- explicitly choosing a design pattern
  - read `pattern-selection.md`
  - then `classic-gof-patterns.md` or `modern-patterns.md`

- adapting the chosen pattern to the current language without a separate playbook
  - read `language-mapping.md`

- growing branches, provider variation, or rule dispatch
  - read `pattern-selection.md`
  - then `classic-gof-patterns.md` for local refactors or `modern-patterns.md` for broader seams

- local refactor in a legacy or shared module
  - read `change-budget-and-safety.md`
  - then `legacy-migration-playbook.md`

- business rules are scattered or primitive-heavy
  - read `domain-modeling-patterns.md`

- React component sprawl, hook confusion, or state placement issues
  - read `react-component-architecture.md`

- TypeScript or Node service structure
  - read `typescript-node-service.md`

- FastAPI or Python service orchestration
  - read `python-fastapi-services.md`

- Spring or Java service modularity
  - read `java-spring-modularity.md`

- final review, design critique, or ship/no-ship decision
  - read `code-review-checklist.md`
  - then `self-evaluation-scorecard.md`

- deciding whether changed implementation should refresh `ai-context/`
  - read `project-design-sync-triggers.md`
  - then `context-refresh-rules.md`

- competing priorities or contradictory guidance
  - read `conflict-resolution.md`

- production safety, performance, security, or concurrency concerns
  - read `nonfunctional-guardrails.md`

- uncertainty about whether to keep things simpler
  - read `anti-patterns.md`
  - then `anti-examples-zh-en.md`

## Minimal Starter Packs

Good three-file max starting packs:
- feature + repo fit -> `task-modes.md` + `repo-context-loading.md` + one framework reference
- feature + repo fit with `ai-context/` present -> `task-modes.md` + `repo-context-loading.md` + nearest `ai-context/modules/*.md`
- feature + explicit pattern choice -> `task-modes.md` + `pattern-selection.md` + one of `classic-gof-patterns.md` or `modern-patterns.md`
- feature + pattern choice + language note -> `task-modes.md` + `pattern-selection.md` + `language-mapping.md`
- feature + new variation seam -> `task-modes.md` + `pattern-selection.md` + `test-obligation-matrix.md`
- refactor + safety -> `task-modes.md` + `change-budget-and-safety.md` + `refactor-defer-matrix.md`
- refactor + legacy module -> `task-modes.md` + `change-budget-and-safety.md` + `legacy-migration-playbook.md`
- hotfix + confidence -> `task-modes.md` + `test-obligation-matrix.md` + `conflict-resolution.md`
- review + verdict -> `task-modes.md` + `code-review-checklist.md` + `self-evaluation-scorecard.md`
- review + `ai-context/` refresh decision -> `task-modes.md` + `project-design-sync-triggers.md` + `context-refresh-rules.md`

## Stop Loading More References When

- the mode is clear
- compatibility and test obligations are clear
- one shape decision is clear enough to implement
- extra reading would not change the next action
