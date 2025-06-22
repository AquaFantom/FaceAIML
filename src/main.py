import sys

import face_recognition
import cv2
import numpy as np
from cam_recognition import CamRecognition
from src.database.database import Database, employees, employee_encodings
from src.database.schemas import EmployeeEncoding, Employee
from time import time


class MLApp:
    def __init__(self, url):
        self.database = Database(url)
        self.db_request_time = time()


    def fill_encoding(self, employee: Employee):
        face_encoding = face_recognition.face_encodings(employee.photo_url)[0]
        self.database.add_employee_encoding(employee.id, face_encoding)


    def fill_empty_encodings(self):
        employees = self.database.get_employees_without_encodings()
        for employee in employees:
            self.fill_encoding(employee)


    def main(self):
        self.fill_empty_encodings()
        employees_encodings = self.database.get_employee_encodings()

        video_capture = cv2.VideoCapture(0)
        cam_recognition = CamRecognition(video_capture, employees_encodings)
        while True:
            if time() - self.db_request_time >= 60:
                if not self.database.check_employees_without_encodings():
                    self.fill_empty_encodings()
                    employees_encodings = self.database.get_employee_encodings()
                    cam_recognition.set_known_employees_encodings(employees_encodings)
            cam_recognition.frame_recognition()


if __name__ == '__main__':
    mlapp = MLApp("url")
    mlapp.main()