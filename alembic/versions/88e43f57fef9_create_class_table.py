"""CREATE_CLASS_TABLE

Revision ID: 88e43f57fef9
Revises: 646110c1c1d5
Create Date: 2021-12-12 17:20:30.017266

"""
from sqlalchemy.schema import Sequence, CreateSequence, DropSequence
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88e43f57fef9'
down_revision = '646110c1c1d5'
branch_labels = None
depends_on = None

class_table_name = 'class'
classes_to_students_table_name = 'classes_to_students'
classes_to_reviewers_table_name = 'classes_to_reviewers'
id_sequence = Sequence(f'{class_table_name}_seq')


def upgrade():
    op.execute(CreateSequence(id_sequence))
    op.create_table(
        class_table_name,
        sa.Column('id', sa.Integer, id_sequence,
                  server_default=id_sequence.next_value(), primary_key=True),
        sa.Column('name', sa.Text, nullable=False),
        sa.Column('creator_id', sa.Integer,
                  sa.ForeignKey('reviewer.id'), nullable=False),
        sa.UniqueConstraint('name', 'creator_id')
    )
    op.create_table(
        classes_to_students_table_name,
        sa.Column('class_id', sa.Integer, sa.ForeignKey('class.id')),
        sa.Column('student_id', sa.Integer, sa.ForeignKey('student.id')),
        sa.Column('student_nickname', sa.Text)
    )
    op.create_table(
        classes_to_reviewers_table_name,
        sa.Column('class_id', sa.Integer,
                  sa.ForeignKey('class.id'), primary_key=True),
        sa.Column('reviewer_id', sa.Integer,
                  sa.ForeignKey('reviewer.id'), primary_key=True)
    )


def downgrade():
    op.drop_table(classes_to_reviewers_table_name)
    op.drop_table(classes_to_students_table_name)
    op.drop_table(class_table_name)
    op.execute(DropSequence(id_sequence))
