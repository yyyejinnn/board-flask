"""empty message

Revision ID: 45e02258ba9f
Revises: 6ad4a1dbb803
Create Date: 2021-07-28 14:18:31.149681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45e02258ba9f'
down_revision = '6ad4a1dbb803'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               existing_server_default=sa.text("'1'"))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               existing_server_default=sa.text("'1'"))

    # ### end Alembic commands ###
