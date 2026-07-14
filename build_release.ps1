param(
    [string]$Version = ""
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$specPath = Join-Path $repoRoot "EZ_YT-DLP.spec"
$distDir = Join-Path $repoRoot "dist"
$installerDir = Join-Path $distDir "installer"

if ([string]::IsNullOrWhiteSpace($Version)) {
    $downloadPyPath = Join-Path $repoRoot "download.py"
    $downloadPyContent = Get-Content -Path $downloadPyPath -Raw
    $currentVersion = "1.0.0"
    if ($downloadPyContent -match 'APP_VERSION\s*=\s*"([^"]+)"') {
        $currentVersion = $Matches[1]
    }

    try {
        $latestTagJson = Invoke-RestMethod -Uri "https://api.github.com/repos/LunaFennec/EzYT_DLP/releases/latest" -Headers @{ "User-Agent" = "Mozilla/5.0" }
        $latestTag = $latestTagJson.tag_name
        if ($latestTag -match 'v?(\d+)\.(\d+)(?:\.(\d+))?') {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]
            $patch = if ($Matches[3]) { [int]$Matches[3] } else { 0 }
            $nextPatch = $patch + 1
            $Version = "$major.$minor.$nextPatch"
        }
    }
    catch {
        $Version = $currentVersion
    }

    if ([string]::IsNullOrWhiteSpace($Version)) {
        $Version = $currentVersion
    }
}

$Version = $Version.Trim()
Write-Host "Using version: $Version"

New-Item -ItemType Directory -Path $installerDir -Force | Out-Null

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command py -ErrorAction SilentlyContinue
}
if (-not $pythonCmd) {
    throw "Python was not found. Install Python and the required packages before building."
}

$pythonExe = $pythonCmd.Source
Write-Host "Ensuring build dependencies are installed..."
& $pythonExe -m pip install --upgrade PySide6 PyInstaller
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install build dependencies."
}

Write-Host "Building PyInstaller bundle..."
& $pythonExe -m PyInstaller --clean --noconfirm $specPath
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller build failed."
}

$exePath = Join-Path $distDir "EZ_YT-DLP.exe"
if (-not (Test-Path $exePath)) {
    throw "Expected build output was not created: $exePath"
}

if ($pythonCmd) {
    $patchScript = @"
import os
import pefile
from pathlib import Path
exe_path = Path(r'$exePath')
tmp_path = exe_path.with_suffix('.exe.patched')
pe = pefile.PE(str(exe_path))
pe.OPTIONAL_HEADER.MajorSubsystemVersion = 6
pe.OPTIONAL_HEADER.MinorSubsystemVersion = 0
pe.write(str(tmp_path))
pe.close()
os.replace(str(tmp_path), str(exe_path))
print(f'Patched subsystem version to 6.0 on {exe_path}')
"@
    try {
        & $pythonExe -c $patchScript
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "The subsystem patch step reported a non-zero exit code, but the build will continue."
        }
    }
    catch {
        Write-Warning "The subsystem patch step could not be applied. The build will continue without it."
    }
}
else {
    Write-Warning "Python was not found. The executable was built, but the subsystem version patch step was skipped."
}

$iscc = Get-Command iscc -ErrorAction SilentlyContinue
if ($iscc) {
    $issPath = Join-Path $repoRoot "installer.iss"
    Write-Host "Building Inno Setup installer..."
    & $iscc $issPath "/O$installerDir" "/DMyAppVersion=$Version"
    if ($LASTEXITCODE -ne 0) {
        throw "Inno Setup build failed."
    }
}
else {
    Write-Warning "Inno Setup (iscc) was not found. The EXE was built successfully, but the installer was skipped."
}

Write-Host "Release build completed."
Write-Host "Executable: $exePath"
if (Test-Path (Join-Path $installerDir "EZ_YT-DLP-setup.exe")) {
    Write-Host "Installer: $(Join-Path $installerDir 'EZ_YT-DLP-setup.exe')"
}
