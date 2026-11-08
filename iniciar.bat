@echo off
cd /d "%~dp0"
echo Encendiendo a MONET... (cierra esta ventana para apagarlo)
.venv\Scripts\python.exe -m monet.bot
pause
