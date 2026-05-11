---
name: preflight-dev-context
description: Build cross-project awareness of the user's development environment before coding, debugging, automation, deployment, package installation, language toolchain work, network troubleshooting, or remote-server work. Use at the start of technical tasks when Codex should understand the local machine, common toolchains such as Python/JVM/Android/Node/Go/Rust/.NET, network reachability, storage constraints, and the user-maintained environment profile.
---

# Preflight Dev Context

## Quick Start

1. Read `references/environment-profile.md` first.
2. If a local credential file is configured and the task needs password-based server access, read it after the environment profile.
3. For quick server lookup by alias, short host number, or address fragment, run `scripts/resolve-server-alias.ps1 -Query <value>`.
4. If the task depends on current machine, language runtime/toolchain, package manager, build system, network, SSH, VPN, or server state, run `scripts/collect-dev-context.ps1`.
5. Merge durable facts from the profile, local-only credential hints, and live facts from the script into a 5-10 bullet working summary before taking action.
6. Base tool choice, runtime/interpreter choice, install strategy, build command, and server targeting on that summary.
7. If a stable fact is missing, ask a focused question and offer to update the profile or the local credential file after the user confirms it.

For first-time setup, help the user initialize the profile instead of expecting them to fill it manually:

1. Run `scripts/collect-dev-context.ps1`.
2. Summarize detected toolchains, storage policy clues, network/proxy state, and remote-host clues.
3. Ask focused questions for stable preferences that cannot be inferred, such as preferred cache roots, language version managers, Android SDK location, VPN requirements, and whether remote-host aliases should be recorded.
4. Update `references/environment-profile.md` only with confirmed non-secret facts.
5. Keep credentials, tokens, private keys, customer secrets, and one-off transient failures out of the shared profile.

## Top-Level Constraint

- Treat user-stated storage constraints as defaults for all work, not just Python.
- Prefer workspaces, caches, virtual environments, downloads, generated assets, logs, datasets, and temporary files in the user's preferred project or cache locations whenever practical.
- If a tool defaults to a constrained location, look for a safe override before proceeding.
- If constrained-location usage is unavoidable, keep it minimal and mention it briefly in the working summary before large operations.

## Workflow

### Load durable context

- Treat `references/environment-profile.md` as the cross-project source of truth for stable facts.
- Prefer the profile for server purpose, access method, ownership, mirrors, and recurring caveats.
- Keep credentials, tokens, and secrets out of the skill files and the shared profile.
- Local-only plaintext server credentials may live at the path selected by `$CODEX_PREFLIGHT_CREDENTIAL_FILE`, or under `$CODEX_PRIVATE_HOME/preflight-dev-context/server-credentials.local.json`.
- Use that local credential file only for actual connection work or when a password-auth host is in scope. Do not paste its secret values into routine summaries unless the user explicitly asks.
- For fast operator workflow, use `scripts/resolve-server-alias.ps1` to resolve configured host aliases into address, user, root mode, and purpose. The script reports whether secrets exist but does not print them unless `-IncludeSecrets` is explicitly passed for a task that truly needs them.

### Refresh live context

Run `scripts/collect-dev-context.ps1` whenever the task touches any of the following:
- Python interpreter or environment selection
- Java, Kotlin, Gradle, Maven, Android SDK, or ADB
- Node.js, npm, pnpm, yarn, bun, or deno
- Go, Rust, .NET, Docker, Kubernetes, or database CLIs
- package installs or dependency repair
- build tools or generated artifacts
- network troubleshooting
- intranet or VPN access
- SSH, remote shells, or internal servers
- OS-specific behavior on the local workstation

The script is the live snapshot. The profile is the durable memory. Do not confuse them.

### Build a working summary

Capture the minimum facts needed to act safely:
- machine and shell baseline
- relevant runtime and package-manager entry points
- relevant environment variables such as `JAVA_HOME`, `ANDROID_HOME`, `GOPATH`, `CARGO_HOME`, `NODE_OPTIONS`, or `DOCKER_HOST`
- active network path and proxy state
- intranet clues such as VPN, SSH aliases, and known servers
- whether a local credential file exists for the target host
- blockers, unknowns, and assumptions

State clearly when a claim is inferred from current evidence rather than confirmed by the user.

### Act with environment awareness

- Treat the user's storage policy as a global operating preference across coding, builds, package installs, archives, generated outputs, and local tooling.
- On Windows, prefer the runtime and package entry points that the environment profile recommends.
- For Python work, use the profile's preferred workflow; if none exists, prefer the least invasive project-local option.
- For JVM/Android work, check `JAVA_HOME`, Gradle wrapper presence, Android SDK variables, and ADB availability before changing build settings.
- For Node work, check lockfiles and package-manager markers before installing dependencies with a different manager.
- For Go/Rust/.NET work, check project files and cache/home variables before installing toolchains or dependencies.
- Do not assume generic commands such as `python`, `java`, `node`, or `gradle` are safe when project-local wrappers or profile guidance exist.
- Avoid creating environments or doing heavy package installs in constrained locations unless the user explicitly asks for that path.
- Prefer project-local or user-preferred cache locations for package caches, browser downloads, archives, build outputs, cloned repos, and temporary extraction directories whenever the tool allows it.
- Re-check reachability before using internal servers or assuming a VPN is active.
- Prefer internal mirrors, artifact registries, or support hosts documented in the profile.
- If the profile has no confirmed server inventory yet, use live discovery only as a hint and ask before taking action against a candidate host.

### Maintain the durable profile

- During first-time setup, treat profile creation as an AI-assisted interview: inspect what can be safely detected, ask only for missing stable facts, and write confirmed non-secret context.
- When the user provides new stable information, offer to update `references/environment-profile.md`.
- When the user provides new password-auth server credentials, update the configured local credential file instead of the skill files.
- Do not overwrite stable notes with transient adapter IPs, one-off failures, or noisy scan results unless the user asks.
- Append confirmed server purpose and access rules once known.

## Resource Guide

- `references/environment-profile.md`: durable, cross-project machine and server context.
- Configured local credential file: local-only plaintext server credentials for this workstation. Prefer `$CODEX_PREFLIGHT_CREDENTIAL_FILE`; otherwise use `$CODEX_PRIVATE_HOME/preflight-dev-context/server-credentials.local.json` when available.
- `scripts/resolve-server-alias.ps1`: quick lookup for server aliases, host-number shorthands, and address fragments.
- `scripts/collect-dev-context.ps1`: live snapshot of the current workstation, common language toolchains, package managers, network clues, SSH config, and local credential file presence.
