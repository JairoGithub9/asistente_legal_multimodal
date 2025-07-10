#Se instalo en el computador de manera global : 

-> Instalar el "Traductor Universal" FFmpeg
Comando: Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

ven: .\venv\Scripts\Activate.ps1  
luego: uvicorn backend.main:aplicacion 