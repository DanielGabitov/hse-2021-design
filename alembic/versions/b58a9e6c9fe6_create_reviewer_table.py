"""CREATE_REVIEWER_TABLE

Revision ID: b58a9e6c9fe6
Revises:
Create Date: 2021-11-29 14:59:32.220996

"""
from sqlalchemy.schema import Sequence, CreateSequence, DropSequence
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b58a9e6c9fe6'
down_revision = None
branch_labels = None
depends_on = None


table_name = 'reviewer'
id_sequence = Sequence(f'{table_name}_seq')


def upgrade():
    op.execute(CreateSequence(id_sequence))
    op.create_table(
        table_name,
        sa.Column('id', sa.Integer, id_sequence,
                  server_default=id_sequence.next_value(), primary_key=True),
        sa.Column('username', sa.String(39), nullable=False, unique=True),
        sa.Column('nickname', sa.Text, nullable=False),
        sa.Column('email', sa.TEXT, nullable=False)
    )


def downgrade():
    op.drop_table(table_name)
    op.execute(DropSequence(id_sequence))
