"""Changed relationship

Revision ID: 4f3d5def8ea9
Revises: ad2b1183086d
Create Date: 2024-08-28 03:29:18.877230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f3d5def8ea9'
down_revision: Union[str, None] = 'ad2b1183086d'
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
