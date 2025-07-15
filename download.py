#!/usr/bin/env python3
"""
YouTube Downloader Script

This script downloads a YouTube video as either audio or video.
Audio files are converted to MP3 format after downloading.

Usage:
    python yt_downloader.py <url> [--type {audio,video}] [--output_dir OUTPUT_DIR]
"""

import os
import re
import argparse
import sys
from tqdm import tqdm

# Ensure the required module is available.
try:
    from pytubefix import YouTube
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
    def __init__(self, url: str, media_type: str = "audio", output_dir: str = "outputs"):
        """
        Initialize the downloader with a YouTube URL, media type, and output directory.
        """
        self.url = url
        self.media_type = media_type.lower()
        self.output_dir = os.path.join(output_dir, self.media_type)
        os.makedirs(self.output_dir, exist_ok=True)
        self.yt = YouTube(self.url)
        self.title = self.sanitize_filename(self.yt.title)

    @staticmethod
    def sanitize_filename(name: str) -> str:
        """
        Sanitize the video title to create a safe filename.
        """
        return re.sub(r'[\\/*?:"<>|]', "", name)

    def _on_progress(self, download_bar: tqdm):
        """
        Returns a callback function to update the progress bar.
        """
        def callback(stream, chunk, bytes_remaining):
            download_bar.update(len(chunk))
        return callback

    def download(self):
        """
        Download the media based on the selected type.
        """
        if self.media_type == "audio":
            self._download_audio()
        else:
            self._download_video()

    def _download_audio(self):
        """
        Download the audio stream and convert it to MP3.
        """
        stream = self.yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        if not stream:
            print("No audio stream available.")
            return

        filesize = stream.filesize
        download_bar = tqdm(total=filesize, unit='B', unit_scale=True,
                            desc=f"Downloading: {self.title}")
        self.yt.register_on_progress_callback(self._on_progress(download_bar))

        temp_filename = "temp.m4a"
        temp_filepath = os.path.join(self.output_dir, temp_filename)
        stream.download(output_path=self.output_dir, filename=temp_filename)
        download_bar.close()

        # Convert downloaded audio to MP3
        try:
            sound = AudioSegment.from_file(temp_filepath)
        except Exception as e:
            print(f"Error converting audio: {e}")
            os.remove(temp_filepath)
            return

        duration_sec = len(sound) / 1000.0
        conversion_bar = tqdm(total=duration_sec, unit='sec', desc="Converting audio")
        final_audio_path = os.path.join(self.output_dir, f"{self.title}.mp3")
        sound.export(final_audio_path, format="mp3", bitrate="128k")
        conversion_bar.update(duration_sec)
        conversion_bar.close()

        os.remove(temp_filepath)
        print(f"Audio downloaded and converted to: {final_audio_path}")

    def _download_video(self):
        """
        Download the highest resolution video stream.
        """
        stream = self.yt.streams.get_highest_resolution()
        if not stream:
            print("No video stream available.")
            return

        filesize = stream.filesize
        download_bar = tqdm(total=filesize, unit='B', unit_scale=True,
                            desc=f"Downloading: {self.title}")
        self.yt.register_on_progress_callback(self._on_progress(download_bar))

        video_filename = f"{self.title}.mp4"
        video_filepath = os.path.join(self.output_dir, video_filename)
        stream.download(output_path=self.output_dir, filename=video_filename)
        download_bar.close()

        print(f"Video downloaded as: {video_filepath}")


def parse_args():
    parser = argparse.ArgumentParser(description="Download YouTube videos as audio or video.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--type", choices=["audio", "video"], default="audio",
                        help="Type of media to download (default: audio)")
    parser.add_argument("--output_dir", default="outputs",
                        help="Directory to save downloads (default: outputs)")
    return parser.parse_args()


def main():
    args = parse_args()
    downloader = YouTubeDownloader(url=args.url, media_type=args.type, output_dir=args.output_dir)
    downloader.download()


if __name__ == "__main__":
    main()
