import os
from pydub import AudioSegment
import argparse

def ensure_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def convert_opus_to_mp3(input_file, output_dir):
    ensure_dir(output_dir)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_path = os.path.join(output_dir, base_name + ".mp3")
    try:
        # Coba baca sebagai opus, kalo gagal baru coba ogg
        try:
            audio = AudioSegment.from_file(input_file, format="opus")
        except Exception:
            audio = AudioSegment.from_file(input_file, format="ogg")
        audio.export(output_path, format="mp3", bitrate="128k")
        print(f"Sukses convert: {input_file} -> {output_path}")
    except Exception as e:
        print(f"Gagal convert {input_file}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Convert .opus ke .mp3, biar gaul dan bisa diputer di hape jadul!")
    parser.add_argument("input", help="File .opus yang mau diconvert (pakai tanda petik kalau ada spasi)")
    parser.add_argument("--output_dir", default="outputs/mp3", help="Folder output (default: outputs/mp3)")
    args = parser.parse_args()
    convert_opus_to_mp3(args.input, args.output_dir)

if __name__ == "__main__":
    main()
