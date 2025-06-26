import numpy as np
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import String, Numeric, ARRAY
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from src.database.schemas import EmployeeEncoding, Employee


class AbstractModel(DeclarativeBase):
    pass


class EmployeeModel(AbstractModel):
    __tablename__ = 'employees'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    info: Mapped[str] = mapped_column(String(200))
    photo_url: Mapped[str] = mapped_column(String, nullable=True)
    is_access: Mapped[bool] = mapped_column()

    access_logs: Mapped[list["AccessLogModel"]] = relationship(back_populates="employee", lazy=False)
    encoding: Mapped["EmployeeEncodingsModel"] = relationship(back_populates="employee", lazy=False)

    def to_obj(self):
        return Employee(id=self.id, photo_url=self.photo_url, is_access=self.is_access)


class EmployeeEncodingsModel(AbstractModel):
    __tablename__ = 'employee_encodings'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey('employees.id'), unique=True)
    encoding: Mapped[list[str]] = mapped_column(ARRAY(Numeric))

    employee: Mapped["EmployeeModel"] = relationship(back_populates="encoding", lazy=False)

    def to_obj(self):
        encoding = np.array([float(x) for x in self.encoding], float)
        is_access = self.employee.is_access
        return EmployeeEncoding(id=self.id, employee_id=self.employee_id, encoding=encoding, is_access=is_access)


class AccessLogModel(AbstractModel):
    __tablename__ = "access_logs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey('employees.id'))
    timestamp: Mapped[datetime] = mapped_column()
    photo_url: Mapped[str] = mapped_column(String, nullable=True)

    employee: Mapped["EmployeeModel"] = relationship(back_populates="access_logs", lazy=False)

