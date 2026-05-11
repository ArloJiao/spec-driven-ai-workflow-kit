param(
    [string]$OutFile
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Join-Values {
    param([object[]]$Values)

    $items = @()
    foreach ($value in $Values) {
        if ($null -eq $value) {
            continue
        }
        $text = "$value".Trim()
        if ($text) {
            $items += $text
        }
    }

    if ($items.Count -eq 0) {
        return 'n/a'
    }

    return ($items -join ', ')
}

function Get-CommandPath {
    param([string]$Name)

    $command = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -eq $command) {
        return $null
    }

    return $command.Source
}

function Get-ToolLines {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Names,
        [string]$MissingText = 'none detected in PATH'
    )

    $lines = @()
    foreach ($name in $Names) {
        $path = Get-CommandPath $name
        if ($path) {
            $lines += "- ${name}: $path"
        }
    }

    if ($lines.Count -eq 0) {
        return @("- $MissingText")
    }

    return $lines
}

function Get-EnvLines {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Names,
        [string]$MissingText = 'none set'
    )

    $lines = @()
    foreach ($name in $Names) {
        $value = [Environment]::GetEnvironmentVariable($name, 'Process')
        if (-not $value) {
            $value = [Environment]::GetEnvironmentVariable($name, 'User')
        }
        if (-not $value) {
            $value = [Environment]::GetEnvironmentVariable($name, 'Machine')
        }
        if ($value) {
            $lines += "- ${name}: $value"
        }
    }

    if ($lines.Count -eq 0) {
        return @("- $MissingText")
    }

    return $lines
}

function Invoke-VersionProbe {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Command,
        [string[]]$Arguments = @('--version')
    )

    $commandPath = Get-CommandPath $Command
    if (-not $commandPath) {
        return $null
    }

    try {
        $startInfo = New-Object System.Diagnostics.ProcessStartInfo
        $argumentText = ($Arguments -join ' ')
        $extension = [System.IO.Path]::GetExtension($commandPath).ToLowerInvariant()
        if ($extension -eq '.cmd' -or $extension -eq '.bat') {
            $startInfo.FileName = 'cmd.exe'
            $startInfo.Arguments = "/c `"$commandPath`" $argumentText"
        }
        elseif ($extension -eq '.ps1') {
            $startInfo.FileName = 'powershell.exe'
            $startInfo.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$commandPath`" $argumentText"
        }
        else {
            $startInfo.FileName = $commandPath
            $startInfo.Arguments = $argumentText
        }
        $startInfo.UseShellExecute = $false
        $startInfo.RedirectStandardOutput = $true
        $startInfo.RedirectStandardError = $true
        $startInfo.CreateNoWindow = $true

        $process = New-Object System.Diagnostics.Process
        $process.StartInfo = $startInfo
        [void]$process.Start()
        $stdout = $process.StandardOutput.ReadToEnd()
        $stderr = $process.StandardError.ReadToEnd()
        $process.WaitForExit(5000) | Out-Null
        if (-not $process.HasExited) {
            try {
                $process.Kill()
            }
            catch {
                # Best-effort cleanup only.
            }
            return "${Command}: timed out"
        }

        $text = (($stdout, $stderr) -join [Environment]::NewLine).Trim()
        if (-not $text) {
            return "${Command}: detected"
        }
        $summary = ($text -split "(`r`n|`n|`r)") | Where-Object { $_.Trim() } | Select-Object -First 3
        return "${Command}: $(($summary -join '; ').Trim())"
    }
    catch {
        return "${Command}: failed to query"
    }
}

