"""poke ability upgrade

Revision ID: 938a3a6587c1
Revises: 84417dec1d41
Create Date: 2023-03-05 11:38:10.765452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '938a3a6587c1'
down_revision = '84417dec1d41'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pokemon', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ability', sa.String(length=140), nullable=True))
        batch_op.drop_column('abilities')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pokemon', schema=None) as batch_op:
        batch_op.add_column(sa.Column('abilities', sa.VARCHAR(length=140), autoincrement=False, nullable=True))
        batch_op.drop_column('ability')

    # ### end Alembic commands ###
