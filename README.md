# Mloader

A Python script for downloading YouTube videos/playlists and converting them to high-quality MP3 files with metadata.

## Features

- Downloads from YouTube videos and playlists
- Converts to 192kbps MP3 format
- Automatically embeds video thumbnails as album art
- Adds ID3 metadata (title, artist, album)
- Preview downloads before starting
- Handles duplicate filenames
- Input validation for URLs

## Requirements

- Python 3.9+
- `yt-dlp`, `mutagen`, `validators`, `ffmpeg-python` (install via `python3 Mloader.py install`)
- FFmpeg for audio conversion:

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

## Usage

1. (Optional) Refresh the script and dependencies:
   ```bash
   python3 Mloader.py install    # first-time setup; pulls latest script + Python deps
   python3 Mloader.py update     # later updates; also reminds you about FFmpeg
   ```

2. Run the downloader:
```bash
python3 Mloader.py [URL]             # default output: ~/Music/Mloader
python3 Mloader.py [URL] -o /path    # custom download folder
```
Or run without arguments to input URL when prompted.

3. The script will:
   - Preview content to be downloaded
   - Download and convert videos to MP3
   - Add metadata and album art
   - Save files to the specified folder

## Error Handling

- Validates URLs before processing
- Handles download/conversion errors gracefully
- Prevents filename conflicts
- Reports specific errors for troubleshooting

## Legal Note

Check your local laws regarding YouTube downloads. Use responsibly and respect copyright.