function Get-SshHostEntries {
    $configPath = Join-Path $HOME '.ssh/config'
    if (-not (Test-Path $configPath)) {
        return @()
    }

    $entries = @()
    $currentEntries = @()

    foreach ($line in Get-Content $configPath) {
        $trimmed = $line.Trim()
        if (-not $trimmed) {
            continue
        }
        if ($trimmed.StartsWith('#')) {
            continue
        }

        if ($trimmed -match '^(?i)Host\s+(.+)$') {
            if ($currentEntries.Count -gt 0) {
                $entries += $currentEntries
            }

            $currentEntries = @()
            $aliases = $Matches[1].Split(' ', [System.StringSplitOptions]::RemoveEmptyEntries)
            foreach ($alias in $aliases) {
                if ($alias -match '[*?]') {
                    continue
                }

                $currentEntries += [pscustomobject]@{
                    Alias = $alias
                    HostName = ''
                    User = ''
                    Port = ''
                    IdentityFile = ''
                }
            }

            continue
        }

        if ($currentEntries.Count -eq 0) {
            continue
        }

        if ($trimmed -match '^(?i)HostName\s+(.+)$') {
            foreach ($entry in $currentEntries) {
                $entry.HostName = $Matches[1].Trim()
            }
            continue
        }

        if ($trimmed -match '^(?i)User\s+(.+)$') {
            foreach ($entry in $currentEntries) {
                $entry.User = $Matches[1].Trim()
            }
            continue
        }

        if ($trimmed -match '^(?i)Port\s+(.+)$') {
            foreach ($entry in $currentEntries) {
                $entry.Port = $Matches[1].Trim()
            }
            continue
        }

        if ($trimmed -match '^(?i)IdentityFile\s+(.+)$') {
            foreach ($entry in $currentEntries) {
                $entry.IdentityFile = $Matches[1].Trim()
            }
        }
    }

    if ($currentEntries.Count -gt 0) {
        $entries += $currentEntries
    }

    return $entries
}

function Get-HostsEntries {
    $hostsPath = Join-Path $env:WINDIR 'System32/drivers/etc/hosts'
    if (-not (Test-Path $hostsPath)) {
        return @()
    }

    $entries = @()
    foreach ($line in Get-Content $hostsPath) {
        $trimmed = $line.Trim()
        if (-not $trimmed) {
            continue
        }
        if ($trimmed.StartsWith('#')) {
            continue
        }
        $entries += $trimmed
    }

    return $entries
}

function Get-LocalCredentialSnapshot {
    if ($env:CODEX_PREFLIGHT_CREDENTIAL_FILE) {
        $path = $env:CODEX_PREFLIGHT_CREDENTIAL_FILE
    }
    elseif ($env:CODEX_PRIVATE_HOME) {
        $path = Join-Path $env:CODEX_PRIVATE_HOME "preflight-dev-context/server-credentials.local.json"
    }
    elseif ($env:CODEX_HOME) {
        $path = Join-Path $env:CODEX_HOME "private/preflight-dev-context/server-credentials.local.json"
    }
    else {
        $path = Join-Path $HOME ".codex-private/preflight-dev-context/server-credentials.local.json"
    }
    if (-not (Test-Path -LiteralPath $path)) {
        return [pscustomobject]@{
            Path = $path
            Status = 'missing'
            Entries = @()
        }
    }

    try {
        $raw = Get-Content -LiteralPath $path -Raw
        $parsed = $raw | ConvertFrom-Json
    }
    catch {
        return [pscustomobject]@{
            Path = $path
            Status = 'parse_failed'
            Entries = @()
        }
    }

    $entries = @()
    foreach ($server in @($parsed.servers)) {
        if ($null -eq $server) {
            continue
        }

        $alias = if ($server.alias) { "$($server.alias)".Trim() } else { '' }
        if (-not $alias) {
            continue
        }

        $entries += [pscustomobject]@{
            Alias = $alias
            Address = if ($server.address) { "$($server.address)".Trim() } else { 'n/a' }
            User = if ($server.user) { "$($server.user)".Trim() } else { 'n/a' }
            RootMode = if ($server.root_mode) { "$($server.root_mode)".Trim() } else { 'n/a' }
        }
    }

    return [pscustomobject]@{
        Path = $path
        Status = 'found'
        Entries = $entries
    }
}

$os = Get-CimInstance Win32_OperatingSystem
$computer = Get-CimInstance Win32_ComputerSystem
$psVersion = $PSVersionTable.PSVersion.ToString()

