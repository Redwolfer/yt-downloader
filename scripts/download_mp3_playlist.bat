@echo off
echo YouTube Playlist MP3 Audio Downloader.
set /p url="Enter the YouTube URL Playlist: "

python ../main.py -p -mp3 %url%
echo.
pause
