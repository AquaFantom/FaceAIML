from sqlalchemy import create_engine, select, func, delete, desc, select
from sqlalchemy.orm import registry, Session, sessionmaker, joinedload
from src.database.models import AbstractModel, EmployeeEncodingsModel, AccessLogModel, EmployeeModel
import numpy as np


class Database:

    def __init__(self, url: str):
        self.URL = url
        self.engine = create_engine(self.URL, echo=False)
        self.mapped_registry = registry()
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.encodings_count = 0
        with self.Session().begin():
            AbstractModel.metadata.create_all(self.engine)

    def add(self, session, obj):
        session.add(obj)
        session.commit()

    # Encodings

    def get_employee_encodings(self):
        """
        :return: список сотруников с полями id, employee_id, encoding
        """
        with self.Session() as session:
            res = session.execute(select(EmployeeEncodingsModel))
            encodings = res.scalars().unique()
            encodings = list(map(lambda x: x.to_obj(), encodings))
            self.encodings_count = len(encodings)
            return encodings

    def get_employees_without_encodings(self):
        """
        :return: список сотрудников (с полями id, photo_url) для которых нет энкодингов
        (кроме нулевого сотрудника)
        """
        with self.Session() as session:
            res = session.execute(select(EmployeeModel)
                                  .where(EmployeeModel.encoding == None).where(EmployeeModel.id != 0))
            employees = res.scalars().unique()
            employees = list(map(lambda x: x.to_obj(), employees))
            return employees

    def add_employee_encoding(self, employee_id: int, new_encoding):
        """
        Добавляет или обновляет encoding сотрудника
        :param employee_id:
        :param new_encoding:
        :return: False если сотрудника с таким id не существует
        """
        new_encoding = [str(x) for x in new_encoding]
        with self.Session() as session:
            res = session.execute(select(EmployeeModel).where(EmployeeModel.id == employee_id))
            employee = res.scalar()
            if employee is None: return False
            res = session.execute(select(EmployeeEncodingsModel).where(EmployeeEncodingsModel.employee_id == employee_id))
            encoding = res.scalar()
            if encoding is None:
                res = session.execute(select(EmployeeEncodingsModel.id).order_by(EmployeeEncodingsModel.id.desc()))
                encoding_id = res.scalar()
                encoding_id = encoding_id + 1 if encoding_id is not None else 0
                encoding = EmployeeEncodingsModel(id=encoding_id, employee_id=employee_id, encoding=new_encoding)
            else:
                encoding.encoding = new_encoding
            self.add(session, encoding)
            self.encodings_count += 1
            return True

    def check_employees_without_encodings(self):
        """
        Проверяет был ли удалён энкодинг
        :return:
        """
        with self.Session() as session:
            stmt = select(func.count()).select_from(EmployeeEncodingsModel)
            count = session.execute(stmt).scalar()
            return count == self.encodings_count

    # AccessLogs

    def add_access_log(self, employee_id: int, timestamp):

        """
        :param employee_id:
        :param timestamp: время прохождения
        :return: False если сотрудника с таким id не существует
        """

        with self.Session() as session:
            res = session.execute(select(EmployeeModel).where(EmployeeModel.id == employee_id))
            employee = res.scalar()
            if employee is not None:
                res = session.execute(select(AccessLogModel.id).order_by(AccessLogModel.id.desc()))
                log_id = res.scalar()
                log_id = log_id + 1 if log_id is not None else 0
                access_log = AccessLogModel(id=log_id, employee_id=employee_id,
                                            timestamp=timestamp, photo_url=str(log_id))
                self.add(session, access_log)
                return True
            else:
                return False


# ТЕСТ / ПРИМЕР
URL = "тут должен быть URL базы!"
database = Database(URL)
encoding = np.array([0.2123123, 0.21312312, 0.354353453])
database.add_employee_encoding(1, encoding)

employee_encodings = database.get_employee_encodings()
for i in employee_encodings:
    print(i.encoding)

employees = database.get_employees_without_encodings()
for i in employees:
    print(i.id)

print(database.add_access_log(0, "2024-12-12 12:25:10"))