# Repo-Local Context Fallback

Use this reference when the repository has no durable context system but still benefits from lightweight project memory.

## Primary Goal

Provide a lightweight project-memory structure without requiring a heavy documentation workflow.

## Preferred Fallback Structure

If the repository maintains local context, the most useful files are:
- `ai-context/project.md`
- `ai-context/architecture.md`
- `ai-context/conventions.md`
- `ai-context/hotspots.md`
- `ai-context/nonfunctional.md`
- `ai-context/capabilities/*.md`
- `ai-context/patterns/preferred.md`
- `ai-context/patterns/anti-patterns.md`

## Minimum Useful Set

If only a few files exist, prioritize:
- `project.md` for overall architecture and project rules
- `architecture.md` for boundaries and dependency direction
- one capability doc that matches the current task

## What Each File Should Capture

`project.md`
- tech stack
- architecture style
- naming and testing conventions
- compatibility constraints

`architecture.md`
- module boundaries
- dependency rules
- extension seams
- hotspots to avoid widening casually

`hotspots.md`
- fragile or high-risk areas
- migration constraints
- operationally sensitive code paths

`capabilities/*.md`
- domain vocabulary
- behavior rules
- invariants and known edge cases

## Usage Rule

Read the closest maintained local context first.

Do not create a full folder of docs unless the repository is actually maintaining them. When no such docs exist, infer carefully and keep the project profile lightweight.
