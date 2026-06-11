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

:: Jika dijalankan dengan argumen dari terminal, langsung arahkan ke download.py
if not "%~1"=="" (
    "%~dp0venv\Scripts\python.exe" "%~dp0download.py" %*
    exit /b %errorlevel%
)

:MAIN_MENU
cls
echo ===================================================
echo        YOUTUBE DOWNLOADER ^& AUDIO CONVERTER
echo ===================================================
echo.
echo Pilih alat yang ingin digunakan:
echo   [1] YouTube Downloader (Download Audio/Video)
echo   [2] Audio Converter (Convert audio ke MP3/WAV/FLAC/M4A/OGG)
echo   [3] Keluar
echo.
set "menu_choice=1"
set /p "menu_choice=Masukkan pilihan (1-3, default 1): "

if "%menu_choice%"=="2" (
    call :RUN_CONVERTER
    goto MAIN_MENU
)
if "%menu_choice%"=="3" (
    exit /b 0
)
if "%menu_choice%"=="1" (
    call :RUN_DOWNLOADER
    goto MAIN_MENU
)

echo Pilihan tidak valid!
pause
goto MAIN_MENU


:RUN_DOWNLOADER
cls
echo ===================================================
echo             YOUTUBE DOWNLOADER WIZARD
echo ===================================================
echo.

:INPUT_URL
set "yt_url="
set /p "yt_url=Masukkan URL YouTube: "
if "%yt_url%"=="" (
    echo [Peringatan] URL tidak boleh kosong!
    echo.
    goto INPUT_URL
)

:INPUT_TYPE
echo.
echo Pilih format unduhan:
echo   [1] Audio (MP3)
echo   [2] Video (MP4)
set "type_choice=1"
set /p "type_choice=Pilih nomor (1 atau 2, default: 1): "

set "media_type=audio"
if "%type_choice%"=="2" (
    set "media_type=video"
)

echo.
set "custom_dir="
set /p "custom_dir=Masukkan folder penyimpanan (tekan Enter untuk default 'outputs'): "

echo.
echo ===================================================
echo Memulai pengunduhan...
echo URL    : !yt_url!
echo Format : !media_type!
if not "!custom_dir!"=="" (
    echo Folder : !custom_dir!
)
echo ===================================================
echo.

if "!custom_dir!"=="" (
    "%~dp0venv\Scripts\python.exe" "%~dp0download.py" "!yt_url!" --type !media_type!
) else (
    "%~dp0venv\Scripts\python.exe" "%~dp0download.py" "!yt_url!" --type !media_type! --output_dir "!custom_dir!"
)

echo.
echo ===================================================
echo Proses selesai!
echo ===================================================
echo.
pause
exit /b 0


:RUN_CONVERTER
cls
:: Jalankan universal_converter.py (akan memunculkan wizard-nya sendiri)
"%~dp0venv\Scripts\python.exe" "%~dp0audio_converter\universal_converter.py"
exit /b 0
