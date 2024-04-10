@echo off
echo YouTube Playlist WAV Video Downloader.
set /p url="Enter the YouTube URL Playlist: "

python ../main.py -p -wav %url%
echo.
pause