$activeAdapters = @()
foreach ($config in Get-NetIPConfiguration) {
    $adapter = Get-NetAdapter -InterfaceIndex $config.InterfaceIndex -ErrorAction SilentlyContinue
    if ($null -eq $adapter) {
        continue
    }

    if ($adapter.Status -ne 'Up' -and -not $config.IPv4DefaultGateway) {
        continue
    }

    $gatewayValues = @()
    foreach ($gateway in @($config.IPv4DefaultGateway)) {
        if ($null -ne $gateway -and $gateway.PSObject.Properties.Name -contains 'NextHop') {
            $gatewayValues += $gateway.NextHop
        }
    }

    $activeAdapters += [pscustomobject]@{
        Name = $config.InterfaceAlias
        IPv4 = Join-Values ($config.IPv4Address | ForEach-Object { $_.IPAddress })
        Gateway = Join-Values $gatewayValues
        DNS = Join-Values $config.DNSServer.ServerAddresses
        Description = $adapter.InterfaceDescription
        LinkSpeed = $adapter.LinkSpeed
    }
}

$pythonToolLines = Get-ToolLines -Names @('python', 'py', 'uv', 'conda', 'pip', 'pipx', 'poetry', 'pixi', 'rye') -MissingText 'no Python-related tools detected in PATH'
$jvmToolLines = Get-ToolLines -Names @('java', 'javac', 'gradle', 'mvn', 'kotlinc', 'kotlin') -MissingText 'no JVM-related tools detected in PATH'
$androidToolLines = Get-ToolLines -Names @('adb', 'sdkmanager', 'avdmanager', 'emulator') -MissingText 'no Android SDK tools detected in PATH'
$nodeToolLines = Get-ToolLines -Names @('node', 'npm', 'pnpm', 'yarn', 'corepack', 'bun', 'deno') -MissingText 'no Node/JS tools detected in PATH'
$goToolLines = Get-ToolLines -Names @('go', 'gofmt') -MissingText 'no Go tools detected in PATH'
$rustToolLines = Get-ToolLines -Names @('rustc', 'cargo', 'rustup') -MissingText 'no Rust tools detected in PATH'
$dotnetToolLines = Get-ToolLines -Names @('dotnet', 'msbuild', 'nuget') -MissingText 'no .NET tools detected in PATH'
$containerToolLines = Get-ToolLines -Names @('docker', 'docker-compose', 'kubectl', 'helm', 'podman') -MissingText 'no container/orchestration tools detected in PATH'
$vcsToolLines = Get-ToolLines -Names @('git', 'gh', 'ssh') -MissingText 'no VCS/SSH tools detected in PATH'
$dbToolLines = Get-ToolLines -Names @('psql', 'mysql', 'redis-cli', 'mongosh', 'sqlite3') -MissingText 'no database CLIs detected in PATH'

$jvmEnvLines = Get-EnvLines -Names @('JAVA_HOME', 'JDK_HOME', 'GRADLE_USER_HOME', 'MAVEN_OPTS', 'KOTLIN_HOME')
$androidEnvLines = Get-EnvLines -Names @('ANDROID_HOME', 'ANDROID_SDK_ROOT', 'ANDROID_AVD_HOME', 'ADB_VENDOR_KEYS')
$nodeEnvLines = Get-EnvLines -Names @('NODE_OPTIONS', 'NPM_CONFIG_PREFIX', 'NPM_CONFIG_CACHE', 'PNPM_HOME', 'YARN_CACHE_FOLDER')
$goEnvLines = Get-EnvLines -Names @('GOROOT', 'GOPATH', 'GOMODCACHE', 'GOPROXY')
$rustEnvLines = Get-EnvLines -Names @('RUSTUP_HOME', 'CARGO_HOME', 'RUSTFLAGS')
$dotnetEnvLines = Get-EnvLines -Names @('DOTNET_ROOT', 'NUGET_PACKAGES')
$containerEnvLines = Get-EnvLines -Names @('DOCKER_HOST', 'DOCKER_CONFIG', 'KUBECONFIG')

