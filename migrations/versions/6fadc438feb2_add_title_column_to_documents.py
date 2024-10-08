"""Add title column to documents

Revision ID: 6fadc438feb2
Revises: 
Create Date: 2024-09-06 01:49:36.373180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fadc438feb2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('documents', sa.Column('title', sa.String(length=255), nullable=True))
    op.add_column('documents', sa.Column('content', sa.Text(), nullable=True))
    op.create_index(op.f('ix_documents_content'), 'documents', ['content'], unique=False)
    op.create_index(op.f('ix_documents_title'), 'documents', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_documents_title'), table_name='documents')
    op.drop_index(op.f('ix_documents_content'), table_name='documents')
    op.drop_column('documents', 'content')
    op.drop_column('documents', 'title')
    # ### end Alembic commands ###
