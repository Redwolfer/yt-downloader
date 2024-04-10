@echo off
echo YouTube MP3 Audio Downloader.
set /p url="Enter the YouTube URL: "

python ../main.py -mp3 '%url%'
echo.
pause
