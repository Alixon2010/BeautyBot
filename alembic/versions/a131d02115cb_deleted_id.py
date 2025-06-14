"""deleted id

Revision ID: a131d02115cb
Revises: 725582f7b317
Create Date: 2025-06-04 19:15:29.291110

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a131d02115cb'
down_revision: Union[str, None] = '725582f7b317'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('users_chat_id_key'), 'users', type_='unique')
    op.drop_column('users', 'id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.create_unique_constraint(op.f('users_chat_id_key'), 'users', ['chat_id'], postgresql_nulls_not_distinct=False)
    # ### end Alembic commands ###
