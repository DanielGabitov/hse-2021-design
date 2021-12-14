import sqlalchemy as sa

from app.database.setup import Base


class DeadlineModel(Base):
    __tablename__ = "deadline"

    id = sa.Column('id', sa.Integer, primary_key=True)
    homework_id = sa.Column('class_id', sa.Integer,
                            sa.ForeignKey('homework.id'), nullable=False)
    creator_id = sa.Column('creator_id', sa.Integer,
                           sa.ForeignKey('reviewer.id'), nullable=False)
    time = sa.Column('time', sa.TIMESTAMP, nullable=False)
