"""empty message

Revision ID: 7b06b0e7544d
Revises: 
Create Date: 2019-09-25 21:51:20.475821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b06b0e7544d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.String(length=64), nullable=True),
    sa.Column('data', sa.String(length=64), nullable=True),
    sa.Column('remark', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cctvs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('avatar', sa.String(length=255), nullable=True),
    sa.Column('port', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.String(length=64), nullable=True),
    sa.Column('data', sa.String(length=64), nullable=True),
    sa.Column('remark', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('phs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.String(length=64), nullable=True),
    sa.Column('data', sa.String(length=64), nullable=True),
    sa.Column('remark', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rcpts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('number', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('rcpts')
    op.drop_table('phs')
    op.drop_table('cods')
    op.drop_table('cctvs')
    op.drop_table('bods')
    # ### end Alembic commands ###