import argparse
from pytube import YouTube, exceptions
import re
import os
import moviepy.editor as mp

def validate_url(url):
    youtube_url_validation = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    return youtube_url_validation.match(url)

def download_video(url):
    yt = YouTube(url)
    video = yt.streams.filter(file_extension="mp4").get_highest_resolution()
    print(f"Downloading video: {yt.title}")
    video.download(output_path="../videos")
    
def download_audio(url, audio_format):
    yt = YouTube(url)
    audio = yt.streams.filter(only_audio=True).first()
    print(f"Downloading audio: {yt.title}")
    audio.download(output_path="../audios", filename="temp_audio")

    if audio_format == "mp3":
        clip = mp.AudioFileClip("../audios/temp_audio")
        clip.write_audiofile(f"../audios/{yt.title}.mp3")
    elif audio_format == "wav":
        clip = mp.AudioFileClip("../audios/temp_audio")
        clip.write_audiofile(f"../audios/{yt.title}.wav")

    os.remove(f"../audios/temp_audio")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube video or audio.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-v", "--video", help="Download video", action="store_true")
    parser.add_argument("-a", "--audio", help="Download audio", choices=['mp3', 'wav'])
    
    args = parser.parse_args()

    if not validate_url(args.url):
        print("Invalid YouTube URL.")
        exit(1)

    if args.video:
        download_video(args.url)
    elif args.audio:
        download_audio(args.url, args.audio)
    else:
        print("Please specify whether to download video (-v) or audio (-a) and its format.")