"""Changed relationship

Revision ID: 8c6b5b5f3a8d
Revises: 4f3d5def8ea9
Create Date: 2024-08-28 03:29:49.947131

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c6b5b5f3a8d'
down_revision: Union[str, None] = '4f3d5def8ea9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
