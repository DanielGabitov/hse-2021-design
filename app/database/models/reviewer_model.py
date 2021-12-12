import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref

from app.database.setup import Base


class ReviewerModel(Base):
    __tablename__ = "reviewer"

    id = sa.Column('id', sa.Integer, primary_key=True)
    username = sa.Column('username', sa.String(39), nullable=False, unique=True)
    nickname = sa.Column('nickname', sa.Text, nullable=False)
    email = sa.Column('email', sa.Text, nullable=False)

    created_classes = relationship('ClassModel', backref=backref('creator'))
