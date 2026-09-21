from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtMultimedia import QMediaPlayer, QAudioInput, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
import sys

class VideoTest(QMainWindow):
    def __init__(self, src):
        self.src = src
        super().__init__()
        self.setWindowTitle("PySide6 Multimedia Test")
        self.resize(800, 600)

        self.video = QVideoWidget()
        self.setCentralWidget(self.video)

        self.audio_input = QAudioInput()
        self.audio_input.blockSignals(False)


        self.media_player = QMediaPlayer()

        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)


        self.media_player.setVideoOutput(self.video)

        self.media_player.setSource(QUrl.fromLocalFile(self.src))
        self.media_player.play()

if __name__ == '__main__':


    src = "VID_20260527_152715.mp4"
    app = QApplication(sys.argv)
    window = VideoTest(src)

    window.show()
    sys.exit(app.exec())

