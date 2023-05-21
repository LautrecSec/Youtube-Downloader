import os
import sys

from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from pytube import YouTube
from moviepy.editor import AudioFileClip


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

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_edit)
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_edit)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.download_button)
        self.setLayout(layout)

        # Connect the signals and slots
        self.browse_button.clicked.connect(self.browse_folder)
        self.download_button.clicked.connect(self.download_video)

        # Set the window properties
        self.setWindowTitle("Video Downloader")
        self.resize(500, 200)

    def browse_folder(self):
        """ Open a file dialog to choose a folder to save the video. """
        folder = QFileDialog.getExistingDirectory(self, "Choose Save Folder")
        self.folder_edit.setText(folder)

    def download_video(self):
        """ Download the video from the specified URL and save it to the specified folder. """
        url = self.url_edit.text()
        folder = self.folder_edit.text()
        if not url or not folder:
            return

        # Download the audio
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        download_path = audio.download(folder)
        
        # Convert the audio to mp3
        clip = AudioFileClip(download_path)
        if download_path.endswith('.3gpp'):
            mp3_path = download_path.replace('.3gpp', '.mp3')
        else:
            mp3_path = download_path.replace('.mp4', '.mp3')
        clip.write_audiofile(mp3_path)

        # Delete the original file
        if os.path.exists(download_path):
            os.remove(download_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    downloader = Downloader()
    downloader.show()
    sys.exit(app.exec_())
