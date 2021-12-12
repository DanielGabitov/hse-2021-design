from pydantic import BaseModel


class ReviewerBase(BaseModel):
    username: str
    email: str


class Reviewer(ReviewerBase):
    id: int

    class Config:
        orm_mode = True
