import sys
from pathlib import Path


from PySide6.QtCore import QSize, QThread, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QPixmap

from thread_dir.thread import ImageWorker


class CameraWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flux video")
        self.resize(QSize(600, 500))
        self.camera_thread = None
        self.camera_worker = None
        self.model_path = str(Path(__file__).resolve().parent.parent / "models" / "yolo26n.pt")
        self.setup_ui()

    def setup_ui(self):
        self.video_label = QLabel("La caméra est arrêtée")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("background-color: rgba(23, 34, 56, 0.5); color: rgb(233, 0, 77); border: 2px solid #444;")
        self.video_label.setMinimumSize(320, 240)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video_label)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def start_camera(self):
        self.camera_thread = QThread()
        self.camera_worker = ImageWorker(0, self.model_path)
        self.camera_worker.moveToThread(self.camera_thread)

        self.camera_thread.started.connect(self.camera_worker.run)
        self.camera_worker.frame_ready.connect(self.update_frame)
        self.camera_worker.error.connect(self.show_error)
        self.camera_worker.finished.connect(self.camera_thread.quit)
        self.camera_worker.finished.connect(self.camera_worker.deleteLater)
        self.camera_thread.finished.connect(self.camera_thread.deleteLater)

        self.camera_thread.start()

    def update_frame(self, qimage):
        pixmap = QPixmap.fromImage(qimage)
        scaled = pixmap.scaled(self.video_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.video_label.setPixmap(scaled)

    def show_error(self, message):
        self.video_label.setText(message)

    def stop_camera(self):
        if self.camera_worker is not None:
            self.camera_worker.stop()

        if self.camera_thread is not None and self.camera_thread.isRunning():
            self.camera_thread.quit()
            self.camera_thread.wait(1000)










if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraWindow()
    window.show()
    sys.exit(app.exec())
