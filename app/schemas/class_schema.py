from typing import List
from pydantic import BaseModel

from app.schemas.student_schema import StudentCreate


class ClassBase(BaseModel):
    name: str


class ClassCreate(ClassBase):
    students: List[StudentCreate]


class Class(ClassBase):
    id: int
    creator_id: int
    student_ids: List[int]

    class Config:
        orm_mode = True
