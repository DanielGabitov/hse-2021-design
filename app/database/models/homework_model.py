import sqlalchemy as sa

from app.database.setup import Base


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
