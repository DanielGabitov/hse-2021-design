from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship, backref

from app.database.setup import Base


class UserModel(Base):
    __tablename__ = "utilisateur"

    id = Column('id', Integer, primary_key=True)
    username = Column('username', String(39), nullable=False, unique=True)
    email = Column('email', Text, nullable=False)
    created_classes = relationship('ClassModel', backref=backref('creator'))
