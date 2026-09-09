# Animal Bracelet - Local Service Guard
# Checks localhost:8000 every 30s, auto-restarts if dead
# Log: C:\DoubaoProjects\animal-bracelet\guard\guard.log
$ErrorActionPreference = 'SilentlyContinue'
$proj = 'C:\DoubaoProjects\animal-bracelet'
$log = "$proj\guard\guard.log"
$python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) { $python = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" }

function Write-Log($msg) {
  $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $msg"
  Add-Content -Path $log -Value $line -Encoding utf8
}

function Test-Service {
  try {
    $client = New-Object System.Net.Sockets.TcpClient
    $task = $client.ConnectAsync('127.0.0.1', 8000)
    if ($task.Wait(3000)) { $ok = $client.Connected } else { $ok = $false }
    $client.Close()
    return $ok
  } catch { return $false }
}

if (-not (Test-Service)) {
  Start-Process -FilePath $python -ArgumentList 'run.py' -WorkingDirectory $proj -WindowStyle Hidden
  Write-Log 'guard start: service down, relaunched'
} else {
  Write-Log 'guard start: service already running'
}

$deadCount = 0
while ($true) {
  Start-Sleep -Seconds 30
  $alive = Test-Service
  if ($alive) {
    $deadCount = 0
  } else {
    $deadCount++
    if ($deadCount -ge 2) {
      try {
        $conns = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
        foreach ($c in $conns) {
          Stop-Process -Id $c.OwningProcess -Force -ErrorAction SilentlyContinue
        }
      } catch {}
      Start-Sleep -Seconds 2
      Start-Process -FilePath $python -ArgumentList 'run.py' -WorkingDirectory $proj -WindowStyle Hidden
      Write-Log "guard: service down, relaunched (deadCount=$deadCount)"
      $deadCount = 0
      Start-Sleep -Seconds 10
    }
  }
}
