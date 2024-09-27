import os
import yt_dlp

# Ask the user to input multiple video URLs separated by commas
video_urls = input("Enter video URLs separated by commas: ").split(',')

# Path to the Downloads folder (adjust path for your environment)
download_path = '/storage/emulated/0/Download'

# Function to get available formats and allow the user to choose
def choose_format(video_url):
    # yt-dlp options to list available formats without downloading
    ydl_opts = {
        'listformats': True
    }

    # Extract video information and list formats
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        formats = info_dict.get('formats', [])

    # Display available formats with a number for selection
    print(f"\nAvailable formats for {info_dict.get('title')}:")
    for i, f in enumerate(formats, start=1):
        print(f"{i}. Format code: {f['format_id']}, Quality: {f['format']}, Resolution: {f.get('height', 'Unknown')}p")

    # Ask the user to select a format number
    choice = int(input("Enter the number of the format you want to download: "))
    
    # Return the selected format code
    selected_format = formats[choice - 1]['format_id']
    return selected_format

# Loop through each video URL
for video_url in video_urls:
    video_url = video_url.strip()  # Remove leading/trailing spaces

    # Get the format code selected by the user
    format_code = choose_format(video_url)

    # yt-dlp options to download the selected format using aria2c
    ydl_opts = {
        'format': format_code,  # Download the selected format
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),  # Save in Downloads folder
        'external_downloader': 'aria2c',  # Use aria2c as the downloader
        'external_downloader_args': ['-x', '16', '-k', '1M']  # 16 connections, 1M chunk size
    }

    # Download the video in the selected quality using aria2c for speed
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    print(f"Video downloaded in the selected quality and saved to {download_path}.\n")
