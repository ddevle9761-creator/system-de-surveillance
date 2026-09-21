import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PySide6 import QtWidgets, QtCore

from interface_ui.camera_section import CameraWindow


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Window")
        self.setFixedSize(QtCore.QSize(900, 700))
        self.setupUi()
        self.connextion()

    def setupUi(self):
        sidebar = QtWidgets.QVBoxLayout()
        sidebar.setContentsMargins(10, 10, 10, 10)
        sidebar.setSpacing(20)

        self.stack = QtWidgets.QStackedWidget()
        self.pile_pages = self.stack

        self.camera_window = CameraWindow()
        self.pile_pages.addWidget(self.camera_window)

        self.btn_stop = QtWidgets.QPushButton("Stop Video")
        self.bnt_start = QtWidgets.QPushButton("Start Video")

        sidebar.addWidget(self.bnt_start)
        sidebar.addWidget(self.btn_stop)

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(20)
        main_layout.addLayout(sidebar)
        main_layout.addWidget(self.stack)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)

    def connextion(self):
        self.btn_stop.clicked.connect(self.stop_camera)
        self.bnt_start.clicked.connect(self.start_camera)

    def pile_pages(self):
        self.pile_pages.setCurrentIndex(0)

    def stop_camera(self):
        self.camera_window.stop_camera()

    def start_camera(self):
        self.camera_window.start_camera()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    try:
        with open(ROOT / "assets" / "styles.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass
    window.show()
    sys.exit(app.exec())
