"""Added FileMetaData tabke

Revision ID: 2bfd8cc61834
Revises: 
Create Date: 2024-08-26 14:40:50.118954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bfd8cc61834'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('s3_url', sa.String(length=255), nullable=True),
    sa.Column('current_bytes', sa.Integer(), nullable=True),
    sa.Column('is_stream', sa.Boolean(), nullable=True),
    sa.Column('is_ready', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('file_meta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original_title', sa.String(length=255), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('content_type', sa.String(length=255), nullable=True),
    sa.Column('extension', sa.String(length=255), nullable=True),
    sa.Column('file_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['file_id'], ['file.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file_meta')
    op.drop_table('file')
    # ### end Alembic commands ###
