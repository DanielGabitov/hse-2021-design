from sqlalchemy import Column, Integer, String, Text

from app.database.setup import Base


class User(Base):
    __tablename__ = "utilisateur"

    id = Column('id', Integer, primary_key=True)
    github_login = Column(String(39), nullable=False, unique=True)
    nickname = Column(Text, nullable=False)
    email = Column('email', Text, nullable=False)
