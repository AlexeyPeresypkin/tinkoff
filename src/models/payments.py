import enum
from typing import Optional, List

from sqlalchemy import String, ForeignKey, UniqueConstraint, Enum, DateTime, func, BigInteger
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    pass


class PayType(enum.Enum):
    SINGLE_STAGE = 'O'  # одностадийная
    TWO_STAGE = 'T'  # двухстадийная


class Taxation(enum.Enum):
    OSN = 'osn'  # общая
    USN_INCOME = 'usn_income'  # упрощенная (доходы)
    USN_INCOME_OUTCOME = 'usn_income_outcome'  # упрощенная (доходы минус расходы)
    PATENT = 'patent'  # патентная
    ENVD = 'envd'  # единый налог на вмененный доход
    ESN = 'esn'  # единый сельскохозяйственный налог


class FfdVersion(enum.Enum):
    VERSION_1_2 = '1.2'
    VERSION_1_05 = '1.05'


class PaymentMethod(enum.Enum):
    FULL_PAYMENT = 'full_payment'  # полный расчет
    FULL_PREPAYMENT = 'full_prepayment'  # предоплата 100% - полная предварительная оплата (до получения товара)
    PREPAYMENT = 'prepayment'  # предоплата - частичная предварительная оплата
    ADVANCE = 'advance'  # аванс - предоплата в случаях, когда заранее нельзя определить перечень товаров/работ/услуг
    PARTIAL_PAYMENT = 'partial_payment'  # частичный расчет и кредит
    CREDIT = 'credit'  # передача в кредит
    CREDIT_PAYMENT = 'credit_payment'  # оплата кредита


class PaymentObject(enum.Enum):
    COMMODITY = 'commodity'  # товар
    EXCISE = 'excise'  # подакцизный товар
    JOB = 'job'  # работа
    SERVICE = 'service'  # услуга
    GAMBLING_BET = 'gambling_bet'  # ставка азартной игры
    GAMBLING_PRIZE = 'gambling_prize'  # выигрыш азартной игры
    LOTTERY = 'lottery'  # лотерейный билет
    LOTTERY_PRIZE = 'lottery_prize'  # выигрыш лотереи
    INTELLECTUAL_ACTIVITY = 'intellectual_activity'  # предоставление результатов интеллектуальной деятельности
    PAYMENT = 'payment'  # платеж
    AGENT_COMMISSION = 'agent_commission'  # агентское вознаграждение
    COMPOSITE = 'composite'  # составной предмет расчета
    ANOTHER = 'another'  # иной предмет расчета


class Tax(enum.Enum):
    NONE = 'none'  # без НДС
    VAT0 = 'vat0'  # 0%
    VAT10 = 'vat10'  # 10%
    VAT20 = 'vat20'  # 20%
    VAT110 = 'vat110'  # 10/110
    VAT120 = 'vat120'  # 20/120


class AgentSign(enum.Enum):
    BANK_PAYING_AGENT = 'bank_paying_agent'  # банковский платежный агент
    BANK_PAYING_SUBAGENT = 'bank_paying_subagent'  # банковский платежный субагент
    PAYING_AGENT = 'paying_agent'  # платежный агент
    PAYING_SUBAGENT = 'paying_subagent'  # платежный субагент
    ATTORNEY = 'attorney'  # поверенный
    COMMISSION_AGENT = 'commission_agent'  # комиссионер
    ANOTHER = 'another'  # другой тип агента


class Language(enum.Enum):
    RU = 'ru'
    EN = 'en'


