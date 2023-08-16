import os
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from pytube import YouTube, exceptions
from moviepy.editor import AudioFileClip
import sys

class DownloadThread(QThread):
    def __init__(self, url, folder):
        super().__init__()
        self.url = url.strip()
        self.folder = folder

    def run(self):
        try:
            yt = YouTube(self.url)
            stream = yt.streams.get_audio_only()
            if stream:
                download_path = stream.download(self.folder)
                mp3_path = os.path.splitext(download_path)[0] + '.mp3'
                clip = AudioFileClip(download_path)
                clip.write_audiofile(mp3_path)
                clip.close()
                if os.path.exists(download_path):
                    os.remove(download_path)
            else:
                print(f"No audio stream found for URL: {self.url}")
        except exceptions.PytubeError as e:
            print(f"PytubeError encountered: {str(e)}")

class Downloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Youtube Audio Downloader")
        self.setWindowIcon(QIcon('icon.png')) # Add an icon file

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
        layout.setSpacing(15)
        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
            }
            QLabel {
                font-size: 12px;
            }
        """)

        self.browse_button.clicked.connect(self.browse_folder)
        self.download_button.clicked.connect(self.start_download)

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
