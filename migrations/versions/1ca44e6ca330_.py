"""empty message

Revision ID: 1ca44e6ca330
Revises: af2aba323fb9
Create Date: 2018-03-19 00:36:14.695580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ca44e6ca330'
down_revision = 'af2aba323fb9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post_image', sa.Column('is_main', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post_image', 'is_main')
    # ### end Alembic commands ###
