"""CREATE_HW_TABLE

Revision ID: d18e0df40ab6
Revises: 88e43f57fef9
Create Date: 2021-12-12 21:58:24.282855

"""
from sqlalchemy.schema import Sequence, CreateSequence, DropSequence
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd18e0df40ab6'
down_revision = '88e43f57fef9'
branch_labels = None
depends_on = None


table_name = 'homework'
id_sequence = Sequence(f'{table_name}_seq')


def upgrade():
    op.execute(CreateSequence(id_sequence))
    op.create_table(
        table_name,
        sa.Column('id', sa.Integer, id_sequence,
                  server_default=id_sequence.next_value(), primary_key=True),
        sa.Column('class_id', sa.Integer,
                  sa.ForeignKey('class.id'), nullable=False),
        sa.Column('creator_id', sa.Integer,
                  sa.ForeignKey('reviewer.id'), nullable=False),
        sa.Column('name', sa.Text, nullable=False),
        sa.Column('branch_name', sa.Text, nullable=False),
        sa.UniqueConstraint('name', 'creator_id'),
        sa.UniqueConstraint('name', 'branch_name')
    )


def downgrade():
    op.drop_table(table_name)
    op.execute(DropSequence(id_sequence))
