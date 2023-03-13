"""empty message

Revision ID: afdf409c9d15
Revises: 938a3a6587c1
Create Date: 2023-03-05 11:40:50.325066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afdf409c9d15'
down_revision = '938a3a6587c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pokemon', schema=None) as batch_op:
        batch_op.alter_column('pokemon_name',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=240),
               existing_nullable=False)
        batch_op.alter_column('ability',
               existing_type=sa.VARCHAR(length=140),
               type_=sa.String(length=240),
               existing_nullable=True)
        batch_op.alter_column('type',
               existing_type=sa.VARCHAR(length=40),
               type_=sa.String(length=240),
               existing_nullable=True)
        batch_op.alter_column('sprite',
               existing_type=sa.VARCHAR(length=40),
               type_=sa.String(length=240),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pokemon', schema=None) as batch_op:
        batch_op.alter_column('sprite',
               existing_type=sa.String(length=240),
               type_=sa.VARCHAR(length=40),
               existing_nullable=True)
        batch_op.alter_column('type',
               existing_type=sa.String(length=240),
               type_=sa.VARCHAR(length=40),
               existing_nullable=True)
        batch_op.alter_column('ability',
               existing_type=sa.String(length=240),
               type_=sa.VARCHAR(length=140),
               existing_nullable=True)
        batch_op.alter_column('pokemon_name',
               existing_type=sa.String(length=240),
               type_=sa.VARCHAR(length=64),
               existing_nullable=False)

    # ### end Alembic commands ###
