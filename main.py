import os
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from pytube import YouTube, exceptions
from moviepy.editor import AudioFileClip

class DownloadThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, url, folder):
        super().__init__()
        self.url = url.strip()  # Remove potential leading/trailing whitespaces
        self.folder = folder

    def run(self):
        try:
            yt = YouTube(self.url)
            audio = yt.streams.filter(only_audio=True).first()
            if audio:
                download_path = audio.download(self.folder)

                # Create the mp3_path more efficiently
                mp3_path = os.path.splitext(download_path)[0] + '.mp3'

                clip = AudioFileClip(download_path)
                clip.write_audiofile(mp3_path)
                clip.close()  # Close the clip to free resources

                if os.path.exists(download_path):
                    os.remove(download_path)
            else:
                print(f"No audio stream found for URL: {self.url}")

        except exceptions.PytubeError as e:
            print(f"PytubeError encountered: {str(e)}")

class Downloader(QWidget):
    def __init__(self):
        super().__init__()

        self.url_label = QLabel("Video URL:")
        self.url_edit = QLineEdit()
        self.folder_label = QLabel("Save to:")
        self.folder_edit = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.download_button = QPushButton("Download")

        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_edit)
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_edit)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.download_button)
        self.setLayout(layout)

        self.browse_button.clicked.connect(self.browse_folder)
        self.download_button.clicked.connect(self.start_download)

        self.setWindowTitle("Video Downloader")
        self.resize(500, 200)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Choose Save Folder")
        self.folder_edit.setText(folder)

    def start_download(self):
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
