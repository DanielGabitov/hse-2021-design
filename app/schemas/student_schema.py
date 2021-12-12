from pydantic import BaseModel


class StudentBase(BaseModel):
    username: str


class StudentCreate(StudentBase):
    nickname: str


class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True
