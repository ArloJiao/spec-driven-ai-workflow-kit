param(
  [string]$Root = $(
    if ($env:CODEX_SKILL_LAB) {
      $env:CODEX_SKILL_LAB
    }
    elseif ($env:CODEX_HOME) {
      Join-Path $env:CODEX_HOME "skill-lab"
    }
    else {
      Join-Path $HOME ".codex/skill-lab"
    }
  )
)

$dirs = @(
  $Root,
  (Join-Path $Root "ledger"),
  (Join-Path $Root "scorecards"),
  (Join-Path $Root "snapshots")
)

foreach ($dir in $dirs) {
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

$files = @{
  (Join-Path $Root "ledger\cases.md") = "# Skill Evolution Cases`r`n`r`nShort evidence from real skill usage. Keep entries concise.`r`n"
  (Join-Path $Root "ledger\experiments.md") = "# Skill Evolution Experiments`r`n`r`nTentative rules being tested before becoming stable skill behavior.`r`n"
  (Join-Path $Root "ledger\decisions.md") = "# Skill Evolution Decisions`r`n`r`nAccepted meta-decisions about the personal skill system.`r`n"
  (Join-Path $Root "ledger\framework-extraction.md") = "# OpenDesign Extraction Candidates`r`n`r`nValidated lessons that may later be extracted from pure skills into OpenDesign.`r`n"
  (Join-Path $Root "scorecards\skill-ecosystem.md") = "# Skill Ecosystem Scorecard`r`n`r`n## Current Snapshot`r`n`r`n- last_review:`r`n- trigger accuracy:`r`n- coordination:`r`n- context efficiency:`r`n- OpenDesign extraction readiness:`r`n"
}

foreach ($path in $files.Keys) {
  if (-not (Test-Path $path)) {
    Set-Content -Encoding ASCII -Path $path -Value $files[$path]
  }
}

Write-Host "Skill lab ready: $Root"
