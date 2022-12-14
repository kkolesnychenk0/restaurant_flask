"""product_order

Revision ID: fea91c3e0a16
Revises: 6b9170de22c6
Create Date: 2022-08-16 13:39:02.923766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fea91c3e0a16'
down_revision = '6b9170de22c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products_for_order', sa.Column('p_id', sa.Integer(), nullable=False))
    op.drop_column('products_for_order', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products_for_order', sa.Column('id', sa.INTEGER(), nullable=False))
    op.drop_column('products_for_order', 'p_id')
    # ### end Alembic commands ###
