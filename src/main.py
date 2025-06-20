import face_recognition
import cv2
import numpy as np
from cam_recognition import CamRecognition


video_capture = cv2.VideoCapture(0)
cam_recognition = CamRecognition(video_capture)
# получение данных с бд (айди, фото)
# заполнение столбца encodings
while True:
    # запрос об изменениях в бд
    # если запись новая / изменена:
        # перевод фото в encodings
        # запись нового encoding в бд
        # выполнение add / update encoding
    # если запись удалена - выполнение delete encoding
    # выполнение fill_known_faces
    cam_recognition.frame_recognition()
