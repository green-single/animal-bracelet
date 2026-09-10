# Animal Bracelet - Guard Watchdog
# Every check: if guard.ps1 loop process is dead, relaunch it
$ErrorActionPreference = 'SilentlyContinue'
$guard = 'C:\DoubaoProjects\animal-bracelet\guard\guard.ps1'
$log = 'C:\DoubaoProjects\animal-bracelet\guard\watchdog.log'

$guardRunning = Get-CimInstance Win32_Process -Filter "Name='powershell.exe' OR Name='pwsh.exe'" |
  Where-Object { $_.CommandLine -like '*guard.ps1*' } | Select-Object -First 1

if (-not $guardRunning) {
  Start-Process powershell -ArgumentList '-ExecutionPolicy','Bypass','-WindowStyle','Hidden','-File',"`"$guard`"" -WindowStyle Hidden
  $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') watchdog: guard.ps1 relaunched"
  Add-Content -Path $log -Value $line -Encoding utf8
}
