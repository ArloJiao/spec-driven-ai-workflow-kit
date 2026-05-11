---
name: design-pattern-engineering
description: Use this skill when implementing, refactoring, or reviewing code that must stay maintainable in a growing codebase. It helps the agent fit the existing repository, choose the lightest justified abstractions, name concrete classic or modern pattern candidates when useful, keep refactors inside scope, protect behavior with tests, and surface larger redesigns separately.
---

# Design Pattern Engineering

## Overview

Use this skill to keep code maintainable while it is being written, not after the fact.

This skill works even when a repository has no dedicated context system or spec workflow. When repo-local design docs do exist, treat them as high-value context that sharpens decisions instead of as hard prerequisites.

The goal is not to force patterns everywhere. The goal is to:
- fit the existing codebase before inventing structure
- choose the lightest abstraction that improves the next likely change
- name concrete pattern candidates when a classic or modern pattern really fits
- keep refactors inside the user's scope and compatibility budget
- protect structural edits with tests
- record larger redesigns separately instead of smuggling them into local work

## When To Use This Skill

Use this skill when the user asks for any of the following:
- implement a feature that should remain easy to extend
- refactor AI-generated or fast-written code that is getting brittle
- review code for maintainability, modularity, or design-pattern quality
- reduce branching, duplication, mixed responsibilities, or poor seams
- improve a shared module without breaking compatibility
- add business rules that are likely to grow in number or variation

Do not use this skill for tiny throwaway scripts with no likely evolution.

## First Decision

Start by selecting the task mode in `references/task-modes.md`:
- `feature` for new behavior or a new variant
- `refactor` for structural improvement while preserving behavior
- `hotfix` for urgent correctness or production-risk repair
- `review` for design critique, maintainability review, or readiness judgment

The mode determines how aggressive the design work should be, which safety gates are mandatory, and which references to load first.

## Core Operating Rules

Always work from these rules:
- repository fit beats greenfield neatness
- compatibility beats cleanup unless the user explicitly approves breakage
- the smallest useful seam beats broad redesign
- pattern pressure beats pattern collecting
- tests move with behavior
- when rules conflict, choose the safer, more local, more reversible step

Use `references/conflict-resolution.md` whenever design quality, delivery pressure, repo conventions, or framework idioms pull in different directions.

## Default Workflow

### Step 1: Read the local architecture before designing

Before choosing patterns or splitting modules, inspect:
- existing module layout, naming style, dependency direction, and extension seams
- public APIs, persistence contracts, schemas, and rollout assumptions that must remain stable
- tests that currently define behavior
- repo-local design docs, if they exist

Prefer repository context in this order:
1. `ai-context/sync-status.md` to judge freshness when `ai-context/` exists
2. `ai-context/repo-layout.json` when it exists, to understand declared source roots, module mappings, and design sources
3. `ai-context/project.md`, `ai-context/architecture.md`, and the nearest `ai-context/modules/*.md` for the touched area
4. `ai-context/interfaces.md`, `ai-context/runtime.md`, `ai-context/hotspots.md`, and `ai-context/decisions.md` when the task touches those concerns
5. the closest maintained project context docs for the affected area
6. other local context folders or project guidance such as `project-context/`, capability notes, or architecture docs
7. project architecture, contributor, or ADR-style docs
8. inferred repo profile from `references/repo-conventions-template.md`

Use `references/repo-context-loading.md` and `references/repo-local-context-fallback.md` only as needed. Do not load every reference by default.

If `ai-context/` exists but `sync-status.md` is stale, missing, or low-confidence, use the docs as hints and verify critical decisions from code and tests before trusting them.

When reading any `ai-context/*.md` file:
- consume `High-Confidence Evidence` first for file, module, entrypoint, and test facts
- use `Heuristic Signals` as prompts for where to inspect next, not as final architectural truth
- treat `Needs Human Review` as explicit caution tape around contracts, boundaries, and design intent

### Step 2: Set the scope, compatibility, and test gates

Before structural edits, decide:
- what behavior and contracts must remain unchanged
- whether the task justifies refactoring now, deferring it, or merely recording it
- which tests must exist before or during the change

Required references for this decision:
- `references/change-budget-and-safety.md`
- `references/refactor-defer-matrix.md`
- `references/test-obligation-matrix.md`

