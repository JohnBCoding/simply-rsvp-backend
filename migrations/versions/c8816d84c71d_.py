"""empty message

Revision ID: c8816d84c71d
Revises: 9311ef35530e
Create Date: 2021-11-17 17:15:22.758693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8816d84c71d'
down_revision = '9311ef35530e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('event_location', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'event_location')
    # ### end Alembic commands ###
