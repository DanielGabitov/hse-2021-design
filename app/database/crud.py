from sqlalchemy.orm import Session

from app.database.models.user_model import UserModel
from app.database.models.class_model import ClassModel
from app.schemas.class_schema import ClassCreate


def get_user(*, db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()


# todo get all users by ids
def get_user_by_username(*, db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()


def create_user(*, db: Session, username: str, email: str):
    db_user = UserModel(username=username, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def find_class(*, db: Session, class_name: str, creator: UserModel):
    return (db.query(ClassModel).
            filter(ClassModel.name == class_name and ClassModel.creator == creator).
            first()
            )


def create_class(*, db: Session, creator: UserModel, class_: ClassCreate):
    db_class = ClassModel(name=class_.name, creator=creator)
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class


def get_class(*, db: Session, class_id: int):
    return db.query(ClassModel).filter(ClassModel.id == class_id).first()


def delete_class(*, db: Session, class_: ClassModel):
    return (db.query(ClassModel).
            filter(ClassModel == class_).
            delete()
            )
