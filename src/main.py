import face_recognition
import cv2
import numpy as np
from cam_recognition import CamRecognition


video_capture = cv2.VideoCapture(0)
cam_recognition = CamRecognition(video_capture)
while True:
    # получение данных с бд / изменение пользователей и т.п.
    # перевод фото в encodings если у новой записи в бд пустой "face_encoding" -> запись кодировки в бд
    # заполнение полей cam_recognition
    cam_recognition.frame_recognition()
