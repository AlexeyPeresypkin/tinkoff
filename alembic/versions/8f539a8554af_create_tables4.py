"""create tables4

Revision ID: 8f539a8554af
Revises: d693e33dc9e0
Create Date: 2023-07-23 12:36:25.713512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f539a8554af'
down_revision = 'd693e33dc9e0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cancelled_payments', sa.Column('status', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cancelled_payments', 'status')
    # ### end Alembic commands ###