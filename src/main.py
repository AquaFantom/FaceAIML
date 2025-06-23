import sys
from dotenv import load_dotenv
import os
import face_recognition
import cv2
import numpy as np
from cam_recognition import CamRecognition
from src.database.database import Database, employees, employee_encodings
from src.database.schemas import EmployeeEncoding, Employee
from src.utils.backend_connection import Backend
from time import time


class MLApp:
    def __init__(self, database: Database, backend: Backend):
        self.database = database
        self.backend = backend
        self.db_request_time = time()
        self.log_root = "static/log/"


    def fill_encoding(self, employee: Employee):
        """
        Вычисляет кодировку лица для сотрудника и добавляет его в таблицу 'employee_encodings'.
        :param employee:
        :return:
        """
        face_encoding = face_recognition.face_encodings(employee.photo_url)[0]
        self.database.add_employee_encoding(employee.id, face_encoding)


    def fill_empty_encodings(self):
        """
        Находит сотрудников без кодировки лиц из таблицы 'employees' и
        поочередно вызывает для каждого функцию 'fill_encoding()'.
        :return:
        """
        employees = self.database.get_employees_without_encodings()
        for employee in employees:
            self.fill_encoding(employee)


    def main(self):
        """
        Основной цикл программы.
        :return:
        """
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
            employee, timestamp, face_img = cam_recognition.frame_recognition()
            if employee:
                log_id = self.database.add_access_log(employee.employee_id, timestamp)
                if log_id:
                    cv2.imwrite(self.log_root + str(log_id) + ".png", face_img)
                    if employee.employee_id == 0:
                        self.backend.notify_access_log(False)
                    else:
                        self.backend.notify_access_log(employee.is_access)



if __name__ == '__main__':
    load_dotenv()
    DB_URL = os.getenv('DB_URL')
    BACKEND_URL = os.getenv('BACKEND_URL')
    DB_ROOT_PASSWORD = os.getenv('ROOT_PASSWORD')
    database = Database(DB_URL)
    backend = Backend(BACKEND_URL, DB_ROOT_PASSWORD)

    mlapp = MLApp(database, backend)
    mlapp.main()