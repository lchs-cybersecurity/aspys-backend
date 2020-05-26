$Env:SECRET_KEY = Invoke-Command {py.exe -c "import os ; print(os.urandom(32))"}
Write-Output "Set SECRET_KEY to $Env:SECRET_KEY."