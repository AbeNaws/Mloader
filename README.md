# Mloader - YouTube to MP3 Downloader

## Overview

Mloader is a Python script that allows downloading YouTube videos and playlists and converting them to MP3 files. It utilizes the PyTube and MoviePy libraries.

The script has the following features:

- Accept a YouTube video URL or playlist URL as input
- Download the video(s) as MP4 files
- Convert the MP4 files to MP3 
- Add ID3 metadata tags (title, artist) to the MP3 files
- Download and embed the video thumbnail as album art in the MP3 file

## Requirements

Mloader requires the following Python packages:

- PyTube
- MoviePy 
- FFmpeg

Install them via pip:

```
pip install pytube moviepy ffmpeg-python ffmpeg
```

Note, you may need to install ffmpeg on linux:
```
sudo apt install ffmpeg
```
## Usage

1. Set the `downloaded_songs_folder` and `converted_songs_folder` variables to the desired download locations.

2. Run Mloader:

```
python mloader.py
```

3. Enter a YouTube video or playlist URL when prompted. 

4. Mloader will display the video title(s) and download the videos to the `downloaded_songs_folder`.

5. It will then convert them to MP3 and move them to the `converted_songs_folder`. Metadata and thumbnails will be added. 

6. The downloaded videos will be deleted after conversion.

## Functions

- `create_folders()` - Creates the download and converted folders if they don't exist.

- `display_playlist()` - Prints the playlist title and video titles.

- `display_single_video()` - Prints the video title. 

- `process_video()` - Downloads, converts, and adds metadata for a single video.

- The main logic checks for a playlist or single video and calls the appropriate functions.

## Notes

- Mloader requires FFmpeg to be installed and accessible on the PATH.

- Downloading copyrighted material may be illegal in your country. Use at your own risk. 

- Thumbnails and metadata may not always be available for some videos.

- Temporary folders are created during processing and deleted after completion.
