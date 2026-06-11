@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo       YOUTUBE DOWNLOADER ^& CONVERTER SETUP
echo ===================================================
echo.
echo Skrip ini akan memeriksa dan menyiapkan semua kebutuhan
echo aplikasi secara otomatis (Python, FFmpeg, venv, dan dependensi).
echo Sangat cocok untuk komputer baru yang belum terinstal apa-apa.
echo.
echo ===================================================
echo.

:: 1. Periksa Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Python tidak ditemukan di komputer Anda.
    echo [INFO] Mencoba menginstal Python secara otomatis menggunakan winget...
    echo.
    winget install -e --id Python.Python.3 --source winget
    if !errorlevel! neq 0 (
        echo.
        echo [ERROR] Gagal menginstal Python secara otomatis.
        echo Silakan unduh dan instal Python manual dari: https://www.python.org/
        echo *PENTING: Centang opsi "Add Python to PATH" saat instalasi.*
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [SUCCESS] Python berhasil diinstal!
    echo [PENTING] Anda harus menutup jendela Command Prompt ini dan membuka kembali
    echo           file setup.bat agar sistem mendeteksi instalasi Python yang baru.
    echo.
    pause
    exit /b 0
) else (
    echo [OK] Python sudah terinstall.
)

:: 2. Periksa FFmpeg
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] FFmpeg tidak ditemukan di komputer Anda.
    echo [INFO] Mencoba menginstal FFmpeg secara otomatis menggunakan winget...
    echo.
    winget install -e --id Gyan.FFmpeg --source winget
    if !errorlevel! neq 0 (
        echo.
        echo [ERROR] Gagal menginstal FFmpeg secara otomatis.
        echo Silakan ikuti panduan instalasi FFmpeg secara manual di file README.md.
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [SUCCESS] FFmpeg berhasil diinstal!
    echo [PENTING] Jika proses konversi audio nantinya error, silakan restart komputer Anda
    echo           agar path FFmpeg yang baru saja diinstal terbaca sepenuhnya oleh sistem.
    echo.
) else (
    echo [OK] FFmpeg sudah terinstall.
)

:: 3. Membuat Virtual Environment (venv)
if not exist "%~dp0venv\Scripts\python.exe" (
    echo [INFO] Membuat Virtual Environment (venv)...
    python -m venv "%~dp0venv"
    if !errorlevel! neq 0 (
        echo [ERROR] Gagal membuat virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual Environment berhasil dibuat.
) else (
    echo [OK] Virtual Environment (venv) sudah ada.
)

:: 4. Menginstal Dependensi dari requirements.txt
echo [INFO] Menginstal dependensi pustaka Python (tqdm, pytubefix, pydub)...
"%~dp0venv\Scripts\python.exe" -m pip install --upgrade pip
"%~dp0venv\Scripts\python.exe" -m pip install -r "%~dp0requirements.txt"
if %errorlevel% neq 0 (
    echo [ERROR] Gagal menginstal dependensi.
    pause
    exit /b 1
)

echo.
echo ===================================================
echo [SUCCESS] INSTALASI DAN SETUP BERHASIL!
echo ===================================================
echo.
echo Sekarang Anda bisa langsung menjalankan:
echo   - yt-downloader.bat  (untuk download dari YouTube)
echo   - audio-converter.bat (untuk mengonversi audio)
echo.
pause
exit /b 0
