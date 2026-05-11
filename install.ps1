[CmdletBinding()]
param(
    [ValidateSet("portable-core", "personal-overlay", "all")]
    [string]$Package = "portable-core",

    [string]$CodexHome = $(
        if ($env:CODEX_HOME) {
            $env:CODEX_HOME
        }
        else {
            Join-Path $HOME ".codex"
        }
    ),

    [switch]$Force,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$packageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillsRoot = Join-Path $CodexHome "skills"

function Get-SourceRoots {
    switch ($Package) {
        "portable-core" {
            return @((Join-Path $packageRoot "portable-core/skills"))
        }
        "personal-overlay" {
            return @((Join-Path $packageRoot "personal-overlay/skills"))
        }
        "all" {
            return @(
                (Join-Path $packageRoot "portable-core/skills"),
                (Join-Path $packageRoot "personal-overlay/skills")
            )
        }
    }
}

function Invoke-Step {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message,
        [Parameter(Mandatory = $true)]
        [scriptblock]$Action
    )

    if ($DryRun) {
        Write-Host "[dry-run] $Message"
        return
    }

    & $Action
    Write-Host $Message
}

if (-not (Test-Path -LiteralPath $skillsRoot)) {
    Invoke-Step -Message "Created skills root: $skillsRoot" -Action {
        New-Item -ItemType Directory -Path $skillsRoot -Force | Out-Null
    }
}

foreach ($sourceRoot in Get-SourceRoots) {
    if (-not (Test-Path -LiteralPath $sourceRoot)) {
        throw "Missing source root: $sourceRoot"
    }

    foreach ($skillDir in Get-ChildItem -LiteralPath $sourceRoot -Directory) {
        $sourceSkill = $skillDir.FullName
        $targetSkill = Join-Path $skillsRoot $skillDir.Name

        if (-not (Test-Path -LiteralPath (Join-Path $sourceSkill "SKILL.md"))) {
            Write-Warning "Skipping $sourceSkill because SKILL.md is missing."
            continue
        }

        if (Test-Path -LiteralPath $targetSkill) {
            if (-not $Force) {
                Write-Host "Preserved existing skill: $targetSkill (use -Force to overwrite)"
                continue
            }

            Invoke-Step -Message "Removed existing skill: $targetSkill" -Action {
                Remove-Item -LiteralPath $targetSkill -Recurse -Force
            }
        }

        Invoke-Step -Message "Installed skill: $($skillDir.Name)" -Action {
            Copy-Item -LiteralPath $sourceSkill -Destination $targetSkill -Recurse
        }
    }
}

Write-Host "Install complete. Codex home: $CodexHome"
