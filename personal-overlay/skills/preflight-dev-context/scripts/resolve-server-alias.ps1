[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Query,
    [string]$CredentialFile = $(
        if ($env:CODEX_PREFLIGHT_CREDENTIAL_FILE) {
            $env:CODEX_PREFLIGHT_CREDENTIAL_FILE
        }
        elseif ($env:CODEX_PRIVATE_HOME) {
            Join-Path $env:CODEX_PRIVATE_HOME "preflight-dev-context/server-credentials.local.json"
        }
        elseif ($env:CODEX_HOME) {
            Join-Path $env:CODEX_HOME "private/preflight-dev-context/server-credentials.local.json"
        }
        else {
            Join-Path $HOME ".codex-private/preflight-dev-context/server-credentials.local.json"
        }
    ),
    [switch]$Json,
    [switch]$List,
    [switch]$IncludeSecrets
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Normalize-Text {
    param([string]$Value)

    if ($null -eq $Value) {
        return ''
    }

    return $Value.Trim().ToLowerInvariant()
}

function Get-ObjectText {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Object,
        [Parameter(Mandatory = $true)]
        [string]$PropertyName
    )

    if ($null -eq $Object) {
        return ''
    }

    $property = $Object.PSObject.Properties[$PropertyName]
    if ($null -eq $property) {
        return ''
    }

    if ($null -eq $property.Value) {
        return ''
    }

    return "$($property.Value)".Trim()
}

if (-not (Test-Path -LiteralPath $CredentialFile)) {
    throw "Credential file not found: $CredentialFile"
}

$raw = Get-Content -LiteralPath $CredentialFile -Raw
$parsed = $raw | ConvertFrom-Json
$servers = @($parsed.servers)

if ($List) {
    $list = foreach ($server in $servers) {
        [pscustomobject]@{
            Alias = if ($server.alias) { "$($server.alias)".Trim() } else { '' }
            Address = if ($server.address) { "$($server.address)".Trim() } else { '' }
            User = if ($server.user) { "$($server.user)".Trim() } else { '' }
            RootMode = if ($server.root_mode) { "$($server.root_mode)".Trim() } else { '' }
            Purpose = if ($server.purpose) { "$($server.purpose)".Trim() } else { '' }
        }
    }

    if ($Json) {
        $list | ConvertTo-Json -Depth 5
        return
    }

    foreach ($item in $list) {
        Write-Output "$($item.Alias): address=$($item.Address); user=$($item.User); root=$($item.RootMode); purpose=$($item.Purpose)"
    }
    return
}

$normalizedQuery = Normalize-Text $Query
$serverMatches = @()

foreach ($server in $servers) {
    $alias = Get-ObjectText -Object $server -PropertyName 'alias'
    $address = Get-ObjectText -Object $server -PropertyName 'address'
    $purpose = Get-ObjectText -Object $server -PropertyName 'purpose'

    $aliasKey = Normalize-Text $alias
    $addressKey = Normalize-Text $address
    $purposeKey = Normalize-Text $purpose
    $hostTail = if ($address -match '\.(\d+)$') { $Matches[1] } else { '' }

    $score = 0

    if ($normalizedQuery -eq $aliasKey -or $normalizedQuery -eq $addressKey) {
        $score = 100
    }
    elseif ($hostTail -and $normalizedQuery -eq $hostTail) {
        $score = 90
    }
    elseif ($aliasKey.Contains($normalizedQuery)) {
        $score = 80
    }
    elseif ($addressKey.Contains($normalizedQuery)) {
        $score = 70
    }
    elseif ($purposeKey.Contains($normalizedQuery)) {
        $score = 60
    }

    if ($score -gt 0) {
        $serverMatches += [pscustomobject]@{
            Score = $score
            Alias = $alias
            Address = $address
            User = Get-ObjectText -Object $server -PropertyName 'user'
            Password = Get-ObjectText -Object $server -PropertyName 'password'
            RootMode = Get-ObjectText -Object $server -PropertyName 'root_mode'
            SudoPassword = Get-ObjectText -Object $server -PropertyName 'sudo_password'
            Purpose = $purpose
            Notes = Get-ObjectText -Object $server -PropertyName 'notes'
        }
    }
}

$ordered = @(
    $serverMatches | Sort-Object -Property @(
        @{ Expression = 'Score'; Descending = $true },
        @{ Expression = 'Alias'; Descending = $false }
    )
)

if ($ordered.Count -gt 0) {
    $topScore = $ordered[0].Score
    if ($topScore -ge 70) {
        $ordered = @($ordered | Where-Object { $_.Score -eq $topScore })
    }
}

if ($ordered.Count -eq 0) {
    Write-Error "No credential entry matched query '$Query'. Use -List to show known aliases."
    exit 1
}

if ($ordered.Count -gt 1 -and $ordered[0].Score -eq $ordered[1].Score) {
    if ($Json) {
        $ordered | Select-Object Alias, Address, User, RootMode, Purpose, Notes | ConvertTo-Json -Depth 5
        return
    }

    Write-Output "Multiple matches for '$Query':"
    foreach ($item in $ordered) {
        Write-Output "- $($item.Alias): address=$($item.Address); user=$($item.User); root=$($item.RootMode); purpose=$($item.Purpose)"
    }
    return
}

$winner = $ordered[0]
$sshHint = if ($winner.User -and $winner.Address) { "ssh $($winner.User)@$($winner.Address)" } else { '' }

$result = [pscustomobject]@{
    alias = $winner.Alias
    address = $winner.Address
    user = $winner.User
    has_password = [bool]$winner.Password
    root_mode = $winner.RootMode
    has_sudo_password = [bool]$winner.SudoPassword
    purpose = $winner.Purpose
    notes = $winner.Notes
    ssh_hint = $sshHint
}

if ($IncludeSecrets) {
    $result | Add-Member -NotePropertyName password -NotePropertyValue $winner.Password
    $result | Add-Member -NotePropertyName sudo_password -NotePropertyValue $winner.SudoPassword
}

if ($Json) {
    $result | ConvertTo-Json -Depth 5
    return
}

Write-Output "alias: $($result.alias)"
Write-Output "address: $($result.address)"
Write-Output "user: $($result.user)"
Write-Output "has_password = $($result.has_password)"
Write-Output "root_mode: $($result.root_mode)"
Write-Output "has_sudo_password = $($result.has_sudo_password)"
if ($IncludeSecrets) {
    Write-Output "credential_password = $($winner.Password)"
    if ($winner.SudoPassword) {
        Write-Output "credential_sudo_password = $($winner.SudoPassword)"
    }
}
Write-Output "purpose: $($result.purpose)"
if ($result.notes) {
    Write-Output "notes: $($result.notes)"
}
if ($result.ssh_hint) {
    Write-Output "ssh_hint: $($result.ssh_hint)"
}
