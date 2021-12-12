import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.database.setup import Base


class ClassToStudentAssociation(Base):
    __tablename__ = 'classes_to_students'
    class_id = sa.Column(sa.ForeignKey('class.id'), primary_key=True)
    student_id = sa.Column(sa.ForeignKey('student.id'), primary_key=True)
    student_nickname = sa.Column(sa.Text, nullable=False)
    student = relationship('StudentModel', back_populates='classes')
    class_ = relationship('ClassModel', back_populates='students')


class ClassModel(Base):
    __tablename__ = "class"

    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.Text, nullable=False)

    creator_id = sa.Column('creator_id', sa.Integer,
                           sa.ForeignKey('reviewer.id'), nullable=False)

    students = relationship('Association', back_populates='class_')
