from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import DatabaseError

from app.database.models.class_model import ClassModel
from app.database.models.homework_model import HomeworkModel, GradeModel
from app.database.models.reviewer_model import ReviewerModel
from app.database.models.student_model import StudentModel
from app.schemas.homework_schema import Homework, HomeworkCreate
from app.schemas.grade_schema import Grade, GradeCreate
from app.helpers.auth_setup import AuthInfo, get_authorized_user

from app.database.setup import get_db
from app.database import crud
from app.helpers import github_interactions

homeworks_router = APIRouter(
    prefix='/homeworks'
)


def check_reviewer_rights(*, user_id: int,
                          reviewers: List[ReviewerModel]) -> bool:
    for reviewer in reviewers:
        if reviewer.id == user_id:
            return True
    return False


def check_student(*, student_id: int, class_: ClassModel) -> bool:
    for association in class_.students:
        if association.student.id == student_id:
            return True
    return False


@homeworks_router.post("/", response_model=Homework)
async def create_homework(homework_info: HomeworkCreate, db=Depends(get_db),
                          auth_info: AuthInfo = Depends(get_authorized_user)):

    class_: ClassModel = crud.get_class(db=db, class_id=homework_info.class_id)
    if class_ is None:
        raise HTTPException(
            status_code=400,
            detail=f'Class with id <{homework_info.class_id}> does not exist'
        )

    if check_reviewer_rights(user_id=auth_info.user.id,
                             reviewers=class_.reviewers) is None:
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
    homeworks_amount = len(class_.homeworks)
    try:
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
            class_=class_, creator=auth_info.user)

    except DatabaseError as e:
        github_interactions.delete_branch(
            owner=auth_info.user.username, repo=class_.name,
            branch_name=f'HW_{homeworks_amount}',
            access_token=auth_info.access_token
        )
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


@homeworks_router.post("/{homework_id}/grades", response_model=Grade)
async def add_grade(
        homework_id: int, grade_info: GradeCreate, db=Depends(get_db),
        auth_info=Depends(get_authorized_user)):

    homework: HomeworkModel = crud.get_homework_by_id(
        db=db, homework_id=homework_id
    )

    if homework is None:
        raise HTTPException(
            status_code=404,
            detail=f'Could not find homework with <{homework_id}> id'
        )

    class_: ClassModel = homework.class_
    if check_reviewer_rights(user_id=auth_info.user.id,
                             reviewers=class_.reviewers) is None:
        raise HTTPException(
            status_code=400,
            detail=f'User with id <{auth_info.user.id}> does not have rights '
                   f'to create homeworks in <{class_.id}> class'
        )

    student: StudentModel = crud.get_student_by_id(
        db=db, student_id=grade_info.student_id
    )
    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f'Student with id <{grade_info.student_id}> does not exits'
        )

    if check_student(student_id=grade_info.student_id, class_=class_) is None:
        raise HTTPException(
            status_code=400,
            detail=f'Student <{auth_info.user.id}> does not belong to '
                   f'class <{class_.id}>'
        )

    grade: GradeModel = crud.create_grade(
        db=db, homework=homework, reviewer=auth_info.user,
        student=student, grade=grade_info.grade
    )
    return grade
