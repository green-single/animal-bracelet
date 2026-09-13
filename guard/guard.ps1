# Animal Bracelet - Local Service Guard
# Checks localhost:8000 every 30s, auto-restarts if dead
# Log: C:\DoubaoProjects\animal-bracelet\guard\guard.log
$ErrorActionPreference = 'SilentlyContinue'
$proj = 'C:\DoubaoProjects\animal-bracelet'
$log = "$proj\guard\guard.log"
# 固定使用豆包沙箱 python（Get-Command 会解析到 WindowsApps 假壳导致闪黑窗）
$python = "$env:LOCALAPPDATA\Doubao\User Data\sandbox_runtime\bases\9f6d27f23933fb44a3a1c728c88a5ce4\python\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
  # 兜底：扫一遍 bases 目录找第一个带 python.exe 的
  $cand = Get-ChildItem "$env:LOCALAPPDATA\Doubao\User Data\sandbox_runtime\bases" -Directory -ErrorAction SilentlyContinue |
    ForEach-Object { Join-Path $_.FullName 'python\python.exe' } |
    Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
  if ($cand) { $python = $cand }
}

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
