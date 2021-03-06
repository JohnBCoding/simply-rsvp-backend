"""empty message

Revision ID: 9311ef35530e
Revises: 
Create Date: 2021-09-21 19:02:32.385065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9311ef35530e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creator_fn', sa.String(), nullable=True),
    sa.Column('creator_ln', sa.String(), nullable=True),
    sa.Column('creator_email', sa.String(), nullable=True),
    sa.Column('event_desc', sa.Text(), nullable=True),
    sa.Column('event_date', sa.Date(), nullable=True),
    sa.Column('event_time', sa.Time(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invited',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invited_email', sa.String(), nullable=True),
    sa.Column('invite_code', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invited')
    op.drop_table('events')
    # ### end Alembic commands ###
