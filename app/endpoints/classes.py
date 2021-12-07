import re
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import DatabaseError

from app.schemas.class_schema import ClassCreate
from app.database import crud, setup
from app.database.models.class_model import ClassModel
from app.helpers import github_interactions
from app.helpers.auth_setup import AuthInfo, get_authorized_user

classes_router = APIRouter(
    prefix='/classes'
)

github_repo_pattern = r'[a-zA-Z._-]+'


@classes_router.post('/')
async def create_class(class_: ClassCreate, db=Depends(setup.get_db),
                       auth_info: AuthInfo = Depends(get_authorized_user)):

    if re.match(pattern=github_repo_pattern, string=class_.name) is None:
        raise HTTPException(status_code=400,
                            detail=f'<{class_.name}> is not a valid github name. '
                                   f'It should have only [a-zA-Z._-]')

    if github_interactions.get_repo(auth_info=auth_info, class_name=class_.name):
        raise HTTPException(status_code=400,
                            detail=f'<{class_.name}> repo already exists. '
                                   f'Pick a different name')

    if crud.find_class(db=db, class_name=class_.name, creator=auth_info.user):
        raise HTTPException(status_code=400,
                            detail=f'User <{auth_info.user.username}> already has class '
                                   f'with name <{class_.name}>')

    link_to_repo = github_interactions.create_repo(auth_info=auth_info, class_=class_)
    try:
        crud.create_class(db=db, class_=class_, creator=auth_info.user)
    except DatabaseError as e:
        github_interactions.delete_repo(auth_info=auth_info, class_name=class_.name)
        raise HTTPException(status_code=500, detail=f'Some error in DB. {e.detail}')

    return f"class has benn successfully created. Link to github: {link_to_repo}"


@classes_router.delete('/')
async def delete_class(class_name: str, db=Depends(setup.get_db),
                       auth_info: AuthInfo = Depends(get_authorized_user)):
    class_: ClassModel = crud.find_class(db=db, class_name=class_name, creator=auth_info.user)
    if class_ is None:
        raise HTTPException(status_code=400,
                            detail=f'User <{auth_info.user.username}> does not have class '
                                   f'with name <{class_name}>')
    github_interactions.delete_repo(auth_info=auth_info, class_name=class_name)
    crud.delete_class(db=db, class_=class_)
    return f"Class <{class_name}> has been successfully deleted"
