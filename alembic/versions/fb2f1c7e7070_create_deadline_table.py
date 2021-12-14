"""CREATE_DEADLINE_TABLE

Revision ID: fb2f1c7e7070
Revises: d18e0df40ab6
Create Date: 2021-12-13 16:52:19.110727

"""
from sqlalchemy.schema import Sequence, CreateSequence, DropSequence
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb2f1c7e7070'
down_revision = 'd18e0df40ab6'
branch_labels = None
depends_on = None


table_name = 'deadline'
id_sequence = Sequence(f'{table_name}_seq')


# todo look for proper way to work with time
def upgrade():
    op.execute(CreateSequence(id_sequence))
    op.create_table(
        table_name,
        sa.Column('id', sa.Integer, id_sequence,
                  server_default=id_sequence.next_value(), primary_key=True),
        sa.Column('homework_id', sa.Integer,
                  sa.ForeignKey('homework.id'), unique=True, nullable=False),
        sa.Column('creator_id', sa.Integer,
                  sa.ForeignKey('reviewer.id'), nullable=False),
        sa.Column('time', sa.TIMESTAMP, nullable=False),
    )


def downgrade():
    op.drop_table(table_name)
    op.execute(DropSequence(id_sequence))
