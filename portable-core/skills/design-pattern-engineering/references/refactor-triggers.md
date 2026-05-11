# Refactor Triggers

Use this reference while coding. If one or more triggers appear, pause feature work and reassess the structure before continuing.

If the code is legacy, shared, or operationally risky, pair this file with `references/legacy-migration-playbook.md` before making wide structural moves.

## Trigger Categories

## 1. Duplication Pressure

Refactor when:
- the same business rule appears a second time
- two modules differ only by provider names, constants, or mapping tables
- a new feature is easiest to build by copying an older feature and editing details

Preferred responses:
- extract a shared domain concept
- extract `Strategy` or polymorphic behavior
- extract a shared workflow component or use-case

## 2. Branch Explosion

Refactor when:
- a function keeps growing `if/else`, `switch`, or pattern-matching branches
- each new variant requires editing the same conditional hub
- behavior varies by mode, type, channel, state, or environment

Preferred responses:
- use `Strategy`, `State`, or dispatch by collaborator
- move per-variant behavior next to the variant itself
- keep the orchestrator small and declarative

## 3. Responsibility Drift

Refactor when:
- one module validates input, coordinates dependencies, applies business rules, and persists data
- a controller or handler becomes the real application layer
- a class gains several reasons to change

Preferred responses:
- split domain logic from orchestration
- extract application service, domain service, or repository boundary
- rename modules around real responsibilities

## 4. Dependency Tangling

Refactor when:
- a core business module imports framework, transport, and persistence concerns directly
- testing requires too many integration dependencies for a simple rule
- the dependency graph points inward from infrastructure into core logic

Preferred responses:
- introduce ports, repositories, adapters, or facades
- invert dependencies so core logic speaks to stable interfaces
- isolate SDK and ORM details in edge modules

## 5. Naming Breakdown

Refactor when:
- names like `Helper`, `Manager`, `Processor`, or `CommonUtils` become the default escape hatch
- methods need long comments because names do not communicate intent
- a single file stores multiple unrelated concepts under a vague label

Preferred responses:
- model the underlying concept explicitly
- split generic modules by purpose
- rename around business language, not implementation trivia

## 6. Change Friction

Refactor when:
- one requirement change touches many unrelated files
- adding a variant requires editing existing tested code in multiple places
- simple changes feel risky because behavior is not localized

Preferred responses:
- create extension seams
- move policy decisions into replaceable collaborators
- consolidate behavior behind one clear entry point
- use phased migration tactics instead of rewriting everything at once

## 7. Readability Collapse

Refactor when:
- functions become long enough that the reader loses the high-level flow
- nested blocks hide the main business path
- boilerplate overwhelms the intent

Preferred responses:
- extract named steps
- separate orchestration from detail work
- move translations and mapping code to dedicated helpers or adapters

## Practical Thresholds

These are heuristics, not laws. Reassess when you see any of the following:
- one concept implemented in three or more places
- one function handling three or more distinct responsibilities
- one module depending on many unrelated collaborators
- the second variant of a feature arriving soon after the first
- test setup becoming more complex than the behavior under test

## Legacy Migration Tactics

When the right shape is clear but the code cannot be changed safely in one pass, prefer one of these:
- `branch-by-abstraction` to move callers gradually behind a stable seam
- `compatibility adapter` to preserve old contracts while improving internal structure
- `deprecation shim` to retire old entrypoints without breaking callers immediately
- `strangler seam` to replace one slice of a large legacy module at a time
- `feature-flagged cutover` when rollback simplicity matters

Choose the smallest tactic that preserves compatibility and keeps the migration reversible.

## Anti-Reaction Warning

Do not answer every trigger with a heavy pattern. Sometimes the right refactor is only:
- extracting one function
- renaming a module
- moving a mapping table
- splitting transport code from business code
- creating one interface at a clear seam

The goal is to restore clarity and changeability with the smallest credible move.
