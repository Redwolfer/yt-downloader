@echo off
echo YouTube Playlist MP4 Video Downloader.
set /p url="Enter the YouTube URL Playlist: "

python ../main.py -p -mp4 %url%
echo.
pause
