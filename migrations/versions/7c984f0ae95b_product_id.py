"""product id

Revision ID: 7c984f0ae95b
Revises: 86dcae090f6b
Create Date: 2022-08-31 22:56:04.101436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c984f0ae95b'
down_revision = '86dcae090f6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products_for_order', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('products_for_order', 'p_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products_for_order', sa.Column('p_id', sa.INTEGER(), nullable=False))
    op.alter_column('products_for_order', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###