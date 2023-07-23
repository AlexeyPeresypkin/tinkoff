import json
from datetime import datetime, date, time
from enum import Enum
from hashlib import sha256

import aiohttp
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from payments import models

TERMINAL_PASSWORD = 'TinkoffBankTest'
headers = {'content-type': 'application/json'}


# TERMINAL_PASSWORD = os.getenv('TERMINAL_PASSWORD')

def default(obj):
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat(timespec='seconds')
    elif isinstance(obj, Enum):
        return obj.value
    return obj


def normalize_value(value):
    if isinstance(value, datetime):
        return value.isoformat(timespec='seconds')
    elif isinstance(value, Enum):
        return value.value  # noqa
    elif isinstance(value, int):
        return str(value)
    return value


def get_token(data: dict):
    data = data.copy()
    exclude_keys = ('Receipt', 'DATA')
    data.update({"Password": TERMINAL_PASSWORD})
    list_data = [(key, normalize_value(v)) for key, v in data.items() if key not in exclude_keys and v]
    list_data = [x[1] for x in sorted(list_data, key=lambda x: x[0])]
    data_for_token = ''.join(list_data)
    token = sha256(data_for_token.encode('utf-8')).hexdigest()
    return token


def to_camel(string: str) -> str:
    camel_cases = {'receipt_payment': 'Payments', 'agent': 'AgentData', 'supplier': 'SupplierInfo'}
    return camel_cases.get(string) or ''.join(word.capitalize() if word not in ('url', 'data', 'ip')
                                              else word.upper() for word in string.split('_'))


def get_camel_case_data(data: dict):
    # Конвертируем ключи payload в camel_case стиль для запроса
    for key in list(data):
        data_key = data.pop(key)
        if isinstance(data_key, dict):
            data[to_camel(key)] = get_camel_case_data(data_key)
        elif isinstance(data_key, list):
            data[to_camel(key)] = [get_camel_case_data(item) if isinstance(item, dict) else item for item in data_key]
        else:
            data[to_camel(key)] = data_key
    return data


def create_receipt_payment(db: AsyncSession, receipt: models.Receipts, receipt_payment: dict | None):
    if receipt_payment:
        receipt_payment = models.ReceiptPayments(**receipt_payment, receipt=receipt)
        db.add(receipt_payment)


def get_payload(data: dict) -> json:
    camel_case_data = get_camel_case_data(data)
    token = get_token(camel_case_data)
    camel_case_data.update({'Token': token})
    data = {k: v for k, v in camel_case_data.items() if v}
    return json.dumps(data, default=default)


async def get_response_or_400(url: str, payload: json) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as resp:
            response: dict = await resp.json()
        if not response.get('Success'):
            message = response.get('Message')
            details = response.get('Details')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{message} {details}')
        return response


def get_payload_init(data: dict) -> json:
    data = {k: v for k, v in data.items() if v}
    return json.dumps(data, default=default)


def create_agent(db: AsyncSession, item: models.Items, agent: dict | None):
    if agent:
        agent['phones'] = ', '.join(agent['phones'])
        agent['receiver_phones'] = ', '.join(agent['receiver_phones'])
        agent['transfer_phones'] = ', '.join(agent['transfer_phones'])
        agent = models.Agents(**agent, item=item)
        db.add(agent)


def create_supplier(db: AsyncSession, item: models.Items, supplier: dict | None):
    if supplier:
        supplier['phones'] = ', '.join(supplier['phones'])
        supplier = models.Suppliers(**supplier, item=item)
        db.add(supplier)


async def create_items(db: AsyncSession, receipt: models.Receipts, items: list[dict] | None):
    if items:
        for item in items:
            agent = item.pop('agent', None)
            supplier = item.pop('supplier', None)
            item = models.Items(**item, receipt=receipt)
            db.add(item)
            await db.flush()
            create_agent(db, item, agent)
            create_supplier(db, item, supplier)


async def create_receipt(
        db: AsyncSession,
        obj_model: models.CancelledPayments | models.Payments,
        receipt: dict | None):
    if not receipt:
        return
    items = receipt.pop('items', None)
    receipt_payment = receipt.pop('receipt_payment', None)
    if isinstance(obj_model, models.CancelledPayments):
        receipt = models.Receipts(**receipt, cancelled_payment=obj_model)
    elif isinstance(obj_model, models.Payments):
        receipt = models.Receipts(**receipt, payment=obj_model)
    db.add(receipt)
    await db.flush()
    await create_items(db, receipt, items)
    create_receipt_payment(db, receipt, receipt_payment)


async def get_payment_or_404(db: AsyncSession, payment_id: int) -> models.Payments:
    stmt = select(models.Payments).where(models.Payments.payment_id == payment_id)
    payment = await db.execute(stmt)
    payment = payment.scalar_one_or_none()
    if payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return payment
