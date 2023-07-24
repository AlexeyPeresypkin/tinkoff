import json

import aiohttp
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.payments import Payments, CancelledPayments, Receipts, Agents, Suppliers, Items, ReceiptPayments
from schemas.payments import PaymentCreate
from services import utils


class PaymentService:
    def __init__(self, db: AsyncSession):
        self.headers = {'content-type': 'application/json'}
        self.db = db
        self._create_payment_url = 'https://securepay.tinkoff.ru/v2/Init'
        self.headers = {'content-type': 'application/json'}

    async def create_payment(self, payment_create: PaymentCreate):
        payload = utils.get_payload(payment_create.model_dump())
        response = await self.get_response_or_400(self._create_payment_url, payload)
        data = payment_create.model_dump()
        receipt = data.pop('receipt', None)
        payment = Payments(
            **data,
            payment_id=int(response.get('PaymentId')),
            payment_url=response.get('PaymentURL'),
            payment_status=response.get('Status'))
        self.db.add(payment)
        await self.db.flush()
        await self.create_receipt(payment, receipt)
        await self.db.commit()

    async def update_payment_status_or_none(self, payment: Payments, payment_status: str):
        if payment.payment_status != payment_status:
            payment.payment_status = payment_status
            self.db.add(payment)
            await self.db.commit()

    async def get_payment_or_404(self, payment_id: int) -> Payments:
        stmt = select(Payments).where(Payments.payment_id == payment_id)
        payment = await self.db.execute(stmt)
        payment = payment.scalar_one_or_none()
        if payment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return payment

    async def create_receipt(
            self,
            obj_model: CancelledPayments | Payments,
            receipt: dict | None):
        if not receipt:
            return
        items = receipt.pop('items', None)
        receipt_payment = receipt.pop('receipt_payment', None)
        if isinstance(obj_model, CancelledPayments):
            receipt = Receipts(**receipt, cancelled_payment=obj_model)
        elif isinstance(obj_model, Payments):
            receipt = Receipts(**receipt, payment=obj_model)
        self.db.add(receipt)
        await self.db.flush()
        await self.create_items(receipt, items)
        self.create_receipt_payment(receipt, receipt_payment)

    def create_agent(self, item: Items, agent: dict | None):
        if agent:
            agent['phones'] = ', '.join(agent['phones'])
            agent['receiver_phones'] = ', '.join(agent['receiver_phones'])
            agent['transfer_phones'] = ', '.join(agent['transfer_phones'])
            agent = Agents(**agent, item=item)
            self.db.add(agent)

    def create_supplier(self, item: Items, supplier: dict | None):
        if supplier:
            supplier['phones'] = ', '.join(supplier['phones'])
            supplier = Suppliers(**supplier, item=item)
            self.db.add(supplier)

    async def create_items(self, receipt: Receipts, items: list[dict] | None) -> None:
        if items:
            for item in items:
                agent = item.pop('agent', None)
                supplier = item.pop('supplier', None)
                item = Items(**item, receipt=receipt)
                self.db.add(item)
                await self.db.flush()
                self.create_agent(item, agent)
                self.create_supplier(item, supplier)

    def create_receipt_payment(self, receipt: Receipts, receipt_payment: dict | None):
        if receipt_payment:
            receipt_payment = ReceiptPayments(**receipt_payment, receipt=receipt)
            self.db.add(receipt_payment)

    async def get_response_or_400(self, url: str, payload: json) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=self.headers) as resp:
                response: dict = await resp.json()
            if not response.get('Success'):
                message = response.get('Message')
                details = response.get('Details')
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{message}: {details}')
            return response
