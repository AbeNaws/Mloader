#!/usr/bin/env python
########################Disclaimer:########################
#Mloader is provided for educational and personal use only. 
#Downloading copyrighted content without permission may be 
#illegal in your jurisdiction.The authors do not encourage 
#or condone using this software for illegal activity. Users 
#accept full responsibility for determining whether their use
#of this software complies with applicable laws in their region.
#The authors provide this software as-is without warranty and 
#accept no liability for damages resulting from its use. 
#By using this software, you agree to these terms.
##########################################################

import sys
import os
import yt_dlp
import validators
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from urllib.request import urlopen

# Set the download folder
DOWNLOAD_FOLDER = '/home/user/Music/Mloader'

def preview_downloads(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': 'in_playlist',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            
            if 'entries' in info:
                # Playlist
                print("Songs to be downloaded:")
                for idx, entry in enumerate(info['entries'], 1):
                    print(f"{idx}. {entry['title']}")
            else:
                # Single video
                print("Song to be downloaded:")
                print(f"1. {info['title']}")
            
            print()  # Add a blank line after the list
            return info
        except Exception as e:
            print(f"Error previewing downloads: {str(e)}")
            sys.exit(1)

def get_safe_filename(base_filename, extension):
    counter = 1
    new_filename = f"{base_filename}.{extension}"
    while os.path.exists(os.path.join(DOWNLOAD_FOLDER, new_filename)):
        if counter == 1:
            return new_filename  # Return the original filename for the first occurrence
        new_filename = f"{base_filename} ({counter}).{extension}"
        counter += 1
    return new_filename

def download_and_convert(info):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
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

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if 'entries' in info:
            # Playlist
            for entry in info['entries']:
                try:
                    print(f"Downloading: {entry['title']}")
                    ydl.download([entry['url']])
                    process_file(entry)
                except Exception as e:
                    print(f"Error downloading {entry['title']}: {str(e)}")
        else:
            # Single video
            try:
                print(f"Downloading: {info['title']}")
                ydl.download([info['webpage_url']])
                process_file(info)
            except Exception as e:
                print(f"Error downloading {info['title']}: {str(e)}")

def process_file(info):
    base_filename = info['title']
    safe_filename = get_safe_filename(base_filename, 'mp3')
    filename = os.path.join(DOWNLOAD_FOLDER, safe_filename)
    
    # Rename the file if it's different from the original filename
    original_filename = os.path.join(DOWNLOAD_FOLDER, f"{base_filename}.mp3")
    if original_filename != filename and os.path.exists(original_filename):
        os.rename(original_filename, filename)

    # Add metadata
    try:
        audio = EasyID3(filename)
        audio['title'] = info['title']
        audio['artist'] = info['uploader']
        audio['album'] = info.get('album', 'Unknown Album')
        audio.save()

    except Exception as e:
        print(f"Error processing metadata for {info['title']}: {str(e)}")

def is_valid_url(url):
    return validators.url(url)

def main():
    # Create the download folder if it doesn't exist
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter the URL of the song or playlist: ")

    if not is_valid_url(url):
        print("Invalid URL. Please provide a valid URL.")
        return

    info = preview_downloads(url)
    if info:
        download_and_convert(info)

if __name__ == "__main__":
    main()
