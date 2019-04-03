"""empty message

Revision ID: 81ccb9046d0f
Revises: aabe182b6346
Create Date: 2019-03-21 09:54:34.938947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81ccb9046d0f'
down_revision = 'aabe182b6346'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('city', sa.String(length=80), nullable=False))
    op.add_column('items', sa.Column('country', sa.String(length=80), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items', 'country')
    op.drop_column('items', 'city')
    # ### end Alembic commands ###