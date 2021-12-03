from sqlalchemy.orm import Session

from app.database.models.user import User


def get_user(*, db: Session, github_login: str):
    return db.query(User).filter(User.github_login == github_login).first()


def create_user(*, db: Session, github_login: str, nickname: str, email: str):
    db_user = User(github_login=github_login, nickname=nickname, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
