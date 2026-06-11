#!/usr/bin/env python3
"""
Universal Audio Converter Script

This script converts audio files (single files or entire directories) between various formats
(MP3, WAV, FLAC, M4A, OGG, OPUS, etc.) using pydub.

Usage:
    python universal_converter.py <input_path> --to {mp3,wav,flac,m4a,ogg} [--bitrate BITRATE] [--output_dir OUTPUT_DIR]
"""

import os
import sys
import argparse
from typing import List

# Ensure required libraries are installed
try:
    from pydub import AudioSegment
except ImportError:
    print("Error: 'pydub' module is not installed. Install it with 'pip install pydub'.")
    sys.exit(1)

try:
    from tqdm import tqdm
except ImportError:
    print("Error: 'tqdm' module is not installed. Install it with 'pip install tqdm'.")
    sys.exit(1)


SUPPORTED_OUTPUTS = ["mp3", "wav", "flac", "m4a", "ogg"]
DEFAULT_BITRATES = {
    "mp3": "192k",
    "m4a": "192k",
    "ogg": "192k",
    "wav": None,   # WAV doesn't use bitrate (PCM)
    "flac": None   # FLAC uses lossless compression level
}


class UniversalAudioConverter:
    def __init__(self, input_path: str, target_format: str, bitrate: str = None, output_dir: str = None):
        self.input_path = input_path
        self.target_format = target_format.lower().strip(".")
        self.bitrate = bitrate or DEFAULT_BITRATES.get(self.target_format)
        
        if self.target_format not in SUPPORTED_OUTPUTS:
            raise ValueError(f"Target format '{self.target_format}' is not supported. Choose from {SUPPORTED_OUTPUTS}")

        # Set default output directory if not provided
        if output_dir:
            self.output_dir = output_dir
        else:
            self.output_dir = os.path.join("outputs", "converted", self.target_format)
            
        os.makedirs(self.output_dir, exist_ok=True)

    def run(self):
        if os.path.isdir(self.input_path):
            self._convert_directory()
        elif os.path.isfile(self.input_path):
            self._convert_file(self.input_path)
        else:
            print(f"Error: Input path '{self.input_path}' does not exist.")

    def _get_all_audio_files(self, directory: str) -> List[str]:
        """Find all files in a directory that are likely audio files."""
        audio_extensions = {
            ".mp3", ".wav", ".flac", ".m4a", ".ogg", ".opus", 
            ".aac", ".wma", ".webm", ".mp4", ".m4r", ".amr"
        }
        audio_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in audio_extensions:
                    audio_files.append(os.path.join(root, file))
        return audio_files

    def _convert_file(self, file_path: str):
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        ext = os.path.splitext(file_path)[1].lower().strip(".")
        output_file = os.path.join(self.output_dir, f"{base_name}.{self.target_format}")
        
        # Avoid converting a file to the exact same format in the same place
        if ext == self.target_format and os.path.dirname(file_path) == os.path.abspath(self.output_dir):
            print(f"Skipping: '{file_path}' is already in the target format in the output directory.")
            return

        print(f"\nConverting: {os.path.basename(file_path)} -> {self.target_format.upper()}")
        
        try:
            # Read the audio file (pydub auto-detects formats via ffmpeg)
            # Special formats like opus might need format hint, but from_file generally handles it
            sound = AudioSegment.from_file(file_path)
            duration_sec = len(sound) / 1000.0
            
            # Export with progress bar
            with tqdm(total=duration_sec, unit="sec", desc="Processing", leave=False) as bar:
                if self.target_format in ["mp3", "m4a", "ogg"]:
                    sound.export(output_file, format=self.target_format, bitrate=self.bitrate)
                else:
                    # WAV or FLAC (lossless)
                    sound.export(output_file, format=self.target_format)
                bar.update(duration_sec)
                
            print(f"Success: Saved to {output_file}")
        except Exception as e:
            print(f"Error converting '{os.path.basename(file_path)}': {e}")

    def _convert_directory(self):
        print(f"Scanning directory: {self.input_path}...")
        files = self._get_all_audio_files(self.input_path)
        total_files = len(files)
        
        if total_files == 0:
            print("No audio files found in the directory.")
            return

        print(f"Found {total_files} audio files. Starting conversion to {self.target_format.upper()}...")
        print(f"Output folder: {self.output_dir}")
        print("===================================================")
        
        for idx, file in enumerate(files, start=1):
            print(f"\n[{idx}/{total_files}] ", end="")
            self._convert_file(file)
            print("-" * 50)
            
        print("\nBatch conversion complete!")


def parse_args():
    parser = argparse.ArgumentParser(description="Universal Audio Converter using pydub.")
    parser.add_argument("input", help="Path to input audio file or directory")
    parser.add_argument("--to", choices=SUPPORTED_OUTPUTS, required=True,
                        help="Target audio format")
    parser.add_argument("--bitrate", help="Audio bitrate (e.g. 192k, 256k, 320k) for MP3/M4A/OGG")
    parser.add_argument("--output_dir", help="Directory to save output files")
    return parser.parse_args()


def run_interactive_wizard():
    print("===================================================")
    print("           UNIVERSAL AUDIO CONVERTER")
    print("===================================================")
    print()
    
    # 1. Get input path
    while True:
        input_path = input("Masukkan file atau folder audio yang ingin diconvert: ").strip('"').strip("'")
        if os.path.exists(input_path):
            break
        print("Path tidak ditemukan! Silakan masukkan path yang valid.")
        print()

    # 2. Get target format
    print()
    print("Pilih format output target:")
    for idx, fmt in enumerate(SUPPORTED_OUTPUTS, start=1):
        print(f"  [{idx}] {fmt.upper()}")
        
    while True:
        choice = input("Pilih nomor format (1-5): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(SUPPORTED_OUTPUTS):
            target_format = SUPPORTED_OUTPUTS[int(choice) - 1]
            break
        print("Pilihan tidak valid! Silakan masukkan nomor antara 1 sampai 5.")

    # 3. Custom output folder (Optional)
    print()
    output_dir = input("Masukkan folder output (tekan Enter untuk default 'outputs/converted'): ").strip()
    if output_dir == "":
        output_dir = None

    # Run the converter
    try:
        converter = UniversalAudioConverter(
            input_path=input_path,
            target_format=target_format,
            output_dir=output_dir
        )
        converter.run()
    except Exception as e:
        print(f"Error: {e}")
        
    print()
    input("Proses selesai. Tekan Enter untuk keluar...")


def main():
    # If no arguments passed, run the wizard
    if len(sys.argv) == 1:
        run_interactive_wizard()
    else:
        args = parse_args()
        try:
            converter = UniversalAudioConverter(
                input_path=args.input,
                target_format=args.to,
                bitrate=args.bitrate,
                output_dir=args.output_dir
            )
            converter.run()
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
