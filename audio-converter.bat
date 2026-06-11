@echo off
setlocal enabledelayedexpansion

:: Periksa apakah venv terinstall
if not exist "%~dp0venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment venv tidak ditemukan!
    echo Pastikan folder venv ada di folder yang sama dengan file .bat ini.
    echo.
    pause
    exit /b 1
)

:: Jalankan universal converter dengan argumen apa pun yang diberikan
"%~dp0venv\Scripts\python.exe" "%~dp0audio_converter\universal_converter.py" %*
