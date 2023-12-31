"""create tables

Revision ID: 5b5217015c23
Revises: 
Create Date: 2023-07-24 19:58:43.619228

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5b5217015c23'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('terminal_key', sa.String(length=20), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.String(length=36), nullable=False),
    sa.Column('ip', postgresql.INET(), nullable=True),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.Column('language', sa.Enum('ru', 'en', name='language'), nullable=True),
    sa.Column('recurrent', sa.String(length=1), nullable=False),
    sa.Column('customer_key', sa.String(length=36), nullable=True),
    sa.Column('notification_url', sa.String(), nullable=True),
    sa.Column('success_url', sa.String(), nullable=True),
    sa.Column('fail_url', sa.String(), nullable=True),
    sa.Column('redirect_due_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('pay_type', sa.Enum('O', 'T', name='paytype'), nullable=True),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('payment_url', sa.String(length=100), nullable=False),
    sa.Column('payment_id', sa.BigInteger(), nullable=False),
    sa.Column('payment_status', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payments_payment_id'), 'payments', ['payment_id'], unique=False)
    op.create_table('cancelled_payments',
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('terminal_key', sa.String(length=20), nullable=False),
    sa.Column('payment_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('payment_status', sa.String(), nullable=False),
    sa.Column('original_amount', sa.Integer(), nullable=False),
    sa.Column('new_amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['payment_id'], ['payments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receipts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('phone', sa.String(length=64), nullable=True),
    sa.Column('additional_check_props', sa.String(), nullable=True),
    sa.Column('taxation', sa.Enum('osn', 'usn_income', 'usn_income_outcome', 'patent', 'envd', 'esn', name='taxation'), nullable=False),
    sa.Column('ffd_version', sa.Enum('1.2', '1.05', name='ffdversion'), nullable=True),
    sa.Column('payment_id', sa.Integer(), nullable=True),
    sa.Column('cancelled_payment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cancelled_payment_id'], ['cancelled_payments.id'], ),
    sa.ForeignKeyConstraint(['payment_id'], ['payments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('payment_method', sa.Enum('full_payment', 'full_prepayment', 'prepayment', 'advance', 'partial_payment', 'credit', 'credit_payment', name='paymentmethod'), nullable=True),
    sa.Column('payment_object', sa.Enum('commodity', 'excise', 'job', 'service', 'gambling_bet', 'gambling_prize', 'lottery', 'lottery_prize', 'intellectual_activity', 'payment', 'agent_commission', 'composite', 'another', name='paymentobject'), nullable=True),
    sa.Column('tax', sa.Enum('none', 'vat0', 'vat10', 'vat20', 'vat110', 'vat120', name='tax'), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('ean13', sa.String(length=20), nullable=True),
    sa.Column('receipt_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['receipt_id'], ['receipts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receipt_payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('electronic', sa.Integer(), nullable=False),
    sa.Column('cash', sa.Integer(), nullable=False),
    sa.Column('advance_payment', sa.Integer(), nullable=False),
    sa.Column('credit', sa.Integer(), nullable=False),
    sa.Column('provision', sa.Integer(), nullable=False),
    sa.Column('receipt_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['receipt_id'], ['receipts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('agents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('agent_sign', sa.Enum('bank_paying_agent', 'bank_paying_subagent', 'paying_agent', 'paying_subagent', 'attorney', 'commission_agent', 'another', name='agentsign'), nullable=True),
    sa.Column('operation_name', sa.String(length=64), nullable=True),
    sa.Column('phones', sa.String(), nullable=True),
    sa.Column('receiver_phones', sa.String(), nullable=True),
    sa.Column('transfer_phones', sa.String(), nullable=True),
    sa.Column('operator_name', sa.String(length=64), nullable=True),
    sa.Column('operator_address', sa.String(length=243), nullable=True),
    sa.Column('operator_inn', sa.String(length=12), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('item_id', 'id', name='agent_id_item_id_constr')
    )
    op.create_table('suppliers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phones', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=239), nullable=False),
    sa.Column('inn', sa.String(length=12), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('item_id', 'id', name='supplier_id_item_id_constr')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_table('suppliers')
    op.drop_table('agents')
    op.drop_table('receipt_payments')
    op.drop_table('items')
    op.drop_table('receipts')
    op.drop_table('cancelled_payments')
    op.drop_index(op.f('ix_payments_payment_id'), table_name='payments')
    op.drop_table('payments')
    # ### end Alembic commands ###
