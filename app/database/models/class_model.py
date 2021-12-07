import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref

from app.database.setup import Base


# classes_to_students = sa.Table(
#     'classes_to_students',
#     Base.metadata,
#     sa.Column('class_id', sa.Integer, sa.ForeignKey('class.id')),
#     sa.Column('user_id', sa.Integer, sa.ForeignKey('utilisateur.id'))
# )


class ClassModel(Base):
    __tablename__ = "class"

    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.Text, nullable=False)

    creator_id = sa.Column('creator_id', sa.Integer, sa.ForeignKey('utilisateur.id'), nullable=False)

    # students = relationship('UserModel', secondary=classes_to_students, backref=backref('classes'))
