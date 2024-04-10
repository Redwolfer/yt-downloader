@echo off
echo YouTube WAV Audio Downloader.
set /p url="Enter the YouTube URL: "

python ../main.py -wav '%url%'
echo.
pause
