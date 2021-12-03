"""CREATE_USER_TABLE

Revision ID: b58a9e6c9fe6
Revises: 
Create Date: 2021-11-29 14:59:32.220996

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import Sequence, CreateSequence, DropSequence


# revision identifiers, used by Alembic.
revision = 'b58a9e6c9fe6'
down_revision = None
branch_labels = None
depends_on = None


table_name = 'utilisateur'
id_sequence = Sequence(f'{table_name}_seq')


def upgrade():
    # todo logging
    op.execute(CreateSequence(id_sequence))
    op.create_table(
        table_name,
        sa.Column('id', sa.Integer, id_sequence, server_default=id_sequence.next_value(), primary_key=True),
        sa.Column('github_login', sa.String(39), nullable=False, unique=True),
        sa.Column('nickname', sa.TEXT, nullable=False),
        sa.Column('email', sa.TEXT, nullable=False)
    )


def downgrade():
    op.drop_table(table_name)
    op.execute(DropSequence(id_sequence))
