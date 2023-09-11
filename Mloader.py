#!/usr/bin/env python
import os
import subprocess
from time import sleep
from pytube import Playlist, YouTube
from moviepy.editor import *

downloaded_songs_folder = '' #ie. /home/user/Music/temp"
converted_songs_folder = '' #ie. /home/user/Music/Mloader"

# If needed folders don't exist, create them
def create_folders():
    if not os.path.exists(downloaded_songs_folder):
        os.makedirs(downloaded_songs_folder)
    if not os.path.exists(converted_songs_folder):
        os.makedirs(converted_songs_folder)

# Display songs in playlist
def display_playlist(playlist):
    print(f'Number Of Songs In playlist: {len(playlist.video_urls)}')
    print('-' * len(playlist.title))
    print(playlist.title)
    print('-' * len(playlist.title))
    for video in playlist.video_urls:
        yt = YouTube(video)
        print(yt.title)
    print()
    sleep(2)

# Display song
def display_single_video(yt):
    print('-' * len(yt.title) + '------')
    print(f'Song: {yt.title}')
    print('-' * len(yt.title) + '------')


def process_video(video, downloaded_songs_folder, converted_songs_folder):
    # Download the video
    print(f'Downloading: {video.title}')
    audio_stream = video.streams.filter(only_audio=True).first()
    audio_stream.download(output_path=downloaded_songs_folder)

    # Convert the downloaded video to MP3 and add metadata
    for file in os.listdir(downloaded_songs_folder):
        if file.endswith(".mp4"):
            video_path = os.path.join(downloaded_songs_folder, file)
            mp3_path = os.path.join(converted_songs_folder, f"{file[:-4]}.mp3")
            try:
                video = VideoFileClip(video_path)
                subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "panic",
                                "-i", video_path, "-vn", "-acodec", "copy", mp3_path], check=True)
                os.remove(video_path)
            except KeyError:
                audio = AudioFileClip(video_path)
                audio.write_audiofile(mp3_path, verbose=False)
                os.remove(video_path)

            # Download the thumbnail
            thumbnail_url = video.thumbnail_url
            thumbnail_path = "thumbnail.jpg"
            subprocess.run(["wget", "-O", thumbnail_path, thumbnail_url],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Add metadata and thumbnail to the MP3 file
            temp_path = os.path.join(
                converted_songs_folder, f"temp_{file[:-4]}.mp3")
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "panic", "-i", mp3_path, "-i", thumbnail_path, "-c", "copy",
                "-metadata", f"title={video.title}", "-metadata", f"artist={video.author}",
                "-map", "0", "-map", "1", "-id3v2_version", "3", temp_path
            ], check=True)

            # Replace the original MP3 file with the updated one
            os.remove(mp3_path)
            os.rename(temp_path, mp3_path)

            # Remove the downloaded thumbnail
            os.remove(thumbnail_path)

# Check that the file destinations have been set
if downloaded_songs_folder == '' or converted_songs_folder == '':
    print('Add locations for folders')
    quit()

# Url input
url = input('Url: ')

# Determine if playlist or single song
if 'playlist' in url or 'list' in url:
    playlist = Playlist(url)
    display_playlist(playlist)
    create_folders()
    for video in playlist.videos:
        process_video(video, downloaded_songs_folder, converted_songs_folder)
else:
    yt = YouTube(url)
    display_single_video(yt)
    create_folders()
    process_video(yt, downloaded_songs_folder, converted_songs_folder)

# Remove temporary folder
if os.path.exists(downloaded_songs_folder):
    os.rmdir(downloaded_songs_folder)
