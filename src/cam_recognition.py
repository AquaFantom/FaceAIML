import face_recognition
import cv2
import numpy as np
from time import time
from datetime import datetime

from src.database.schemas import EmployeeEncoding


class CamRecognition:
    def __init__(self, video_capture, known_employees_encodings=None):
        self.video_capture = video_capture
        self.face_locations = []
        self.known_employees_encodings = known_employees_encodings
        self.prev_id = -1
        self.waiting_time = time()
        self.process_this_frame = True


    def set_known_employees_encodings(self, known_employees_encodings):
        self.known_employees_encodings = known_employees_encodings


    def send_photo(self):
        ...

    @staticmethod
    def cut_face(frame, face_location):
        top, right, bottom, left = face_location
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        face_img = frame[top:bottom, left:right]
        return face_img

    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    def frame_recognition(self):
        ret, frame = self.video_capture.read()

        if self.process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_small_frame)
            if face_locations:
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces([face.face_encoding for face in self.known_employees_encodings], face_encoding)
                    id = 0 # индекс "неизвестного сотрудника"

                    face_distances = face_recognition.face_distance([face.face_encoding for face in self.known_employees_encodings], face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        id = self.known_employees_encodings[best_match_index].employee_id

                    if self.prev_id == id and time() - self.waiting_time < 60:
                        return

                    self.waiting_time = time()
                    return id, self.get_timestamp()

        self.process_this_frame = not self.process_this_frame