"""create tables3

Revision ID: d693e33dc9e0
Revises: 39216b1d6526
Create Date: 2023-07-23 11:52:10.433189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd693e33dc9e0'
down_revision = '39216b1d6526'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cancelled_payments',
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('terminal_key', sa.String(length=20), nullable=False),
    sa.Column('payment_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['payment_id'], ['payments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('receipts', sa.Column('cancelled_payment_id', sa.Integer(), nullable=True))
    op.alter_column('receipts', 'payment_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_foreign_key(None, 'receipts', 'cancelled_payments', ['cancelled_payment_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'receipts', type_='foreignkey')
    op.alter_column('receipts', 'payment_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('receipts', 'cancelled_payment_id')
    op.drop_table('cancelled_payments')
    # ### end Alembic commands ###
