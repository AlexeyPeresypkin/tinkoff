import enum
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    pass


class PayType(enum.Enum):
    single_stage = 'O'  # одностадийная
    two_stage = 'T'  # двухстадийная


class Taxation(enum.Enum):
    OSN = 'osn'  # общая
    USN_INCOME = 'usn_income'  # упрощенная (доходы)
    USN_INCOME_OUTCOME = 'usn_income_outcome'  # упрощенная (доходы минус расходы)
    PATENT = 'patent'  # патентная
    ENVD = 'envd'  # единый налог на вмененный доход
    ESN = 'esn'  # единый сельскохозяйственный налог


class FfdVersion(enum.Enum):
    version_1_2 = '1.2'
    version_1_05 = '1.05'


class PaymentType(enum.Enum):
    Cash = 'Cash'  # Наличные
    Electronic = 'Electronic'  # Безналичный
    AdvancePayment = 'AdvancePayment'  # Предварительная оплата (Аванс)
    Credit = 'Credit'  # Постоплата (Кредит)
    Provision = 'Provision'  # Иная форма оплаты


class PaymentMethod(enum.Enum):
    full_payment = 'full_payment'  # полный расчет
    full_prepayment = 'full_prepayment'  # предоплата 100% - полная предварительная оплата (до получения товара)
    prepayment = 'prepayment'  # предоплата - частичная предварительная оплата
    advance = 'advance'  # аванс - предоплата в случаях, когда заранее нельзя определить перечень товаров/работ/услуг
    partial_payment = 'partial_payment'  # частичный расчет и кредит
    credit = 'credit'  # передача в кредит
    credit_payment = 'credit_payment'  # оплата кредита


class PaymentObject(enum.Enum):
    commodity = 'commodity'  # товар
    excise = 'excise'  # подакцизный товар
    job = 'job'  # работа
    service = 'service'  # услуга
    gambling_bet = 'gambling_bet'  # ставка азартной игры
    gambling_prize = 'gambling_prize'  # выигрыш азартной игры
    lottery = 'lottery'  # лотерейный билет
    lottery_prize = 'lottery_prize'  # выигрыш лотереи
    intellectual_activity = 'intellectual_activity'  # предоставление результатов интеллектуальной деятельности
    payment = 'payment'  # платеж
    agent_commission = 'agent_commission'  # агентское вознаграждение
    composite = 'composite'  # составной предмет расчета
    another = 'another'  # иной предмет расчета


class Tax(enum.Enum):
    none = 'none'  # без НДС
    vat0 = 'vat0'  # 0%
    vat10 = 'vat10'  # 10%
    vat20 = 'vat20'  # 20%
    vat110 = 'vat110'  # 10/110
    vat120 = 'vat120'  # 20/120


class AgentSign(enum.Enum):
    bank_paying_agent = 'bank_paying_agent'  # банковский платежный агент
    bank_paying_subagent = 'bank_paying_subagent'  # банковский платежный субагент
    paying_agent = 'paying_agent'  # платежный агент
    paying_subagent = 'paying_subagent'  # платежный субагент
    attorney = 'attorney'  # поверенный
    commission_agent = 'commission_agent'  # комиссионер
    another = 'another'  # другой тип агента


class Payments(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(primary_key=True)
    TerminalKey: Mapped[str] = mapped_column(String(20))
    Amount: Mapped[int]
    OrderId: Mapped[str] = mapped_column(String(36))
    ip: Mapped[Optional[str]] = mapped_column(INET)
    Description: Mapped[str] = mapped_column(String(250))
    # Token
    Language: Mapped[str] = mapped_column(String(2))
    Recurrent: Mapped[str] = mapped_column(String(1))
    CustomerKey: Mapped[str] = mapped_column(String(36))
    RedirectDueDate: Mapped[Optional[datetime]]
    NotificationURL: Mapped[Optional[str]]
    SuccessURL: Mapped[Optional[str]]
    FailURL: Mapped[Optional[str]]
    PayType: Mapped[PayType]
    DATA = mapped_column(JSONB, nullable=True)

    receipts: Mapped[List['Receipts']] = relationship(back_populates='payment')


class Receipts(Base):
    __tablename__ = 'receipts'

    Email: Mapped[str] = mapped_column(String(64))
    Phone: Mapped[str] = mapped_column(String(64))
    Taxation: Mapped[Taxation]
    # Items = mapped_column(JSONB, nullable=True)
    # Payments = mapped_column(JSONB, nullable=True)
    AdditionalCheckProps: Mapped[str]
    FfdVersion: Mapped[FfdVersion]
    receipt_payments: Mapped[int] = mapped_column(ForeignKey('receipt_payments.id'))
    payment_id: Mapped[int] = mapped_column(ForeignKey('payments.id'))

    payment: Mapped['Payments'] = relationship(back_populates='receipts')
    items: Mapped['Items'] = relationship(back_populates='receipt')


class ReceiptPayments(Base):
    __tablename__ = 'receipt_payments'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[PaymentType]
    amount: Mapped[int]
    receipt: Mapped[int] = mapped_column(ForeignKey('receipts.id'))


class Items(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(128))
    Quantity: Mapped[int]
    Amount: Mapped[int]
    Price: Mapped[int]
    PaymentMethod: Mapped[PaymentMethod]
    PaymentObject: Mapped[PaymentObject]
    Tax: Mapped[Tax]
    Ean13: Mapped[Optional[str]] = mapped_column(String(20))
    AgentData
    SupplierInfo


class Agents(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    AgentSign: Mapped[Optional[AgentSign]]
    OperationName: Mapped[Optional[str]] = mapped_column(String(64))
    Phones: Mapped[Optional[str]]
    ReceiverPhones: Mapped[Optional[str]]
    TransferPhones: Mapped[Optional[str]]
    OperatorName: Mapped[Optional[str]] = mapped_column(String(64))
    OperatorAddress: Mapped[Optional[str]] = mapped_column(String(243))
    OperatorInn: Mapped[Optional[str]] = mapped_column(String(12))
