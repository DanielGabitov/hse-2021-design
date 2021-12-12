from sqlalchemy.orm import relationship
import sqlalchemy as sa

from app.database.setup import Base


class StudentModel(Base):
    __tablename__ = "student"

    id = sa.Column('id', sa.Integer, primary_key=True)
    username = sa.Column('username', sa.String(39), nullable=False, unique=True)

    classes = relationship('Association', back_populates='student')
