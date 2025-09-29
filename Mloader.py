#!/usr/bin/env python3
import sys
import os
import yt_dlp
import validators
import re
import argparse
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC, TDRC
from urllib.request import urlopen

DEFAULT_DOWNLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'Music', 'Mloader')

def sanitize_filename(filename):
    """Removes invalid characters from a filename."""
    return re.sub(r'[\\/*?:"<>|]',"", filename)

def get_safe_filename(download_folder, base_filename, extension):
    """Generates a safe, unique filename, handling existing files."""
    sanitized_base = sanitize_filename(base_filename)
    new_filename = f"{sanitized_base}.{extension}"
    counter = 1
    while os.path.exists(os.path.join(download_folder, new_filename)):
        new_filename = f"{sanitized_base} ({counter}).{extension}"
        counter += 1
    return new_filename

def preview_downloads(url):
    """Previews the songs to be downloaded from a given URL."""
    ydl_opts = {
        'quiet': True,
        'extract_flat': 'in_playlist',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                print("Songs to be downloaded:")
                for idx, entry in enumerate(info['entries'], 1):
                    print(f"{idx}. {entry['title']}")
            else:
                print("Song to be downloaded:")
                print(f"1. {info['title']}")
            print()
            return info
        except Exception as e:
            print(f"Error previewing downloads: {str(e)}")
            sys.exit(1)

def download_song(url, download_folder):
    """Downloads a single song, ensuring a unique filename."""
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': False, 'playlist_items': '1'}) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                info = info['entries'][0]
    except Exception as e:
        print(f"Error fetching video info: {str(e)}")
        return None, None

    safe_mp3_filename = get_safe_filename(download_folder, info['title'], 'mp3')
    final_path = os.path.join(download_folder, safe_mp3_filename)
    final_path_without_ext, _ = os.path.splitext(final_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{final_path_without_ext}.%(ext)s',
        'quiet': True,
        'writethumbnail': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }, {
            'key': 'EmbedThumbnail',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return info, final_path
    except Exception as e:
        print(f"Error during download for {info.get('title', 'Unknown Title')}: {str(e)}")
        return None, None

def process_metadata(filename, info):
    """Writes comprehensive ID3 tags to the MP3 file."""
    try:
        audio = ID3(filename)
        audio['TIT2'] = TIT2(encoding=3, text=info.get('title', 'Unknown Title'))
        audio['TPE1'] = TPE1(encoding=3, text=info.get('uploader', 'Unknown Artist'))
        audio['TALB'] = TALB(encoding=3, text=info.get('album', info.get('playlist_title', 'Unknown Album')))

        if info.get('upload_date'):
            audio['TDRC'] = TDRC(encoding=3, text=info['upload_date'][:4])

        if 'thumbnail' in info and not audio.getall('APIC'):
            with urlopen(info['thumbnail']) as art:
                audio['APIC'] = APIC(
                    encoding=3,
                    mime='image/jpeg',
                    type=3,
                    desc='Cover',
                    data=art.read()
                )
        audio.save(v2_version=3)
    except Exception as e:
        print(f"Error processing metadata for {info.get('title', 'Unknown Title')}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Download audio from YouTube videos and playlists.")
    parser.add_argument('url', nargs='?', default=None, help="The URL of the video or playlist.")
    parser.add_argument('-o', '--output', default=DEFAULT_DOWNLOAD_FOLDER, help=f"The folder to download songs to. Defaults to {DEFAULT_DOWNLOAD_FOLDER}")
    args = parser.parse_args()

    download_folder = args.output
    os.makedirs(download_folder, exist_ok=True)

    url = args.url
    if not url:
        url = input("Enter the URL of the song or playlist: ")

    if not validators.url(url):
        print("Invalid URL. Please provide a valid URL.")
        return

    playlist_info = preview_downloads(url)
    if not playlist_info:
        return

    if 'entries' in playlist_info:
        total_tracks = len(playlist_info['entries'])
        for idx, entry in enumerate(playlist_info['entries'], 1):
            print(f"Downloading ({idx}/{total_tracks}): {entry['title']}")
            song_info, song_path = download_song(entry['url'], download_folder)
            if song_info and song_path:
                song_info['playlist_title'] = playlist_info.get('title')
                process_metadata(song_path, song_info)
                print(f"Finished: {os.path.basename(song_path)}")
    else:
        print(f"Downloading: {playlist_info['title']}")
        song_info, song_path = download_song(playlist_info['webpage_url'], download_folder)
        if song_info and song_path:
            process_metadata(song_path, song_info)
            print(f"Finished: {os.path.basename(song_path)}")

if __name__ == "__main__":
    main()
