# Environment Profile Template

Update this file when stable environment facts change. Keep credentials, tokens, passwords, private keys, and customer secrets out of it.

## Purpose

This file is durable, cross-project context for the local development environment. Use it before technical work, then refresh session-specific facts with `scripts/collect-dev-context.ps1` when needed.

## Local Credential File

- Credentials are not stored in this shared profile.
- If password-auth hosts are part of the user's environment, store them in a local-only file selected by:
  - `$CODEX_PREFLIGHT_CREDENTIAL_FILE`, or
  - `$CODEX_PRIVATE_HOME/preflight-dev-context/server-credentials.local.json`, or
  - `$CODEX_HOME/private/preflight-dev-context/server-credentials.local.json`.
- For quick lookup, use `scripts/resolve-server-alias.ps1 -Query <alias>`.

## Stable Baseline

Fill this in for the recipient's machine:

- Hostname:
- OS/platform:
- Shell baseline:
- Hardware notes:
- Preferred workspace roots:
- Storage constraints:

## Python Baseline

- Preferred environment workflow:
- Preferred direct interpreter:
- Package manager notes:
- Known shims or broken commands:
- Cache or virtualenv location policy:

## Java / JVM / Android Baseline

- Preferred JDK distribution and version:
- `JAVA_HOME` policy:
- Gradle wrapper versus global Gradle policy:
- Maven policy:
- Kotlin/Android notes:
- Android SDK location:
- ADB/emulator/device testing notes:
- Gradle/Maven cache location policy:

## Node / JavaScript Baseline

- Preferred Node version manager:
- Preferred package manager:
- Lockfile policy:
- Global install policy:
- Cache location policy:

## Go Baseline

- Preferred Go version:
- `GOROOT` / `GOPATH` policy:
- Module cache policy:
- Proxy policy:

## Rust Baseline

- Preferred Rust toolchain:
- `rustup` policy:
- `CARGO_HOME` / `RUSTUP_HOME` policy:
- Build cache policy:

## .NET Baseline

- Preferred SDK version:
- NuGet cache policy:
- MSBuild/Visual Studio Build Tools notes:

## Containers / Deployment Baseline

- Docker or Podman availability:
- Kubernetes context policy:
- Registry/mirror policy:
- Compose/deployment notes:

## Database CLI Baseline

- PostgreSQL CLI:
- MySQL CLI:
- Redis CLI:
- SQLite CLI:
- MongoDB CLI:

## Network Baseline

- Normal network environment:
- VPN or intranet requirements:
- Proxy variables:
- Internal package mirrors:
- Reachability checks to run before remote work:

## Remote Host Inventory

Do not include secrets. Use aliases, purpose, access type, and caveats only.

| Alias | Address | Access | Purpose | Evidence | Notes |
| --- | --- | --- | --- | --- | --- |
| `example-staging` | `staging.example.internal` | SSH as deploy user | staging deploy host | user confirmed | Credentials live only in the local credential file |

## Working Rules

- Before language/toolchain work, confirm the relevant runtime, package manager, and project-local wrapper strategy.
- Before package installation, confirm cache location and mirror/proxy requirements.
- Before Android work, confirm JDK, Android SDK, Gradle wrapper, and ADB/device state.
- Before remote-server work, identify the target host, access method, environment tier, and intended action.
- Treat live discovery as a hint; treat confirmed user-supplied notes in this file as durable context.

## Questions To Resolve Over Time

- Which package mirrors should be preferred?
- Which language runtimes are managed globally versus per-project?
- Which build caches should stay project-local or on a specific drive?
- Which hosts require VPN, proxy, or jump hosts?
- Which credentials are intentionally local-only?
