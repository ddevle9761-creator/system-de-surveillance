import time
import datetime

import cv2
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QImage

from model_project.main import SourceModel
from repository.repot import Repot


class ImageWorker(QObject):
    frame_ready = Signal(object)
    finished = Signal()
    error = Signal(str)

    def __init__(self, source=0, model_path=None):
        super().__init__()
        self.source = source
        self.capture = cv2.VideoCapture(source)
        self.running = False
        self.counter = 10

        if model_path is None:
            import pathlib
            root = pathlib.Path(__file__).resolve().parent.parent
            model_path = str(root / "models" / "yolov8n.pt")

        self.model = SourceModel(model_path)

    def save_detected_objects(self, frame):
        try:
            _, detections = self.model.detect(frame)
        except Exception:
            return

        if not detections:
            return

        repo = Repot()
        now = str(datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S"))


        for detection in detections:
            nom = detection[0]

            try:
                confidence = float(str(detection[1]).replace("%", ""))
            except (TypeError, ValueError):
                continue

            data = {
                "nom": nom,
                "confident": confidence,
                "date": now,
            }

            if self.check(nom, now):
                repo.save(data)



    def check(self,nom, now):
        last_save = Repot().get_last_now()
        if last_save is None:
            return None

        last_nom = last_save[0]
        last_time = last_save[1]

        last_time = self.__make_str_maintenant_to_time__(last_time)
        now = self.__make_str_maintenant_to_time__(now)

        if last_nom == nom:
            if now - last_time < datetime.timedelta(seconds=10):
                return False
            return True

        return True


    def __make_str_maintenant_to_time__(self, now):
        maintenant = datetime.datetime.strptime(now, "%Y/%m/%d %H:%M:%S")
        return maintenant








    @Slot()
    def run(self):
        self.running = True
        try:
            while self.running:
                ret, frame = self.capture.read()
                if not ret:
                    self.error.emit("Impossible de lire la caméra.")
                    break

                self.save_detected_objects(frame)
                processed_frame = self.model.design_les_objets(frame, draw=True)
                rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                qimage = QImage(rgb_frame.data, w, h, ch * w, QImage.Format_RGB888)
                self.frame_ready.emit(qimage)

        except Exception as exc:
            self.error.emit(str(exc))
        finally:
            self.capture.release()
            self.finished.emit()

    @Slot()
    def stop(self):
        self.running = False

