class Payments(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(primary_key=True)
    created = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated = mapped_column(DateTime(timezone=True), onupdate=func.now())
    terminal_key: Mapped[str] = mapped_column(String(20))
    amount: Mapped[int]
    order_id: Mapped[str] = mapped_column(String(36))
    ip: Mapped[Optional[str]] = mapped_column(INET)
    description: Mapped[Optional[str]] = mapped_column(String(250))
    language = mapped_column(Enum(Language, values_callable=lambda obj: [e.value for e in obj]))
    recurrent: Mapped[str] = mapped_column(String(1), default='Y')
    customer_key: Mapped[Optional[str]] = mapped_column(String(36))
    redirect_due_date = mapped_column(DateTime(timezone=True))
    notification_url: Mapped[Optional[str]]
    success_url: Mapped[Optional[str]]
    fail_url: Mapped[Optional[str]]
    pay_type = mapped_column(Enum(PayType, values_callable=lambda obj: [e.value for e in obj]))
    data = mapped_column(JSONB)
    payment_url: Mapped[str] = mapped_column(String(100))
    payment_id: Mapped[int] = mapped_column(BigInteger, index=True)
    payment_status: Mapped[Optional[str]] = mapped_column(String(20))
    receipt: Mapped['Receipts'] = relationship(back_populates='payment')
    cancelled_payments: Mapped[Optional['CancelledPayments']] = relationship(back_populates='payment')


class CancelledPayments(Base):
    __tablename__ = 'cancelled_payments'

    created = mapped_column(DateTime(timezone=True), server_default=func.now())
    id: Mapped[int] = mapped_column(primary_key=True)
    terminal_key: Mapped[str] = mapped_column(String(20))
    payment_id: Mapped[int] = mapped_column(ForeignKey('payments.id'))
    amount: Mapped[Optional[int]]
    payment_status: Mapped[str]
    original_amount: Mapped[int]
    new_amount: Mapped[int]
    payment: Mapped['Payments'] = relationship(back_populates='cancelled_payments')
    receipt: Mapped[Optional['Receipts']] = relationship(back_populates='cancelled_payment')


class Receipts(Base):
    __tablename__ = 'receipts'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(String(64))
    phone: Mapped[Optional[str]] = mapped_column(String(64))
    taxation = mapped_column(Enum(Taxation, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    additional_check_props: Mapped[Optional[str]]
    ffd_version = mapped_column(Enum(FfdVersion, values_callable=lambda obj: [e.value for e in obj]))
    payment_id: Mapped[Optional[int]] = mapped_column(ForeignKey('payments.id'))
    cancelled_payment_id: Mapped[Optional[int]] = mapped_column(ForeignKey('cancelled_payments.id'))
    payment: Mapped[Optional['Payments']] = relationship(back_populates='receipt')
    cancelled_payment: Mapped[Optional['CancelledPayments']] = relationship(back_populates='receipt')
    items: Mapped[List['Items']] = relationship(back_populates='receipt')
    receipt_payment: Mapped[Optional['ReceiptPayments']] = relationship(back_populates='receipt')


class ReceiptPayments(Base):
    __tablename__ = 'receipt_payments'

    id: Mapped[int] = mapped_column(primary_key=True)
    electronic: Mapped[int]
    cash: Mapped[int]
    advance_payment: Mapped[int]
    credit: Mapped[int]
    provision: Mapped[int]
    receipt_id: Mapped[int] = mapped_column(ForeignKey('receipts.id'))
    receipt: Mapped['Receipts'] = relationship(back_populates='receipt_payment')


class Items(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    quantity: Mapped[int]
    amount: Mapped[int]
    price: Mapped[int]
    payment_method = mapped_column(Enum(PaymentMethod, values_callable=lambda obj: [e.value for e in obj]))
    payment_object = mapped_column(Enum(PaymentObject, values_callable=lambda obj: [e.value for e in obj]))
    tax = mapped_column(Enum(Tax, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    ean13: Mapped[Optional[str]] = mapped_column(String(20))
    agent: Mapped[Optional['Agents']] = relationship(back_populates='item')
    supplier: Mapped[Optional['Suppliers']] = relationship(back_populates='item')
    receipt_id: Mapped[int] = mapped_column(ForeignKey('receipts.id'))
    receipt: Mapped['Receipts'] = relationship(back_populates='items')


class Agents(Base):
    __tablename__ = 'agents'
    __table_args__ = (UniqueConstraint('item_id', 'id', name='agent_id_item_id_constr'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    agent_sign = mapped_column(Enum(AgentSign, values_callable=lambda obj: [e.value for e in obj]))
    operation_name: Mapped[Optional[str]] = mapped_column(String(64))
    phones: Mapped[Optional[str]]
    receiver_phones: Mapped[Optional[str]]
    transfer_phones: Mapped[Optional[str]]
    operator_name: Mapped[Optional[str]] = mapped_column(String(64))
    operator_address: Mapped[Optional[str]] = mapped_column(String(243))
    operator_inn: Mapped[Optional[str]] = mapped_column(String(12))
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))
    item: Mapped['Items'] = relationship(back_populates='agent')


class Suppliers(Base):
    __tablename__ = 'suppliers'
    __table_args__ = (UniqueConstraint('item_id', 'id', name='supplier_id_item_id_constr'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    phones: Mapped[str]
    name: Mapped[str] = mapped_column(String(239))
    inn: Mapped[str] = mapped_column(String(12))
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))
    item: Mapped['Items'] = relationship(back_populates='supplier')
