#!/usr/bin/env python3
"""
YouTube Downloader Script

This script downloads a YouTube video or playlist as either audio or video.
Audio files are converted to MP3 format after downloading.

Usage:
    python download.py <url> [--type {audio,video}] [--output_dir OUTPUT_DIR] [--playlist] [--single]
"""

import os
import re
import sys
import argparse
import tempfile
from typing import Optional

from tqdm import tqdm

# Ensure the required module is available.
try:
    from pytubefix import YouTube, Playlist, extract
except ImportError:
    print("Error: 'pytubefix' module is not installed. Install it with 'pip install pytubefix' "
          "or, if you meant pytube, adjust the import accordingly.")
    sys.exit(1)

try:
    from pydub import AudioSegment
except ImportError:
    print("Error: 'pydub' module is not installed. Install it with 'pip install pydub'.")
    sys.exit(1)


class YouTubeDownloader:
    """Download YouTube videos or playlists as audio or video."""

    def __init__(self, url: str, media_type: str = "audio", output_dir: str = "outputs", is_playlist: Optional[bool] = None):
        self.url = url
        self.media_type = media_type.lower()
        self.base_output_dir = output_dir
        self.output_dir = os.path.join(output_dir, self.media_type)

        # Detect if the URL is a playlist
        if is_playlist is None:
            # A simple heuristic check for playlists
            self.is_playlist = "list=" in url
        else:
            self.is_playlist = is_playlist

        # Check if URL contains a valid video ID
        has_video_id = False
        try:
            extract.video_id(self.url)
            has_video_id = True
        except Exception:
            pass

        if self.is_playlist:
            try:
                print("Checking playlist details...")
                self.playlist = Playlist(self.url)
                self.playlist_title = self._sanitize_filename(self.playlist.title)
                # Create a subfolder inside self.output_dir for the playlist
                self.output_dir = os.path.join(self.output_dir, self.playlist_title)
                os.makedirs(self.output_dir, exist_ok=True)
            except Exception as e:
                if has_video_id:
                    print(f"Warning: Failed to load as playlist ({e}). Falling back to single video.")
                    self.is_playlist = False
                else:
                    print(f"Error: Failed to load as playlist ({e}) and no video ID was found in the URL.")
                    sys.exit(1)

        if not self.is_playlist:
            if not has_video_id:
                print("Error: The URL does not contain a valid YouTube video ID or playlist.")
                sys.exit(1)
            print("Checking video details...")
            self.yt = YouTube(self.url)
            self.title = self._sanitize_filename(self.yt.title)
            os.makedirs(self.output_dir, exist_ok=True)

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """
        Sanitize the video title to create a safe filename.
        """
        return re.sub(r'[\\/*?:"<>|]', "", name)

    def _download_stream(self, yt_obj, stream, filename: str) -> Optional[str]:
        """Download a stream with a progress bar and return the file path."""
        if not stream:
            return None

        # Clean title for display in progress bar
        display_title = filename if len(filename) < 30 else filename[:27] + "..."
        desc = f"Downloading: {display_title}"
        
        with tqdm(total=stream.filesize, unit="B", unit_scale=True, desc=desc, leave=False) as bar:
            def progress(_stream, chunk, _remaining):
                bar.update(len(chunk))

            yt_obj.register_on_progress_callback(progress)
            stream.download(output_path=self.output_dir, filename=filename)
            yt_obj.register_on_progress_callback(None)

        return os.path.join(self.output_dir, filename)

    def download(self):
        """
        Download the media based on the selected type.
        """
        if self.is_playlist:
            self._download_playlist()
        elif self.media_type == "audio":
            self._download_audio(self.yt, self.title)
        else:
            self._download_video(self.yt, self.title)

    def _download_playlist(self):
        """
        Download all videos in the playlist.
        """
        try:
            videos = list(self.playlist.videos)
        except Exception as e:
            print(f"Error: Failed to fetch videos in playlist ({e}).")
            return

        total_videos = len(videos)
        print(f"\n===================================================")
        print(f"Playlist Name: {self.playlist.title}")
        print(f"Total Videos : {total_videos}")
        print(f"Save Path    : {self.output_dir}")
        print(f"===================================================\n")

        for idx, video in enumerate(videos, start=1):
            try:
                # Accessing properties like .title can trigger network requests / exceptions
                title = self._sanitize_filename(video.title)
                print(f"[{idx}/{total_videos}] Processing: {title}")
                if self.media_type == "audio":
                    self._download_audio(video, title)
                else:
                    self._download_video(video, title)
            except Exception as e:
                # If resolving the video details failed
                try:
                    video_id = video.video_id
                except Exception:
                    video_id = "unknown"
                print(f"[{idx}/{total_videos}] Error processing video (ID: {video_id}): {e}")
            print("-" * 50)

    def _download_audio(self, yt_obj, title: str):
        """
        Download the audio stream and convert it to MP3.
        """
        # Get highest bitrate audio stream
        stream = (
            yt_obj.streams.filter(only_audio=True).order_by("abr").desc().first()
        )
        if not stream:
            print(f"No audio stream available for: {title}")
            return

        # Use temp file to download audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a", dir=self.output_dir) as tmp:
            temp_filepath = self._download_stream(yt_obj, stream, os.path.basename(tmp.name))

        if not temp_filepath:
            print(f"Failed to download audio stream for: {title}")
            return

        # Convert downloaded audio to MP3
        try:
            sound = AudioSegment.from_file(temp_filepath)
        except Exception as e:
            print(f"Error converting audio for '{title}': {e}")
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
            return

        duration_sec = len(sound) / 1000.0
        final_audio_path = os.path.join(self.output_dir, f"{title}.mp3")
        with tqdm(total=duration_sec, unit="sec", desc="Converting to MP3", leave=False) as bar:
            sound.export(final_audio_path, format="mp3", bitrate="128k")
            bar.update(duration_sec)

        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        print(f"Success: Audio saved to: {final_audio_path}")

    def _download_video(self, yt_obj, title: str):
        """
        Download the highest resolution video stream.
        """
        stream = yt_obj.streams.get_highest_resolution()
        if not stream:
            print(f"No video stream available for: {title}")
            return

        video_filename = f"{title}.mp4"
        video_filepath = self._download_stream(yt_obj, stream, video_filename)
        if video_filepath:
            print(f"Success: Video saved to: {video_filepath}")
        else:
            print(f"Failed to download video stream for: {title}")


def parse_args():
    parser = argparse.ArgumentParser(description="Download YouTube videos or playlists as audio or video.")
    parser.add_argument("url", help="YouTube video or playlist URL")
    parser.add_argument("--type", choices=["audio", "video"], default="audio",
                        help="Type of media to download (default: audio)")
    parser.add_argument("--output_dir", default="outputs",
                        help="Directory to save downloads (default: outputs)")
    parser.add_argument("--playlist", action="store_true", default=False,
                        help="Force treating the URL as a playlist")
    parser.add_argument("--single", action="store_true", default=False,
                        help="Force treating the URL as a single video")
    return parser.parse_args()


def main():
    args = parse_args()
    
    # Resolve override flags
    is_playlist = None
    if args.playlist:
        is_playlist = True
    elif args.single:
        is_playlist = False

    downloader = YouTubeDownloader(
        url=args.url, 
        media_type=args.type, 
        output_dir=args.output_dir,
        is_playlist=is_playlist
    )
    downloader.download()


if __name__ == "__main__":
    main()
