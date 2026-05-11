# Codex Skill Pack

This package contains a portable set of Codex skills adapted for sharing with other users.

It is split into two parts:

- `portable-core`: recommended default install. These skills support maintainable coding, OpenSpec coordination, repo design memory, and skill governance.
- `personal-overlay`: optional install. These skills support machine preflight context and cross-project workstream continuity. They are safe templates now, but recipients should customize their local profiles before relying on them.

## Included Skills

### Portable Core

| Skill | Purpose |
|---|---|
| `design-pattern-engineering` | Maintainability, refactor discipline, pattern selection, code review, compatibility and test gates. |
| `design-spec` | Coordinates OpenSpec phases with design-pattern engineering. |
| `project-design-init` | Initializes repo-local `ai-context/` design memory. |
| `project-design-sync` | Refreshes repo-local `ai-context/` after structural changes. |
| `skill-evolution-governor` | Records and improves skill behavior from real agent successes and failures. |

### Personal Overlay

| Skill | Purpose | Notes |
|---|---|---|
| `preflight-dev-context` | Builds machine, common toolchain, package manager, network, and remote-host awareness before technical work. | Ships with a template profile only. Recipients must fill their own environment facts. |
| `workstream-hub` | Tracks cross-project workstreams, interruptions, and handoffs. | Uses `$CODEX_HUB` when set. |

## Install

From PowerShell at the package root:

```powershell
.\install.ps1 -Package portable-core
```

To install both packages:

```powershell
.\install.ps1 -Package all
```

To install into a non-default Codex home:

```powershell
.\install.ps1 -Package portable-core -CodexHome "D:\codex-home"
```

The installer copies skills into:

```text
<CodexHome>\skills\<skill-name>
```

Default `CodexHome` resolution:

1. `$CODEX_HOME`
2. `$HOME/.codex`

Use `-Force` to overwrite existing skill directories.

## Recommended First Use

After installing `portable-core`, ask Codex:

```text
Use $project-design-init to create ai-context for this repository.
```

For repositories that already use OpenSpec:

```text
Use $design-spec. Phase: explore. Read the relevant openspec change and ai-context before proposing implementation.
```

For code quality reviews:

```text
Use $design-pattern-engineering in review mode. Focus on maintainability, compatibility, and test gaps.
```

## Environment Variables

Optional variables used by the shared skills:

| Variable | Used By | Meaning |
|---|---|---|
| `CODEX_HOME` | installer, multiple skills | Root Codex home directory. |
| `CODEX_SKILL_LAB` | `skill-evolution-governor` | Durable skill evolution ledger root. |
| `CODEX_HUB` | `workstream-hub` | Durable workstream hub root. |
| `CODEX_PRIVATE_HOME` | `preflight-dev-context` | Local-only private data root. |
| `CODEX_PREFLIGHT_CREDENTIAL_FILE` | `preflight-dev-context` | Explicit local-only remote credential file. |

## What Was Removed

This shareable package does not include:

- System skills from `.system/`
- Plugin cache skills
- Private server inventory
- Local credentials
- Machine-specific paths
- Customer/project-specific workstream records

Recipients should customize `preflight-dev-context/references/environment-profile.md` after installation if they use the optional overlay. This does not need to be manual: ask Codex to use `$preflight-dev-context` to inspect the local machine, ask focused questions for unknowns, and update the profile after confirmation.

Example:

```text
Use $preflight-dev-context to initialize my environment profile. Inspect common toolchains, network/proxy state, storage preferences, and remote-host conventions. Ask before recording any uncertain or sensitive information.
```

## Safety Notes

- Do not store credentials in skill files.
- Do not copy private environment profiles into this package.
- Keep `portable-core` broadly reusable; put user-specific behavior in overlay skills.
- If a skill references another skill that is not installed, Codex should fall back gracefully and say what capability is missing.
