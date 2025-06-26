import face_recognition
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
        """
        Устанавливает новый список известных сотрудников.
        :param known_employees_encodings:
        :return:
        """
        self.known_employees_encodings = known_employees_encodings


    @staticmethod
    def cut_face(frame, face_location):
        """
        Обрезает кадр до лица.
        :param frame:
        :param face_location:
        :return: Обрезанное изображение с лицом.
        """
        top, right, bottom, left = face_location
        face_img = frame[top:bottom, left:right]
        return face_img

    @staticmethod
    def get_timestamp() -> str:
        """
        Создаёт timestamp в формате YYYY-MM-DD HH-MM-SS
        :return:
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    def frame_recognition(self):
        """
        Распознаёт лицо на каждом втором кадре.
        :return: Распознанного сотрудника, timestamp, изображение с лицом.
        """
        while True:
            ret, frame = self.video_capture.read()

            if self.process_this_frame:
                face_locations = face_recognition.face_locations(frame)
                print("found", len(face_locations), "faces")
                if not self.known_employees_encodings:
                    if self.prev_id == 0 and time() - self.waiting_time < 60:
                        print("found same face, abort")
                        return None, None, None
                    self.prev_id = 0
                    return EmployeeEncoding(id=0, employee_id=0, encoding=np.array([0]), is_access=False), self.get_timestamp(), self.cut_face(frame, face_locations[0])
                if face_locations:
                    face_encodings = face_recognition.face_encodings(frame, face_locations)
                    for face_encoding in face_encodings:
                        matches = face_recognition.compare_faces([face.encoding for face in self.known_employees_encodings], face_encoding)
                        best_match_employee = EmployeeEncoding(id=0, employee_id=0, encoding=np.array([0]), is_access=False) # неизвестный сотрудник
                        id = 0 # индекс неизвестного сотрудника

                        face_distances = face_recognition.face_distance([face.encoding for face in self.known_employees_encodings], face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            best_match_employee = self.known_employees_encodings[best_match_index]
                            id = best_match_employee.employee_id

                        if self.prev_id == id and time() - self.waiting_time < 60:
                            print("found same face, abort")
                            return None, None, None

                        print("found employee:", id)

                        self.prev_id = id
                        self.waiting_time = time()

                        face_img = self.cut_face(frame, face_locations[0])
                        return best_match_employee, self.get_timestamp(), face_img

            self.process_this_frame = not self.process_this_frame