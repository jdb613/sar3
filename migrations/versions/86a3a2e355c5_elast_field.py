"""+elast field

Revision ID: 86a3a2e355c5
Revises: c95a91dfc64b
Create Date: 2018-10-13 17:22:03.645042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86a3a2e355c5'
down_revision = 'c95a91dfc64b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('leaver', sa.Column('elast', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_leaver_elast'), 'leaver', ['elast'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_leaver_elast'), table_name='leaver')
    op.drop_column('leaver', 'elast')
    # ### end Alembic commands ###
