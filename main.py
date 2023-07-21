# Import necessary modules
import os
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from pytube import YouTube, exceptions
from moviepy.editor import AudioFileClip

# This class is responsible for downloading audio from a YouTube video in a separate thread.
class DownloadThread(QThread):
    def __init__(self, url, folder):
        super().__init__()
        self.url = url.strip()  # URL of the YouTube video.
        self.folder = folder  # Folder where to save the downloaded audio.

    def run(self):
        try:
            # Create a YouTube object.
            yt = YouTube(self.url)

            # Filter the audio stream from the YouTube object and get the first stream.
            stream = yt.streams.get_audio_only()

            # If the audio stream is available, download it and convert it to MP3.
            if stream:
                download_path = stream.download(self.folder)
                mp3_path = os.path.splitext(download_path)[0] + '.mp3'
                clip = AudioFileClip(download_path)
                clip.write_audiofile(mp3_path)
                clip.close()

                # Remove the original audio file after conversion.
                if os.path.exists(download_path):
                    os.remove(download_path)
            else:
                print(f"No audio stream found for URL: {self.url}")

        # Handle any exceptions that occur during the downloading process.
        except exceptions.PytubeError as e:
            print(f"PytubeError encountered: {str(e)}")

class Downloader(QWidget):
    def __init__(self):
        super().__init__()

        # Create the UI elements.
        self.url_label = QLabel("Video URL:")
        self.url_edit = QLineEdit()
        self.folder_label = QLabel("Save to:")
        self.folder_edit = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.download_button = QPushButton("Download")

        # Arrange the UI elements in a vertical layout.
        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_edit)
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_edit)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.download_button)
        self.setLayout(layout)

        # Connect the buttons to their respective methods.
        self.browse_button.clicked.connect(self.browse_folder)
        self.download_button.clicked.connect(self.start_download)

        # Set the window title and size.
        self.setWindowTitle("Audio Downloader")
        self.resize(500, 200)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Choose Save Folder")
        self.folder_edit.setText(folder)

    def start_download(self):
        url = self.url_edit.text()
        folder = self.folder_edit.text()
        if not url or not folder:
            return
        self.audio_download_thread = DownloadThread(url, folder)
        self.audio_download_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    downloader = Downloader()
    downloader.show()
    sys.exit(app.exec_())
