# Import necessary modules
import os
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from pytube import YouTube, exceptions
from moviepy.editor import AudioFileClip

# The DownloadThread class is used to create a separate thread for downloading the video
class DownloadThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, url, folder, stream_type):
        super().__init__()
        self.url = url.strip()  # The YouTube URL to download
        self.folder = folder  # The folder to download the video to
        self.stream_type = stream_type  # The type of stream to download ('audio' or 'video')

    # The code in this method is run when the thread is started
    def run(self):
        try:
            # Create a YouTube object for the URL
            yt = YouTube(self.url)
            
            # Choose the first stream of the correct type (audio or video)
            if self.stream_type == 'audio':
                stream = yt.streams.filter(only_audio=True).first()
            else:
                stream = yt.streams.filter(progressive=True).first()

            # Download the stream and convert it to MP3 format if it's an audio stream
            if stream:
                download_path = stream.download(self.folder)
                if self.stream_type == 'audio':
                    mp3_path = os.path.splitext(download_path)[0] + '.mp3'
                    clip = AudioFileClip(download_path)
                    clip.write_audiofile(mp3_path)
                    clip.close()
                    if os.path.exists(download_path):
                        os.remove(download_path)
            else:
                print(f"No {self.stream_type} stream found for URL: {self.url}")

        # Handle PytubeError exceptions
        except exceptions.PytubeError as e:
            print(f"PytubeError encountered: {str(e)}")

# The Downloader class is the main application window
class Downloader(QWidget):
    def __init__(self):
        super().__init__()

        # Create the UI elements
        self.url_label = QLabel("Video URL:")
        self.url_edit = QLineEdit()
        self.folder_label = QLabel("Save to:")
        self.folder_edit = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.download_button = QPushButton("Download")

        # Arrange the UI elements in a vertical layout
        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_edit)
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_edit)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.download_button)
        self.setLayout(layout)

        # Connect the buttons to their respective methods
        self.browse_button.clicked.connect(self.browse_folder)
        self.download_button.clicked.connect(self.start_download)

        # Set the window title and size
        self.setWindowTitle("Video Downloader")
        self.resize(500, 200)

    # Open a file dialog to choose the download folder
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Choose Save Folder")
        self.folder_edit.setText(folder)

    # Start two download threads (audio and video) when the Download button is clicked
    def start_download(self):
        url = self.url_edit.text()
        folder = self.folder_edit.text()
        if not url or not folder:
            return

        self.audio_download_thread = DownloadThread(url, folder, 'audio')
        self.video_download_thread = DownloadThread(url, folder, 'video')
        self.audio_download_thread.start()
        self.video_download_thread.start()

# If this script is run directly (instead of imported), create and show the application window
if __name__ == "__main__":
    app = QApplication(sys.argv)
    downloader = Downloader()
    downloader.show()
    sys.exit(app.exec_())
