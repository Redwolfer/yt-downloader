# YouTube Downloader

A Python script that allows you to download YouTube videos and audio directly from the command line.

## Features

- Download YouTube videos in MP4 format with the highest resolution available.
- Download YouTube audio in either MP3 or WAV format.

## Requirements

- Python 3.x
- Install required Python packages.

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/1772012/yt_downloader.git
    ```

2. **Navigate to Project Directory**

    ```bash
    cd yt-downloader
    ```

3. **Install Requirements**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

You can run the script using command-line arguments:

### Download Video

```bash
python yt-downloader.py [URL] -v
```

### Download Audio in MP3

```bash
python yt-downloader.py [URL] -a mp3
```

### Download Audio in WAV

```bash
python yt-downloader.py [URL] -a wav
```

Replace [URL] with the actual YouTube video URL.

### Project Structure
```
youtube_downloader/
├── src/
│   ├── __init__.py
│   └── yt-downloader.py
├── requirements.txt
└── README.md
```

### License

This project is licensed under the MIT License

