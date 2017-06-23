"""Add API keys for users

Revision ID: 2b33b3124266
Revises: 5f64132e92d5
Create Date: 2017-06-23 15:06:14.593787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b33b3124266'
down_revision = '5f64132e92d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('api_enabled', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'api_enabled')
    # ### end Alembic commands ###
