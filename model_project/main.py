import time

import cv2
from ultralytics import YOLO
import numpy as np

import typing

class SourceModel:
    def __init__(self, model_path: typing.Optional[str]) -> None:
        self.resul = None
        self.model_path = model_path


        if not self.model_path:
            raise Exception("No model path provided")
        self.model = YOLO(self.model_path)

    def detect(self, img):
        resultat = self.model(img)
        liste = []

        if resultat:
            for result in resultat:
                noms = result.names
                self.resul = result


                for box in result.boxes:
                    class_id = int(box.cls[0])
                    object_name = noms[class_id]
                    confidence = float(box.conf[0])
                    coords = box.xyxy[0].tolist()
                    xmin, ymin, xmax, ymax = [round(c, 2) for c in coords]



                    info_object = f"Objet': {object_name}, 'Confidence': '{confidence:.2%}"
                    position_object = f"Haut-Gauche : {int(xmin), int(ymin)}, Bas-Droite: {int(xmax), int(ymax)}"

                    liste.append([object_name, f"{confidence:.2%}", int(xmin), int(ymin), int(xmax), int(ymax)])

        return img, liste

    def design_les_objets(self, img, draw=False):
        img, liste = self.detect(img)
        if liste:
            objet_info = liste[0][0]
            confidence = liste[0][1]
            print(liste)
            x, y, w, h = liste[0][2], liste[0][3],liste[0][4], liste[0][5]
            if draw:
                cv2.rectangle(img, (x-40, y), (x + w-10, y + h-10), (0, 0, 255), 2)
                cv2.putText(img, f"{objet_info} {confidence}", (x+10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


        return img

    def get_info(self, img):
        img, liste = self.detect(img)

        if liste:
            for ob in liste:
                objet = ob[0]
                confidence = ob[1]
                print(liste)
                xmin, ymin, xmax, ymax = ob[2], ob[3], ob[4], ob[5]



                print(confidence)

                return objet, confidence, #[xmin, ymin, xmax, ymax]
        return None




if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    H = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    W = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    FPS = int(cap.get(cv2.CAP_PROP_FPS))

    src = SourceModel("../models/yolov8n.pt")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img, result = src.detect(frame)
        src.design_les_objets(img, draw=True)
        src.get_info(img)

        cv2.imshow("Frame", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




















#
# src = SourceModel("../models/yolo11m.pt")
# info = src.detect(img='../Oopncv_project/img2.jpg', show=True)
# if info:
#     for result in info:
#         for i in info:
#             print(i)
#             print()


