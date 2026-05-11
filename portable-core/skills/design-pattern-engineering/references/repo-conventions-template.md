# Repo Conventions Template

Use this reference to build a lightweight repository profile before proposing structural changes in a medium or large codebase.

## Primary Goal

Adapt good design decisions to the local repository instead of importing a foreign architecture style.

## How To Use This File

Do not create a new documentation file unless the user asks. Use this template as:
- an internal checklist
- a short summary in your design intent
- a mental profile of how the repository already works

## Lightweight Repo Profile

Capture the following:

### 1. Structural Style

- Is the repo grouped by layer, feature, package, or service?
- Where do business rules normally live?
- What kinds of modules already act as seams: services, hooks, ports, adapters, strategies, handlers?

### 2. Naming Style

- How are files, classes, functions, and modules named?
- Are domain terms explicit or hidden behind technical names?
- Which generic names are already overloaded and should be avoided?

### 3. Dependency Rules

- Which directions are normal and accepted?
- Are there existing boundaries around transport, persistence, or SDK code?
- Are there forbidden or discouraged cross-layer imports?

### 4. Testing Style

- What kinds of tests are common here: unit, integration, contract, snapshot, end-to-end?
- Where do characterization tests belong?
- How much mocking is typical and acceptable?

### 5. Data And Contract Style

- How are DTOs, entities, value objects, and persistence models separated?
- Which public contracts are treated as stable?
- How does the repo handle schema evolution and migration safety?

### 6. Operational Style

- Are feature flags, phased rollouts, or migration shims already common?
- What observability patterns exist?
- Are there hot paths or high-risk modules with stricter change expectations?

## Decision Rules

Prefer:
- matching the local style when it is coherent and maintainable
- improving the current design from the inside rather than replacing its vocabulary
- introducing new patterns only where local style has a clear gap

Do not:
- rename everything just to match textbook terminology
- fight established structure during a local feature request
- assume the absence of a pattern means the team rejected it; inspect first

## When Local Conventions Are Weak

If the repository is inconsistent:
- preserve the stable parts
- improve the touched area with the smallest clear step
- explain the local inconsistency in your design review
- separate broader cleanup ideas from the current implementation
