from pydantic import BaseModel, ConfigDict
from typing import Any
import numpy as np

class EmployeeEncoding(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int
    employee_id: int
    encoding: np.ndarray[Any, np.dtype[np.float64]]
    is_access: bool

class Employee(BaseModel):
    id: int
    photo_url: str
    is_access: bool

