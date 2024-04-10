@echo off
echo YouTube MP4 Video Downloader.
set /p url="Enter the YouTube URL: "

python ../main.py -mp4 '%url%'
echo.
pause
