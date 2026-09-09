# -*- coding: utf-8 -*-
import subprocess
r = subprocess.run(
    ['wmic', 'process', 'where', "name='python.exe'", 'get', 'ProcessId,ExecutablePath'],
    capture_output=True, text=True
)
print(r.stdout or r.stderr)
