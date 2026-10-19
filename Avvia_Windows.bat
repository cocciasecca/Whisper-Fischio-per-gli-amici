@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
    set "PYTHON=.venv\Scripts\python.exe"
) else (
    where py >nul 2>nul
    if not errorlevel 1 (
        set "PYTHON=py -3"
    ) else (
        where python >nul 2>nul
        if errorlevel 1 (
            echo Python 3 non trovato. Installalo prima di avviare questo file.
            pause
            exit /b 1
        )
        set "PYTHON=python"
    )
)
%PYTHON% subtitles.py %*
set "STATUS=%ERRORLEVEL%"
echo.
echo Operazione terminata. Codice: %STATUS%
pause
exit /b %STATUS%
