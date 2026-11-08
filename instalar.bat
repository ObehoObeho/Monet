@echo off
cd /d "%~dp0"
echo ==============================
echo    Instalando a MONET...
echo ==============================
if not exist .venv (py -m venv .venv || python -m venv .venv)
.venv\Scripts\python.exe -m pip install --upgrade pip -q
.venv\Scripts\python.exe -m pip install -r requirements.txt -q
if errorlevel 1 (echo ERROR instalando. Manda captura a Monet. & pause & exit /b 1)
if not exist .env copy .env.example .env >nul
echo.
echo Pega el token de BotFather (clic derecho para pegar) y presiona Enter:
set /p TOKEN=Token: 
.venv\Scripts\python.exe -c "import sys;from dotenv import set_key;set_key('.env','TELEGRAM_TOKEN',sys.argv[1].strip(),quote_mode='never')" "%TOKEN%"
echo.
echo LISTO. Ahora haz doble clic en iniciar.bat
pause
