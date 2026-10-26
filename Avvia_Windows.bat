@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    where py >nul 2>nul
    if not errorlevel 1 (
        py -3 -m venv .venv
    ) else (
        python -m venv .venv
    )
    if errorlevel 1 (
        echo Impossibile creare il venv. Verifica che Python 3 sia installato.
        pause
        exit /b 1
    )
)
set "PYTHON=.venv\Scripts\python.exe"
%PYTHON% setup_runtime.py %*
set "STATUS=%ERRORLEVEL%"
echo.
echo Operazione terminata. Codice: %STATUS%
pause
exit /b %STATUS%
