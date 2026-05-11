[CmdletBinding()]
param(
    [string]$Root = $(
        if ($env:CODEX_HUB) {
            $env:CODEX_HUB
        }
        elseif ($env:CODEX_HOME) {
            Join-Path $env:CODEX_HOME "workstream-hub"
        }
        else {
            Join-Path $HOME ".codex/workstream-hub"
        }
    ),
    [switch]$Force,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$skillRoot = Split-Path -Parent $PSScriptRoot
$templateRoot = Join-Path $skillRoot "assets\\templates\\hub"

if ($Root -like "C:\\*") {
    Write-Warning "The requested hub root is on C:. Confirm this is acceptable before storing large durable workstream data."
}

$directories = @(
    $Root,
    (Join-Path $Root "portfolio"),
    (Join-Path $Root "workstreams"),
    (Join-Path $Root "sessions"),
    (Join-Path $Root "projects")
)

$templateFiles = @(
    @{
        Source = Join-Path (Join-Path $templateRoot "portfolio") "dashboard.md"
        Destination = Join-Path (Join-Path $Root "portfolio") "dashboard.md"
    },
    @{
        Source = Join-Path (Join-Path $templateRoot "portfolio") "inbox.md"
        Destination = Join-Path (Join-Path $Root "portfolio") "inbox.md"
    }
)

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

foreach ($directory in $directories) {
    if (Test-Path -LiteralPath $directory) {
        Write-Host "Exists: $directory"
        continue
    }

    Invoke-Step -Message "Created directory: $directory" -Action {
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
    }
}

foreach ($item in $templateFiles) {
    if (-not (Test-Path -LiteralPath $item.Source)) {
        throw "Missing template: $($item.Source)"
    }

    $destinationExists = Test-Path -LiteralPath $item.Destination
    if ($destinationExists -and -not $Force) {
        Write-Host "Preserved existing file: $($item.Destination)"
        continue
    }

    $message = if ($destinationExists) {
        "Overwrote file: $($item.Destination)"
    }
    else {
        "Created file: $($item.Destination)"
    }

    Invoke-Step -Message $message -Action {
        Copy-Item -LiteralPath $item.Source -Destination $item.Destination -Force
    }
}

Write-Host "Hub root ready: $Root"
