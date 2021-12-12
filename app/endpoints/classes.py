import re
from typing import Tuple, List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import DatabaseError

from app.schemas.class_schema import Class, ClassCreate
from app.schemas.student_schema import Student, StudentCreate
from app.database.models.class_model import ClassModel
from app.database.models.student_model import StudentModel

from app.database import crud, setup
from app.helpers import github_interactions
from app.helpers.auth_setup import AuthInfo, get_authorized_user

classes_router = APIRouter(
    prefix='/classes'
)

github_repo_pattern = r'[a-zA-Z._-]+'


def get_students(*, db, students: [StudentCreate]):
    fetched_students: [Tuple[StudentModel, str]] = []
    for student in students:
        student_model: StudentModel = crud.get_student_by_username(
            db=db,
            username=student.username
        )
        if student_model is None:
            student_model = crud.create_student(db=db,
                                                username=student.username)
        fetched_students.append((student_model, student.nickname))
    return fetched_students


# todo (4) add logging
@classes_router.post('/')
async def create_class(class_: ClassCreate, db=Depends(setup.get_db),
                       auth_info: AuthInfo = Depends(get_authorized_user)):
    if re.match(pattern=github_repo_pattern, string=class_.name) is None:
        raise HTTPException(
            status_code=400,
            detail=f'<{class_.name}> is not a valid github name. '
                   'It should have only [a-zA-Z._-]')
    repo = github_interactions.get_repo(auth_info=auth_info,
                                        class_name=class_.name)
    if repo:
        raise HTTPException(status_code=400,
                            detail=f'<{class_.name}> repo already exists. '
                                   f'Pick a different name')

    if crud.find_class(db=db, class_name=class_.name, creator=auth_info.user):
        raise HTTPException(
            status_code=400,
            detail=f'User <{auth_info.user.username}> already has class '
                   f'with name <{class_.name}>')

    students_with_nicknames = get_students(db=db, students=class_.students)
    link_to_repo = github_interactions.create_repo(auth_info=auth_info,
                                                   class_=class_)

    try:
        crud.create_class(db=db, class_name=class_.name,
                          creator=auth_info.user,
                          students_data=students_with_nicknames)
    except DatabaseError as e:
        github_interactions.delete_repo(auth_info=auth_info,
                                        class_name=class_.name)
        raise HTTPException(status_code=500, detail=f'Error in DB. {e.detail}')

    return f"Class has been successfully created. Github link: {link_to_repo}."


@classes_router.get('/', response_model=Class)
async def get_class(class_id: int, db=Depends(setup.get_db)):
    class_ = crud.get_class(db=db, class_id=class_id)
    if class_ is None:
        raise HTTPException(
            status_code=400,
            detail=f'Could not find class with id <{class_id}>'
        )

    student_ids: List[int] = []
    for a in class_.students:
        student_ids.append(a.student.id)
    return Class(id=class_.id, name=class_.name,
                 creator_id=class_.creator_id, student_ids=student_ids)


@classes_router.delete('/')
async def delete_class(class_name: str, db=Depends(setup.get_db),
                       auth_info: AuthInfo = Depends(get_authorized_user)):
    class_: ClassModel = crud.find_class(db=db, class_name=class_name,
                                         creator=auth_info.user)
    if class_ is None:
        raise HTTPException(
            status_code=400,
            detail=f'User <{auth_info.user.username}> does not have class '
                   f'with name <{class_name}>')
    github_interactions.delete_repo(auth_info=auth_info, class_name=class_name)
    crud.delete_class(db=db, class_=class_)
    return f"Class <{class_name}> has been successfully deleted"
