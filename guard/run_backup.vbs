' 诊断vbs执行
Set fso = CreateObject("Scripting.FileSystemObject")
fso.CreateTextFile "C:\DoubaoProjects\animal-bracelet\guard\vbs_ran.txt", True
Set sh = CreateObject("WScript.Shell")
sh.Run """C:\Users\13637\AppData\Local\Doubao\User Data\sandbox_runtime\bases\9f6d27f23933fb44a3a1c728c88a5ce4\python\python.exe"" ""C:\DoubaoProjects\animal-bracelet\guard\backup.py""", 0, False
fso.OpenTextFile("C:\DoubaoProjects\animal-bracelet\guard\vbs_ran.txt", 8).Write vbCrLf & "after run"