Default posture:
- keep refactors local to the requested task
- preserve public behavior and integration contracts by default
- use characterization tests before structural edits in unclear legacy areas
- if the best design exceeds the safe budget, take the smallest safe step now and surface the larger redesign separately

### Step 3: Choose the lightest useful shape

Use `references/pattern-selection.md` to decide whether a pattern is justified.

If a pattern is justified, explicitly shortlist one to three candidates:
- use `references/classic-gof-patterns.md` for the 23 classic GoF patterns
- use `references/modern-patterns.md` for current application, domain, integration, and architecture patterns
- use `references/domain-modeling-patterns.md` when business rules, invariants, or domain vocabulary are the real pressure
- use `references/architecture-patterns.md` when module boundaries or system seams are changing
- use `references/language-mapping.md` to express the chosen pattern idiomatically in the current language instead of expecting a separate per-language playbook

Then choose one of these outcomes:
- one classic pattern
- one modern pattern
- a combination of one local pattern plus one broader system pattern
- no named pattern when a simpler function, module split, or narrow seam is enough

Prefer functions, composition, explicit names, and narrow seams before introducing multi-layer hierarchies.

### Step 4: Build and reshape in-loop

Do not postpone all design work until after the feature is finished.

While implementing, continuously scan for pressure from `references/refactor-triggers.md`. If the current shape starts to harden into duplication, branching sprawl, mixed responsibilities, awkward object creation, or painful test setup, pause and reshape inside the current budget.

When the area is legacy, shared, or operationally sensitive:
- use `references/legacy-migration-playbook.md` for branch-by-abstraction, shims, phased seams, and safe cutovers
- use `references/nonfunctional-guardrails.md` for latency, concurrency, observability, security, and rollback concerns

### Step 5: Review the result and choose the right ending

Before concluding substantial work:
- run `references/code-review-checklist.md`
- score the result with `references/self-evaluation-scorecard.md`
- if the repo keeps local design docs, use `references/context-refresh-rules.md`, `references/project-design-sync-triggers.md`, and `references/project-design-doc-lifecycle.md` to decide whether they must be updated

The ending should match the evidence:
- finish normally when scope, compatibility, tests, and local fit are solid
- finish with explicit follow-ups when the code is safe now but broader redesign remains
- if the task introduced or materially changed one module and its detailed design doc is missing, blank, or stale, update that module doc in the same task
- if `ai-context/` exists and structure, interfaces, runtime flow, or tracked module boundaries changed materially, recommend refreshing it through `$project-design-sync` instead of hand-overwriting generated sections
- do not declare success when compatibility or test protection is unverified

## Reference Map

Load only the references needed for the task.

- routing and mode selection
  - `references/quick-routing.md`
  - `references/task-modes.md`
  - `references/conflict-resolution.md`
- pattern selection and shape
  - `references/pattern-selection.md`
  - `references/classic-gof-patterns.md`
  - `references/modern-patterns.md`
  - `references/language-mapping.md`
  - `references/refactor-triggers.md`
  - `references/architecture-patterns.md`
  - `references/domain-modeling-patterns.md`
  - `references/anti-patterns.md`
  - `references/anti-examples-zh-en.md`
- scope, tests, and migration safety
  - `references/change-budget-and-safety.md`
  - `references/refactor-defer-matrix.md`
  - `references/test-obligation-matrix.md`
  - `references/legacy-migration-playbook.md`
  - `references/nonfunctional-guardrails.md`
- repository context
  - `references/repo-context-loading.md`
  - `references/repo-local-context-fallback.md`
  - `references/repo-conventions-template.md`
  - `references/context-refresh-rules.md`
  - `references/project-design-sync-triggers.md`
  - `references/project-design-doc-lifecycle.md`
- stack-specific guidance
  - `references/typescript-node-service.md`
  - `references/react-component-architecture.md`
  - `references/python-fastapi-services.md`
  - `references/java-spring-modularity.md`
- review and verdict
  - `references/code-review-checklist.md`
  - `references/self-evaluation-scorecard.md`
  - `references/worked-examples-zh-en.md`

If context is limited, start with `references/quick-routing.md` and load at most two more references.

## Visible Output By Mode

