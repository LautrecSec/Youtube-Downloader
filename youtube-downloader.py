from pytube import YouTube
from moviepy.editor import *

def download_and_convert_audio(video_url, output_path='./', output_filename='audio'):
    # Create a YouTube object
    yt = YouTube(video_url)
    
    # Select the highest quality audio stream
    audio_stream = yt.streams.filter(only_audio=True).first()
    
    # Download the audio stream
    audio_stream.download(filename=output_filename, output_path=output_path)
    
    # Convert to MP3 using moviepy
    webm_file = f"{output_path}/{output_filename}.webm"
    mp3_file = f"{output_path}/{output_filename}.mp3"
    
    video = VideoFileClip(webm_file)
    video.audio.write_audiofile(mp3_file)

if __name__ == "__main__":
    # Prompt the user for the URL of the video to download
    video_url = input("Please enter the YouTube video URL: ")
    
    # Call the function to download and convert audio
    download_and_convert_audio(video_url)
