"""add last few column to posts table

Revision ID: e7d242cfafc2
Revises: d94940636e60
Create Date: 2023-03-02 09:30:42.297029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7d242cfafc2'
down_revision = 'd94940636e60'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('published', sa.Boolean(),
                                     nullable= False, server_default='True'))
    op.add_column('posts',
                  sa.Column('create_at', sa.TIMESTAMP(timezone=True),
                                    nullable=False,server_default=sa.text('NOW()')
                  )
                )
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','create_at')
    pass
