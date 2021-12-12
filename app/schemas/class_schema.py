from typing import List
from pydantic import BaseModel

from app.schemas.student_schema import StudentBase


class ClassBase(BaseModel):
    name: str


class ClassCreate(ClassBase):
    students: List[StudentBase]


class Class(ClassCreate):
    id: int
    creator_id: int

    class Config:
        orm_mode = True
