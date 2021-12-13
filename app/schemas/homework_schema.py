from pydantic import BaseModel


class HomeworkBase(BaseModel):
    name: str
    class_id: int


class HomeworkCreate(HomeworkBase):
    pass


class Homework(HomeworkBase):
    id: int
    creator_id: int
    branch_name: str

    class Config:
        orm_mode = True
