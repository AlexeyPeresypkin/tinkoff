import re
from datetime import datetime

from fastapi import status
from pydantic import BaseModel, Field, field_validator

from payments import models


class Agent(BaseModel):
    agent_sign: models.AgentSign | None = None
    operation_name: str | None = Field(None, max_length=64)
    phones: list[str] | None = None
    receiver_phones: list[str] | None = None
    transfer_phones: list[str] | None = None
    operator_name: str | None = Field(None, max_length=64)
    operator_address: str | None = Field(None, max_length=243)
    operator_inn: str | None = Field(None, max_length=12)

    @field_validator('operator_inn')
    def operator_inn_validate(cls, v):
        pattern = '^(\\d{10}|\\d{12})$'
        if not re.search(pattern, v):
            raise ValueError('operator_inn must be 10 or 12 digits')
        return v


class Supplier(BaseModel):
    phones: list[str] | None = None
    name: str | None = Field(None, max_length=239)
    inn: str | None = Field(None, max_length=12)

    @field_validator('inn')
    def inn_validate(cls, v):
        pattern = '^(\\d{10}|\\d{12})$'
        if not re.search(pattern, v):
            raise ValueError('inn must be 10 or 12 digits')
        return v


class Item(BaseModel):
    name: str = Field(max_length=128)
    quantity: int = Field(gt=0, le=99999999)
    amount: int = Field(gt=0, le=9999999999)
    price: int = Field(gt=0, le=9999999999)
    payment_method: models.PaymentMethod | None = None
    payment_object: models.PaymentObject | None = None
    tax: models.Tax
    ean13: str | None = Field(None, max_length=20)
    agent: Agent | None = None
    supplier: Supplier | None = None


class ReceiptPayments(BaseModel):
    cash: int | None = Field(None, ge=0, le=99999999999999)
    electronic: int = Field(ge=0, le=99999999999999)
    advance_payment: int | None = Field(None, ge=0, le=99999999999999)
    credit: int | None = Field(None, ge=0, le=99999999999999)
    provision: int | None = Field(None, ge=0, le=99999999999999)


class Receipt(BaseModel):
    email: str = Field(max_length=64)
    phone: str = Field(max_length=64)
    taxation: models.Taxation
    additional_check_props: str | None = None
    ffd_version: models.FfdVersion | None = None
    items: list[Item]
    receipt_payment: ReceiptPayments | None = None


class PaymentCreate(BaseModel):
    terminal_key: str = Field(max_length=20)
    amount: int = Field(gt=0, le=9999999999)
    order_id: str = Field(max_length=36)
    ip: str | None = Field(None, max_length=40)
    description: str | None = Field(None, max_length=250)
    language: str | None = Field(None, max_length=2)
    customer_key: str | None = Field(None, max_length=36)
    redirect_due_date: datetime | None = None
    notification_url: str | None = None
    success_url: str | None = None
    fail_url: str | None = None
    pay_type: models.PayType | None = None
    data: dict | None = None
    receipt: Receipt | None = None


class PaymentRead(BaseModel):
    payment_url: str
    payment_id: int

    class Config:
        from_attributes = True


class CancelPaymentCreate(BaseModel):
    terminal_key: str = Field(max_length=20)
    payment_id: int
    amount: int | None = Field(None, ge=100, le=9999999999)
    receipt: Receipt | None = None


class PaymentStatusCreate(BaseModel):
    terminal_key: str = Field(max_length=20)
    payment_id: int


class PaymentStatusRead(BaseModel):
    payment_status: str

    class Config:
        from_attributes = True


class ErrorModel(BaseModel):
    detail: str


schema_400 = {
    "model": ErrorModel,
    "content": {
        "application/json": {
            "examples": {
                'Bad request': {
                    "value": {
                        "detail": 'Информация об ошибке'
                    },
                }
            },
        },
    }
}

schema_404 = {
    "content": {
        "application/json": {
            "examples": {
                'Not Found': {
                    "value": {
                        "detail": 'Not Found'
                    },
                }
            },
        },
    }
}

bad_request_common = {
    status.HTTP_400_BAD_REQUEST: schema_400
}

bad_request_with_404 = {
    status.HTTP_400_BAD_REQUEST: schema_400,
    status.HTTP_404_NOT_FOUND: schema_404
}
