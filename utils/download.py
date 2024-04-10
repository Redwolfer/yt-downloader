from pytube import YouTube, Playlist
from pytube.cli import on_progress
import os
import moviepy.editor as mp
import yaml

with open('../config.yml', 'r') as file:
    config = yaml.safe_load(file)

def mp4(url):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        video = yt.streams.filter(file_extension="mp4").get_highest_resolution()
        print()
        print(f"Downloading video: {yt.title}.mp4")
        if not os.path.exists(config['output_path_mp4']):
            os.makedirs(config['output_path_mp4'])
        video.download(output_path=config['output_path_mp4'])
    except():
        print('Error downloading MP4')
        
    
def mp3(url):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        audio = yt.streams.filter(only_audio=True).first()
        print()
        print(f"Downloading audio: {yt.title}.mp3")
        if not os.path.exists(config['output_path_mp3']):
            os.makedirs(config['output_path_mp3'])
        audio.download(output_path=config['output_path_mp3'], filename="temp_audio")
        clip = mp.AudioFileClip(config['output_path_mp3'] + '/temp_audio')
        clip.write_audiofile(config['output_path_mp3'] + '/' + yt.title + '.mp3')
        os.remove(config['output_path_mp3'] + '/temp_audio')
    except():
        print('Error downloading MP3')
    
def wav(url):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        audio = yt.streams.filter(only_audio=True).first()
        print()
        print(f"Downloading audio: {yt.title}.wav")
        if not os.path.exists(config['output_path_wav']):
            os.makedirs(config['output_path_wav'])
        audio.download(output_path=config['output_path_wav'], filename="temp_audio")
        clip = mp.AudioFileClip(config['output_path_wav'] + '/temp_audio')
        clip.write_audiofile(config['output_path_wav'] + '/' + yt.title + '.wav')
        os.remove(config['output_path_wav'] + '/temp_audio')
    except():
        print('Error downloading WAV')
    
def mp3_playlist(playlist_url):
    playlist = Playlist(playlist_url)
    if playlist:
        for url in playlist.video_urls:
            mp3(url)
        print()
        print("All MP3 playlist downloads completed.")
    else:
        print("Playlist is empty or not exists.")

def mp4_playlist(playlist_url):
    playlist = Playlist(playlist_url)
    if playlist:
        for url in playlist.video_urls:
            mp4(url)
        print()
        print("All MP4 playlist downloads completed.")
    else:
        print("Playlist is empty or not exists.")
        
def wav_playlist(playlist_url):
    playlist = Playlist(playlist_url)
    if playlist:
        for url in playlist.video_urls:
            wav(url)
        print()
        print("All WAV playlist downloads completed.")
    else:
        print("Playlist is empty or not exists.")
        
def mp3_lists():
    try:
        url_list_file = open(config['url_list'], 'r')
        urls = url_list_file.read().splitlines()
        if urls:
            for url in urls:
                mp3(url)
            print()
            print("All MP3 downloads completed.")
        else:
            print("List is empty")
    except():
        print("Error opening url download list.")
        
        
def mp4_lists():
    try:
        url_list_file = open(config['url_list'], 'r')
        urls = url_list_file.read().splitlines()
        if urls:
            for url in urls:
                mp4(url)
            print()
            print("All MP4 downloads completed.")
        else:
            print("List is empty")
    except():
        print("Error opening url download list.")

def wav_lists():
    try:
        url_list_file = open(config['url_list'], 'r')
        urls = url_list_file.read().splitlines()
        if urls:
            for url in urls:
                wav(url)
            print()
            print("All WAV downloads completed.")
        else:
            print("List is empty")
    except():
        print("Error opening url download list.")
        