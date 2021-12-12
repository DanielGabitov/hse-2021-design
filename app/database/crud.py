from typing import Optional, List, Tuple
from sqlalchemy.orm import Session

from app.database.models.reviewer_model import ReviewerModel
from app.database.models.student_model import StudentModel
from app.database.models.class_model import ClassModel
from app.database.models.class_model import ClassToStudentAssociation


def get_reviewer_by_username(*, db: Session, username: str) -> ReviewerModel:
    return (db.query(ReviewerModel).
            filter(ReviewerModel.username == username).
            first())


def get_reviewer_by_id(*, db: Session, reviewer_id: int) -> ReviewerModel:
    return (db.query(ReviewerModel).
            filter(ReviewerModel.id == reviewer_id).
            first())


def get_student_by_username(*, db: Session, username: str) -> StudentModel:
    return (db.query(StudentModel).
            filter(StudentModel.username == username).
            first())


def get_student_by_id(*, db: Session, student_id: int) -> StudentModel:
    return (db.query(StudentModel).
            filter(StudentModel.id == student_id).
            first())


def create_reviewer(*, db: Session, username: str, nickname: str,
                    email: Optional[str]) -> ReviewerModel:
    db_user = ReviewerModel(username=username, nickname=nickname, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_student(*, db: Session, username: str) -> ReviewerModel:
    db_user = StudentModel(username=username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_class(*, db: Session, class_name: str, creator: ReviewerModel,
                 students_data: List[Tuple[StudentModel, str]]) -> ClassModel:
    class_: ClassModel = ClassModel(name=class_name, creator=creator)
    for student, nickname in students_data:
        a = ClassToStudentAssociation(student_nickname=nickname)
        a.student = student
        class_.students.append(a)
    db.add(class_)
    db.commit()
    db.refresh(class_)
    return class_


def get_class(*, db: Session, class_id: int) -> ClassModel:
    return db.query(ClassModel).filter(ClassModel.id == class_id).first()


def find_class(*, db: Session, class_name: str,
               creator: ReviewerModel) -> ClassModel:
    return (db.query(ClassModel).
            filter(ClassModel.name == class_name
                   and ClassModel.creator == creator).
            first())


def delete_class(*, db: Session, class_: ClassModel):
    return (db.query(ClassModel).
            filter(ClassModel == class_).
            delete()
            )
