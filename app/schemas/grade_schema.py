from pydantic import BaseModel


class GradeBase(BaseModel):
    student_id: int
    grade: int


class GradeCreate(GradeBase):
    pass


class Grade(GradeBase):
    reviewer_id: int
    homework_id: int

    class Config:
        orm_mode = True
