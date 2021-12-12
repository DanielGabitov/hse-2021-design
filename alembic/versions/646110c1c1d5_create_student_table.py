"""CREATE_STUDENT_TABLE

Revision ID: 646110c1c1d5
Revises: b58a9e6c9fe6
Create Date: 2021-12-12 17:20:13.122861

"""
from sqlalchemy.schema import Sequence, CreateSequence, DropSequence
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '646110c1c1d5'
down_revision = 'b58a9e6c9fe6'
branch_labels = None
depends_on = None

table_name = 'student'
id_sequence = Sequence(f'{table_name}_seq')


def upgrade():
    op.execute(CreateSequence(id_sequence))
    op.create_table(
        table_name,
        sa.Column('id', sa.Integer, id_sequence, server_default=id_sequence.next_value(), primary_key=True),
        sa.Column('username', sa.String(39), nullable=False, unique=True),
    )


def downgrade():
    op.drop_table(table_name)
    op.execute(DropSequence(id_sequence))
