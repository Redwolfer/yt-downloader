import argparse
import utils.download as dwn

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download YouTube video or audio in various formats.')
    parser.add_argument('url', action='store_true', help='YouTube URL to download')
    parser.add_argument('-mp3', action='store_true', help='Download audio as MP3')
    parser.add_argument('-mp4', action='store_true', help='Download video as MP4')
    parser.add_argument('-wav', action='store_true', help='Download audio as WAV')
    parser.add_argument('-p', '--playlist', action='store_true', help='Indicates the URL is a playlist')
    parser.add_argument('-l', '--lists', action='store_true', help='Indicates the lists of URLs')

    args = parser.parse_args()

    if args.playlist:
        if args.mp3:
            dwn.mp3_playlist(args.url)
        elif args.mp4:
            dwn.mp4_playlist(args.url)
        elif args.wav:
            dwn.wav_playlist(args.url)
        else:
            print("Please specify the format to download with a playlist: -mp3, -mp4, or -wav")
    else:
        if args.lists:
            if args.mp3:
                dwn.mp3_lists()
            elif args.mp4:
                dwn.mp4_lists()
            elif args.wav:
                dwn.wav_lists()
            else:
                print("Please specify the format to download: -mp3, -mp4, or -wav")
        else:
            if args.mp3:
                dwn.mp3(args.url)
            elif args.mp4:
                dwn.mp4(args.url)
            elif args.wav:
                dwn.wav(args.url)
            else:
                print("Please specify the format to download: -mp3, -mp4, or -wav")
        