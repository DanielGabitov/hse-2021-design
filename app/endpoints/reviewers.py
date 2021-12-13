from fastapi import APIRouter, HTTPException, Depends

from app.schemas.reviewer_schema import Reviewer

from app.database import crud
from app.database.setup import get_db

reviewers_router = APIRouter(
    prefix='/reviewers'
)


@reviewers_router.get('/', response_model=Reviewer)
async def get_reviewer(reviewer_id: int, db=Depends(get_db)):
    reviewer = crud.get_reviewer_by_id(db=db, reviewer_id=reviewer_id)
    if reviewer is None:
        raise HTTPException(
            status_code=400,
            detail=f'Could not find reviewer with id <{reviewer_id}>'
        )
    return reviewer
