from pydantic import BaseModel


class ClassBase(BaseModel):
    name: str


class ClassCreate(ClassBase):
    pass


class Class(ClassCreate):
    id: int
    creator_id: int