$versionProbeSpecs = @(
    @{ Command = 'java'; Arguments = @('-version') },
    @{ Command = 'javac'; Arguments = @('-version') },
    @{ Command = 'gradle'; Arguments = @('--version') },
    @{ Command = 'mvn'; Arguments = @('--version') },
    @{ Command = 'adb'; Arguments = @('version') },
    @{ Command = 'node'; Arguments = @('--version') },
    @{ Command = 'npm'; Arguments = @('--version') },
    @{ Command = 'go'; Arguments = @('version') },
    @{ Command = 'rustc'; Arguments = @('--version') },
    @{ Command = 'cargo'; Arguments = @('--version') },
    @{ Command = 'dotnet'; Arguments = @('--version') },
    @{ Command = 'docker'; Arguments = @('--version') },
    @{ Command = 'git'; Arguments = @('--version') }
)

$versionLines = @()
foreach ($spec in $versionProbeSpecs) {
    $probe = Invoke-VersionProbe -Command $spec.Command -Arguments $spec.Arguments
    if ($probe) {
        $versionLines += "- $probe"
    }
}
if ($versionLines.Count -eq 0) {
    $versionLines = @('- no common tool versions detected')
}

$pyVersion = 'unavailable'
$pyLauncher = 'unavailable'
if (Get-CommandPath 'py') {
    try {
        $pyVersion = (& py --version 2>$null | Out-String).Trim()
    }
    catch {
        $pyVersion = 'failed to query'
    }

    try {
        $pyLauncher = (& py -0p 2>$null | Out-String).Trim()
    }
    catch {
        $pyLauncher = 'failed to query'
    }
}

$proxyPairs = @(
    @{ Name = 'HTTP_PROXY'; Value = [Environment]::GetEnvironmentVariable('HTTP_PROXY', 'User') },
    @{ Name = 'HTTPS_PROXY'; Value = [Environment]::GetEnvironmentVariable('HTTPS_PROXY', 'User') },
    @{ Name = 'NO_PROXY'; Value = [Environment]::GetEnvironmentVariable('NO_PROXY', 'User') }
) | Where-Object { $_.Value }

$proxyLines = @()
foreach ($pair in $proxyPairs) {
    $proxyLines += "- $($pair.Name): $($pair.Value)"
}
if ($proxyLines.Count -eq 0) {
    $proxyLines = @('- no proxy variables found in the user environment')
}

$internetReachable = 'unknown'
try {
    $internetReachable = [string](Test-NetConnection 'www.microsoft.com' -InformationLevel Quiet)
}
catch {
    $internetReachable = 'failed to test'
}

$sshHostEntries = @(Get-SshHostEntries)
$hostsEntries = @(Get-HostsEntries)
$localCredentialSnapshot = Get-LocalCredentialSnapshot

