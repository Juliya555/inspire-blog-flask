"""empty message

Revision ID: ea790a5492c1
Revises: c5f39c13dc84
Create Date: 2018-03-13 23:07:39.011588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea790a5492c1'
down_revision = 'c5f39c13dc84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'post', 'category', ['category_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    # ### end Alembic commands ###
