Get-Process python -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,StartTime | Format-Table
Write-Host '---计划任务---'
schtasks /query /fo csv 2>$null | Select-String 'AB_FileGuard|animal' | Select-Object -First 5
Write-Host '---启动项vbs---'
Get-Item 'C:\Users\13637\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\animal_guard.vbs' -ErrorAction SilentlyContinue | Select-Object Name,LastWriteTime
Write-Host '---guard.ps1内容---'
Get-Content 'C:\DoubaoProjects\animal-bracelet\guard\guard.ps1' -TotalCount 20 -ErrorAction SilentlyContinue
