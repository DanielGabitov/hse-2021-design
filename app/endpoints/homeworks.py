from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import DatabaseError

from app.database.models.class_model import ClassModel
from app.database.models.reviewer_model import ReviewerModel
from app.database.setup import get_db
from app.database import crud
from app.schemas.homework_schema import Homework, HomeworkCreate
from app.helpers import github_interactions
from app.helpers.auth_setup import AuthInfo, get_authorized_user
# todo (8) order imports everywhere

homeworks_router = APIRouter(
    prefix='/homeworks'
)


@homeworks_router.post("/", response_model=Homework)
async def create_homework(homework_info: HomeworkCreate, db=Depends(get_db),
                          auth_info: AuthInfo = Depends(get_authorized_user)):

    class_: ClassModel = crud.get_class(db=db, class_id=homework_info.class_id)
    if class_ is None:
        raise HTTPException(
            status_code=400,
            detail=f'Class with id <{homework_info.class_id}> does not exist'
        )

    reviewers: List[ReviewerModel] = class_.reviewers
    creator: Optional[ReviewerModel] = None
    for reviewer in reviewers:
        if reviewer.id == auth_info.user.id:
            creator = reviewer

    if creator is None:
        raise HTTPException(
            status_code=400,
            detail=f'User with id <{auth_info.user.id}> does not have rights '
                   f'to create homeworks in <{class_.id}> class'
        )

    if crud.find_homework(db=db, creator_id=auth_info.user.id,
                          name=homework_info.name):
        raise HTTPException(
            status_code=400,
            detail=f'Homework with name <{homework_info.name}> already '
                   f'exists in class <{class_.id}>'
        )

    try:
        homeworks_amount = len(class_.homeworks)
        commit_sha = github_interactions.get_branch_last_commit(
            owner=auth_info.user.username, repo=class_.name
        )
        branch_name = f'HW_{homeworks_amount}'
        github_interactions.create_branch(
            owner=auth_info.user.username, repo=class_.name,
            branch_name=f'HW_{homeworks_amount}', commit_sha=commit_sha,
            access_token=auth_info.access_token
        )
        hw = crud.create_homework(
            db=db, name=homework_info.name, branch_name=branch_name,
            class_=class_, creator=creator)

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f'Error in DB. {e.detail}')

    return hw


@homeworks_router.get("/", response_model=Homework)
async def get_hw(homework_id: int, db=Depends(get_db)):
    homework = crud.get_homework_by_id(db=db, homework_id=homework_id)
    if homework is None:
        raise HTTPException(
            status_code=404,
            detail=f'Could not find homework with <{homework_id}> id'
        )
    return homework
