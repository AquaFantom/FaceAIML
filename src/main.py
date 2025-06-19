import face_recognition
import cv2
import numpy as np

# черновое из примера на оф сайте библиотеки - в мейне включаем камеру, создаём объект распознавания и запускаем цикл - здесь или в классе...

video_capture = cv2.VideoCapture(0)

obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden"
]