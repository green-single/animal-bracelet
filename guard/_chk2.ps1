Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" |
  Where-Object { $_.CommandLine -like '*guard*' } |
  Select-Object ProcessId, @{N='Cmd';E={($_.CommandLine).Substring(0,[Math]::Min(90,$_.CommandLine.Length))}} |
  Format-List