For substantial tasks, adapt the visible output to the mode:
- `feature`: design intent, pattern candidates or explicit no-pattern decision, chosen seam, safety plan, implementation notes, follow-up risks
- `refactor`: current pain, pattern candidates if structural pressure is real, compatibility boundary, structural move taken now, tests protecting behavior, deferred cleanup
- `hotfix`: failure being contained, smallest safe change, regression test, optional narrow pattern move only if it directly reduces risk, deferred design debt if any
- `review`: findings first, then pattern candidates or simpler alternatives, then the smallest recommended next move

When a pattern decision matters, make it explicit:
- `Pattern candidates`
- `Chosen pattern` or `No named pattern`
- `Why this fits`
- `Language note`
- `Why simpler or heavier alternatives were rejected`

Keep small tasks lightweight, but keep the same decision logic internally.

## Non-Negotiable Behaviors

- Do not optimize only for immediate feature completion.
- Do not impose greenfield architecture on a mature codebase without checking local conventions first.
- Do not broaden refactors beyond the user's likely scope unless that expansion is made explicit.
- Do not break public contracts, persistence assumptions, or rollout expectations by accident.
- Do not move or redistribute important behavior without adding or updating tests that protect it.
- Do not hide behind vague design language when a concrete pattern candidate is the real decision.
- Do not let naming drift into vague buckets like `Helper`, `Manager`, or `Utils` when a stronger domain concept exists.
- Do not leave repeated business rules scattered across handlers, services, and persistence code.
- Do not keep adding branches when the second or third variation clearly wants a seam.
- Do not trade runtime safety, security, or observability for cleaner structure.
- Do not let generic skill guidance outrank repository-specific docs without a clear reason.

## Trigger Phrases And Mini-Recipes

Common English triggers:
- "Implement this in a maintainable way and use design patterns only where justified."
- "Refactor this service so new providers can be added safely."
- "Review this AI-generated code for architecture and readability issues."
- "Keep the refactor local, preserve compatibility, and protect it with tests."
- "List the candidate design patterns before choosing one."

常见中文触发语:
- "请先理解现有项目结构，再决定是否引入设计模式。"
- "请在不破坏现有接口和兼容性的前提下重构这段代码。"
- "这个模块要边写边抽象，但改动范围请控制在当前需求内。"
- "重构时请补齐测试，确保业务行为不回归。"
- "请先列出候选设计模式，再说明最终为什么选这个。"

Mini-recipes:
- TypeScript or Node: provider-specific `if/else` growth -> `Strategy` plus a stable service interface, or `Plugin Registry` if providers are loaded as extensions
- React: page mixes data fetching, state orchestration, and rendering rules -> feature hook plus smaller boundary components, optionally a `Container-Presenter` split if the screen is getting noisy
- FastAPI or Python service: route owns validation, policy, and I/O orchestration -> thin route plus `Application Service` and `Adapter` or `Port`
- Spring or Java: transaction flow and business policy tangled in one service -> `Application Service` plus extracted `Policy`, `Specification`, or `Strategy`

中文迷你配方:
- TypeScript/Node: `if/else` 里不断追加 provider 分支 -> 用 `Strategy` 包住差异, 如果是扩展式加载再考虑 `Plugin Registry`
- React: 页面同时处理请求、状态编排和渲染规则 -> 拆成 feature hook 和边界清晰的组件, 复杂页面可考虑 `Container-Presenter`
- FastAPI/Python: 路由里混着校验、业务规则和 I/O -> 路由变薄, 业务进入 `Application Service`, 外部依赖落到 `Adapter` 或 `Port`
- Spring/Java: 事务流程和业务策略缠在一个 service -> 保留应用服务编排, 抽离 `Policy`、`Specification` 或 `Strategy`

For more bilingual before/after examples, use `references/worked-examples-zh-en.md`.

## Working Style

Be pragmatic and in-loop.

A good outcome looks like this:
- the next likely change is more obvious than before
- the touched area fits the existing repository better, not worse
- the code gained one or two clear seams instead of a mini-framework
- the chosen pattern is explicit and justified, or clearly rejected as unnecessary
- tests now protect the moved or newly isolated behavior
- larger redesign ideas are captured without destabilizing today's work

A bad outcome looks like this:
- more files and interfaces but no real reduction in complexity
- a hotfix that quietly rewrites a subsystem
- design decisions that ignore the repository's own conventions
- abstractions chosen by name rather than by pressure
- a "cleaner" structure that removed behavioral confidence
