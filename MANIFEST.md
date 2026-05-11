# Skill Pack Manifest

## Package Name

`codex-skill-pack`

## Intended Audience

Developers who use Codex for sustained software engineering work and want:

- OpenSpec-aware change flow
- repo-local design memory through `ai-context/`
- maintainability-focused code review and refactoring guidance
- optional cross-project workstream continuity

## Install Sets

### `portable-core`

Install by default.

```text
portable-core/skills/design-pattern-engineering
portable-core/skills/design-spec
portable-core/skills/project-design-init
portable-core/skills/project-design-sync
portable-core/skills/skill-evolution-governor
```

Dependencies:

- No private files required.
- `design-spec` works best when a repository has `openspec/`.
- `project-design-init` and `project-design-sync` create or refresh `ai-context/`.

### `personal-overlay`

Install only when the recipient wants the extra workflows.

```text
personal-overlay/skills/preflight-dev-context
personal-overlay/skills/workstream-hub
```

Dependencies:

- `preflight-dev-context` is a template until the recipient initializes `references/environment-profile.md`. The recipient can ask Codex to do this interactively with `$preflight-dev-context`; it should inspect the machine, ask focused questions, and write only confirmed non-secret facts.
- `workstream-hub` creates a new hub root; it does not include any personal records.

## Distribution Checklist

Before sharing this folder:

- Run a privacy scan for local absolute paths, private IP ranges, credentials, tokens, customer names, and internal hostnames.
- Confirm no private environment profile was copied in.
- Confirm no `skills/.system` or plugin cache directory was included.
- Confirm recipients know whether they should install `portable-core` only or `all`.

## Version Notes

This package is a shareable snapshot. The skills are expected to evolve through `skill-evolution-governor` as real usage reveals trigger, context, or output gaps.
