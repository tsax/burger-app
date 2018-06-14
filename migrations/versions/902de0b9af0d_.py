"""empty message

Revision ID: 902de0b9af0d
Revises: e4ce2f447eb8
Create Date: 2018-06-14 02:46:53.425529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '902de0b9af0d'
down_revision = 'e4ce2f447eb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('burgers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('has_bun', sa.Boolean(), server_default=sa.text('true'), nullable=True),
    sa.Column('has_patty', sa.Boolean(), server_default=sa.text('true'), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('toppings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('topping_burger_join_table',
    sa.Column('burger_id', sa.Integer(), nullable=True),
    sa.Column('topping_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['burger_id'], ['burgers.id'], ),
    sa.ForeignKeyConstraint(['topping_id'], ['toppings.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('topping_burger_join_table')
    op.drop_table('toppings')
    op.drop_table('burgers')
    # ### end Alembic commands ###
