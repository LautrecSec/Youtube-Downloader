# Youtube downloader to MP3 script

from pytube import YouTube
import os

# URL input prompt
yt = YouTube(input("Enter the URL of the video you want to download: \n>> "))

# Extract audio only
video = yt.streams.filter(only_audio=True).first()

# Replace destination with the path where you want to save the downloaded file
# Select your destination folder (e.g "C:\\Temp\)
destination = ""

# Download the file
out_file = video.download(output_path=destination)

# Save the file
base, ext = os.path.splitext(out_file)
new_file = base + '.mp3'
os.rename(out_file, new_file)

# Download Status
print(yt.title + " has been downloaded successfully.")

