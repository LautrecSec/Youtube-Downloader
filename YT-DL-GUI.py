# Importing necessary libraries:
# os: to interact with the operating system
# PyQt5: to create the graphical user interface (GUI)
# pytube: to download videos from YouTube
# moviepy: to convert the downloaded files to mp3 format
import os
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from pytube import YouTube, exceptions
from moviepy.editor import AudioFileClip

# DownloadThread is a subclass of QThread, a PyQt5 class that creates a new thread. This allows the download to 
# occur in a separate thread from the GUI, preventing the GUI from freezing during the download.
class DownloadThread(QThread):
    def __init__(self, url, folder):
        # Initialize QThread
        super().__init__()

        # Set the YouTube video URL and the download folder
        self.url = url.strip()
        self.folder = folder

    def run(self):
        try:
            # Create a YouTube object using the video URL
            yt = YouTube(self.url)

            # Get the first audio stream available for the video
            stream = yt.streams.get_audio_only()

            # If the audio stream exists, download the stream, convert the file to mp3, and remove the original file
            if stream:
                download_path = stream.download(self.folder)
                mp3_path = os.path.splitext(download_path)[0] + '.mp3'
                clip = AudioFileClip(download_path)
                clip.write_audiofile(mp3_path)
                clip.close()
                if os.path.exists(download_path):
                    os.remove(download_path)

            # If no audio stream is available, print an error message
            else:
                print(f"No audio stream found for URL: {self.url}")

        # If a PytubeError occurs during the download, print the error
        except exceptions.PytubeError as e:
            print(f"PytubeError encountered: {str(e)}")

# The Downloader class creates the application window and controls the download process.
class Downloader(QWidget):
    def __init__(self):
        # Initialize QWidget
        super().__init__()

        # Create the GUI elements: labels, line edits, and buttons
        self.url_label = QLabel("Video URL:")
        self.url_edit = QLineEdit()
        self.folder_label = QLabel("Save to:")
        self.folder_edit = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.download_button = QPushButton("Download")

        # Set the layout of the GUI using QVBoxLayout, which arranges the GUI elements vertically
        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_edit)
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_edit)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.download_button)
        self.setLayout(layout)

        # Connect the "Browse" button to the browse_folder method, which allows the user to choose the download folder
        # Connect the "Download" button to the start_download method, which starts the download
        self.browse_button.clicked.connect(self.browse_folder)
        self.download_button.clicked.connect(self.start_download)

        # Set the title of the application window and its size
        self.setWindowTitle("Audio Downloader")
        self.resize(500, 200)

    # When the "Browse" button is clicked, open a folder dialog for the user to choose the download folder
    # Then, display the chosen folder in the folder_edit line edit
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Choose Save Folder")
        self.folder_edit.setText(folder)

    # When the "Download" button is clicked, get the video URL and the download folder from the line edits
    # Then, create a DownloadThread with these values and start the thread
    def start_download(self):
        url = self.url_edit.text()
        folder = self.folder_edit.text()
        if not url or not folder:
            return
        self.audio_download_thread = DownloadThread(url, folder)
        self.audio_download_thread.start()

# If the script is run directly (not imported), create an application and a Downloader object
# Show the Downloader (which is the application window), and start the application's event loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    downloader = Downloader()
    downloader.show()
    sys.exit(app.exec_())
