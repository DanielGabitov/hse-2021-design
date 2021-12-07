"""create_class_table

Revision ID: 767cf6782aa3
Revises: b58a9e6c9fe6
Create Date: 2021-12-03 22:58:07.053698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import Sequence, ForeignKey, UniqueConstraint
from sqlalchemy.sql.ddl import CreateSequence, DropSequence

revision = '767cf6782aa3'
down_revision = 'b58a9e6c9fe6'
branch_labels = None
depends_on = None


table_name = 'class'
id_sequence = Sequence(f'{table_name}_seq')


def upgrade():
    op.execute(CreateSequence(id_sequence))
    op.create_table(
        table_name,
        sa.Column('id', sa.Integer, id_sequence, server_default=id_sequence.next_value(), primary_key=True),
        sa.Column('name', sa.Text, nullable=False),
        sa.Column('creator_id', sa.Integer, sa.ForeignKey('utilisateur.id'), nullable=False),
        sa.UniqueConstraint('name', 'creator_id')
    )


def downgrade():
    op.drop_table(table_name)
    op.execute(DropSequence(id_sequence))

