from typing import Optional
from fastapi import Depends, Cookie, HTTPException

from app.database import crud
from app.database.models.reviewer_model import ReviewerModel
from app.database.setup import get_db


class AuthInfo:
    def __init__(self, user: ReviewerModel, access_token: str):
        self.user = user
        self.access_token = access_token


async def get_authorized_user(db=Depends(get_db),
                              username: Optional[str] = Cookie(None),
                              access_token: Optional[str] = Cookie(None)):
    if username is None or access_token is None:
        raise HTTPException(status_code=401)
    user = crud.get_reviewer(db=db, username=username)
    if user is None:
        raise HTTPException(status_code=401)
    return AuthInfo(user=user, access_token=access_token)
