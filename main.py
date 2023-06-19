import os
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from pytube import YouTube
from moviepy.editor import AudioFileClip


class DownloadThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, url, folder):
        super().__init__()
        self.url = url
        self.folder = folder

    def run(self):
        # Download the audio
        yt = YouTube(self.url)
        audio = yt.streams.filter(only_audio=True).first()
        download_path = audio.download(self.folder)

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
        self.download_button.clicked.connect(self.start_download)

        # Set the window properties
        self.setWindowTitle("Video Downloader")
        self.resize(500, 200)

    def browse_folder(self):
        """ Open a file dialog to choose a folder to save the video. """
        folder = QFileDialog.getExistingDirectory(self, "Choose Save Folder")
        self.folder_edit.setText(folder)

    def start_download(self):
        """ Start a new thread to download the video. """
        url = self.url_edit.text()
        folder = self.folder_edit.text()
        if not url or not folder:
            return

        self.download_thread = DownloadThread(url, folder)
        self.download_thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    downloader = Downloader()
    downloader.show()
    sys.exit(app.exec_())
