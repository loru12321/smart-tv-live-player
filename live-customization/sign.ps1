param([string]$BuildRoot = 'C:\Users\loru\ysc-live-build')
$ErrorActionPreference = 'Stop'
$javaBin = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot\bin'
$env:JAVA_HOME = Split-Path $javaBin
$sdkBuild = Join-Path $env:LOCALAPPDATA 'Android\Sdk\build-tools\34.0.0'
$keyDir = Join-Path $env:USERPROFILE '.android\ysc-live-signing'
New-Item -ItemType Directory -Force $keyDir | Out-Null
$passwordFile = Join-Path $keyDir 'password.txt'
$keyFile = Join-Path $keyDir 'live.jks'
if (!(Test-Path -LiteralPath $keyFile)) {
    if (!(Test-Path -LiteralPath $passwordFile)) {
        [IO.File]::WriteAllText($passwordFile, [Guid]::NewGuid().ToString('N'))
    }
    & "$javaBin\keytool.exe" -genkeypair -keystore $keyFile -storepass:file $passwordFile -keypass:file $passwordFile -alias live -keyalg RSA -keysize 2048 -validity 10000 -dname 'CN=Local TV Live, OU=Personal, O=Local, C=CN'
    if ($LASTEXITCODE) { throw 'Key generation failed' }
}
& "$sdkBuild\zipalign.exe" -f 4 "$BuildRoot\live-unsigned.apk" "$BuildRoot\live-aligned.apk"
if ($LASTEXITCODE) { throw 'Alignment failed' }
$output = Join-Path (Split-Path $PSScriptRoot) '发布\影视仓直播版'
New-Item -ItemType Directory -Force $output | Out-Null
$apk = Join-Path $output '影视仓直播版-2026.10.apk'
& "$sdkBuild\apksigner.bat" sign --ks $keyFile --ks-key-alias live --ks-pass "file:$passwordFile" --out $apk "$BuildRoot\live-aligned.apk"
if ($LASTEXITCODE) { throw 'Signing failed' }
& "$sdkBuild\apksigner.bat" verify --verbose $apk
if ($LASTEXITCODE) { throw 'Signature verification failed' }
Get-FileHash -Algorithm SHA256 -LiteralPath $apk
