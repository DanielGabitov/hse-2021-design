import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.database.setup import Base


class GradeModel(Base):
    __tablename__ = 'grade'
    homework_id = sa.Column(sa.ForeignKey('homework.id'), primary_key=True)
    student_id = sa.Column(sa.ForeignKey('student.id'), primary_key=True)
    grade = sa.Column(sa.Integer, nullable=False)
    reviewer_id = sa.Column('reviewer_id', sa.Integer, nullable=False)
    student = relationship('StudentModel', back_populates='homeworks')
    homework = relationship('HomeworkModel', back_populates='students')


# todo check if name unique for a
class HomeworkModel(Base):
    __tablename__ = "homework"

    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.Text, nullable=False)
    branch_name = sa.Column('branch_name', sa.Text, nullable=False)

    class_id = sa.Column('class_id', sa.Integer,
                         sa.ForeignKey('class.id'), nullable=False)
    creator_id = sa.Column('creator_id', sa.Integer,
                           sa.ForeignKey('reviewer.id'), nullable=False)
    students = relationship('GradeModel', back_populates='homework')
