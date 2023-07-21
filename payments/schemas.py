from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator
from pydantic.v1.datetime_parse import parse_datetime


class PayType(str, Enum):
    SINGLE_STAGE = 'O'  # одностадийная
    TWO_STAGE = 'T'  # двухстадийная


class Taxation(str, Enum):
    OSN = 'osn'  # общая
    USN_INCOME = 'usn_income'  # упрощенная (доходы)
    USN_INCOME_OUTCOME = 'usn_income_outcome'  # упрощенная (доходы минус расходы)
    PATENT = 'patent'  # патентная
    ENVD = 'envd'  # единый налог на вмененный доход
    ESN = 'esn'  # единый сельскохозяйственный налог


class FfdVersion(str, Enum):
    VERSION_1_2 = '1.2'
    VERSION_1_05 = '1.05'


class PaymentMethod(str, Enum):
    FULL_PAYMENT = 'full_payment'  # полный расчет
    FULL_PREPAYMENT = 'full_prepayment'  # предоплата 100% - полная предварительная оплата (до получения товара)
    PREPAYMENT = 'prepayment'  # предоплата - частичная предварительная оплата
    ADVANCE = 'advance'  # аванс - предоплата в случаях, когда заранее нельзя определить перечень товаров/работ/услуг
    PARTIAL_PAYMENT = 'partial_payment'  # частичный расчет и кредит
    CREDIT = 'credit'  # передача в кредит
    CREDIT_PAYMENT = 'credit_payment'  # оплата кредита


class PaymentObject(str, Enum):
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


class Tax(str, Enum):
    NONE = 'none'  # без НДС
    VAT0 = 'vat0'  # 0%
    VAT10 = 'vat10'  # 10%
    VAT20 = 'vat20'  # 20%
    VAT110 = 'vat110'  # 10/110
    VAT120 = 'vat120'  # 20/120


class AgentSign(str, Enum):
    BANK_PAYING_AGENT = 'bank_paying_agent'  # банковский платежный агент
    BANK_PAYING_SUBAGENT = 'bank_paying_subagent'  # банковский платежный субагент
    PAYING_AGENT = 'paying_agent'  # платежный агент
    PAYING_SUBAGENT = 'paying_subagent'  # платежный субагент
    ATTORNEY = 'attorney'  # поверенный
    COMMISSION_AGENT = 'commission_agent'  # комиссионер
    ANOTHER = 'another'  # другой тип агента


class Agent(BaseModel):
    agent_sign: AgentSign | None = None
    operation_name: str | None = Field(None, max_length=64)
    phones: str
    receiver_phones: str | None = None
    transfer_phones: str | None = None
    operator_name: str | None = Field(None, max_length=64)
    operator_address: str | None = Field(None, max_length=243)
    operator_inn: str | None = Field(None, max_length=12)


class Supplier(BaseModel):
    phones: str
    name: str = Field(max_length=239)
    inn: str = Field(max_length=12)


class Item(BaseModel):
    name: str = Field(max_length=128)
    quantity: int = Field(gt=0, le=99999999)
    amount: int = Field(gt=0, le=9999999999)
    price: int = Field(gt=0, le=9999999999)
    payment_method: PaymentMethod | None = None
    payment_object: PaymentObject | None = None
    tax: Tax
    ean13: str | None = Field(None, max_length=20)
    agent: Agent | None = None
    supplier: Supplier | None = None


class Receipt(BaseModel):
    email: str = Field(max_length=64)  # Нет, если передан параметр Phone
    phone: str = Field(max_length=64)  # Нет, если передан параметр Email
    taxation: Taxation
    additional_check_props: str | None = None
    ffd_version: FfdVersion | None = None
    items: list[Item]
    # receipt_payment: Mapped['ReceiptPayments'] = relationship(back_populates='receipt')


class PaymentCreate(BaseModel):
    terminal_key: str = Field(max_length=20)
    amount: int = Field(gt=0, le=9999999999)
    order_id: str = Field(max_length=36)
    ip: str | None = Field(None, max_length=40)
    description: str | None = Field(None, max_length=250)
    language: str | None = Field(None, max_length=2)
    recurrent: str = Field(max_length=1, default='Y')
    customer_key: str | None = Field(None, max_length=36)
    redirect_due_date: datetime | None = None
    notification_url: str | None = None
    success_url: str | None = None
    fail_url: str | None = None
    pay_type: PayType | None = None
    data: dict | None = None
    receipt: Receipt | None = None

    class Config:
        from_attributes = True

    @field_validator('redirect_due_date')
    def dt_validate(cls, v):
        v = parse_datetime(v)
        v = v.replace(tzinfo=None)
        return v


class PaymentRead(BaseModel):
    id: int
    payment_url: str | None = None
    status: str | None = 'New'

    class Config:
        from_attributes = True