$lines = @()
$lines += '# Live Dev Context Snapshot'
$lines += ''
$lines += "- Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
$lines += ''
$lines += '## Machine'
$lines += ''
$lines += "- Hostname: $($os.CSName)"
$lines += "- OS: $($os.Caption) ($($os.Version), $($os.OSArchitecture))"
$lines += "- PowerShell: $psVersion"
$lines += "- Hardware: $($computer.Manufacturer) $($computer.Model) with $([Math]::Round($computer.TotalPhysicalMemory / 1GB, 1)) GiB RAM"
$lines += "- Last boot: $($os.LastBootUpTime)"
$lines += ''
$lines += '## Python'
$lines += ''
$lines += "- py launcher version: $pyVersion"
$lines += "- py launcher targets: $pyLauncher"
$lines += '- Detected tool paths:'
$lines += $pythonToolLines
$lines += ''
$lines += '## Java / JVM'
$lines += ''
$lines += '- Detected tool paths:'
$lines += $jvmToolLines
$lines += '- Environment variables:'
$lines += $jvmEnvLines
$lines += ''
$lines += '## Android'
$lines += ''
$lines += '- Detected tool paths:'
$lines += $androidToolLines
$lines += '- Environment variables:'
$lines += $androidEnvLines
$lines += ''
$lines += '## Node / JavaScript'
$lines += ''
$lines += '- Detected tool paths:'
$lines += $nodeToolLines
$lines += '- Environment variables:'
$lines += $nodeEnvLines
$lines += ''
$lines += '## Go'
$lines += ''
$lines += '- Detected tool paths:'
$lines += $goToolLines
$lines += '- Environment variables:'
$lines += $goEnvLines
$lines += ''
$lines += '## Rust'
$lines += ''
$lines += '- Detected tool paths:'
$lines += $rustToolLines
$lines += '- Environment variables:'
$lines += $rustEnvLines
$lines += ''
$lines += '## .NET'
$lines += ''
$lines += '- Detected tool paths:'
$lines += $dotnetToolLines
$lines += '- Environment variables:'
$lines += $dotnetEnvLines
$lines += ''
$lines += '## Containers / Orchestration'
$lines += ''
$lines += '- Detected tool paths:'
$lines += $containerToolLines
$lines += '- Environment variables:'
$lines += $containerEnvLines
$lines += ''
$lines += '## VCS / Remote Access'
$lines += ''
$lines += '- Detected tool paths:'
$lines += $vcsToolLines
$lines += ''
$lines += '## Database CLIs'
$lines += ''
$lines += '- Detected tool paths:'
$lines += $dbToolLines
$lines += ''
$lines += '## Common Tool Versions'
$lines += ''
$lines += $versionLines
$lines += ''
$lines += '## Network'
$lines += ''
$lines += "- Public internet reachable: $internetReachable"
$lines += '- Proxy variables:'
$lines += $proxyLines
$lines += '- Active adapters:'
if ($activeAdapters.Count -eq 0) {
    $lines += '- none detected'
}
else {
    foreach ($adapter in $activeAdapters) {
        $lines += "- $($adapter.Name): IPv4=$($adapter.IPv4); Gateway=$($adapter.Gateway); DNS=$($adapter.DNS); Link=$($adapter.LinkSpeed)"
        $lines += "  Description: $($adapter.Description)"
    }
}
$lines += ''
$lines += '## Intranet Clues'
$lines += ''
if ($sshHostEntries.Count -eq 0) {
    $lines += '- SSH config hosts: none found'
}
else {
    $lines += '- SSH config entries:'
    foreach ($sshEntry in $sshHostEntries) {
        $hostName = if ($sshEntry.HostName) { $sshEntry.HostName } else { 'n/a' }
        $user = if ($sshEntry.User) { $sshEntry.User } else { 'n/a' }
        $port = if ($sshEntry.Port) { $sshEntry.Port } else { 'default' }
        $identityFile = if ($sshEntry.IdentityFile) { $sshEntry.IdentityFile } else { 'n/a' }
        $lines += "- $($sshEntry.Alias): host=$hostName; user=$user; port=$port; identity=$identityFile"
    }
}
if ($hostsEntries.Count -eq 0) {
    $lines += '- Hosts file entries: none found'
}
else {
    $lines += "- Hosts file entries: $(Join-Values $hostsEntries)"
}
$lines += ''
$lines += '## Local Credential File'
$lines += ''
switch ($localCredentialSnapshot.Status) {
    'found' {
        $lines += "- File: found at $($localCredentialSnapshot.Path)"
        if ($localCredentialSnapshot.Entries.Count -eq 0) {
            $lines += '- Entries: none'
        }
        else {
            $lines += '- Entries:'
            foreach ($entry in $localCredentialSnapshot.Entries) {
                $lines += "- $($entry.Alias): address=$($entry.Address); user=$($entry.User); root=$($entry.RootMode)"
            }
        }
    }
    'parse_failed' {
        $lines += "- File: found at $($localCredentialSnapshot.Path), but JSON parsing failed"
    }
    default {
        $lines += "- File: missing at $($localCredentialSnapshot.Path)"
    }
}

$output = $lines -join [Environment]::NewLine
if ($OutFile) {
    $parent = Split-Path -Parent $OutFile
    if ($parent) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }
    Set-Content -Path $OutFile -Value $output -Encoding ascii
}
else {
    Write-Output $output
}
