from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from db import get_async_session
from payments import schemas, utils, models
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/payments', tags=['Платежи'])


@router.post('/init',
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.PaymentRead,
             description='Создание платежа')
async def post_init(payment_create: schemas.PaymentCreate, db: AsyncSession = Depends(get_async_session)):
    url = 'https://securepay.tinkoff.ru/v2/Init'
    payload = utils.get_payload(payment_create.model_dump())
    response = await utils.get_response_or_400(url, payload)
    data = payment_create.model_dump()
    receipt = data.pop('receipt', None)
    payment = models.Payments(**data, payment_id=int(response.get('PaymentId')), payment_url=response.get('PaymentURL'))
    db.add(payment)
    await db.flush()
    await utils.create_receipt(db, payment, receipt)
    await db.commit()
    return schemas.PaymentRead.model_validate(payment)


@router.get('/payment_url', response_model=schemas.PaymentRead, description='Получение ссылки платежа')
async def get_payment_url(payment_id: int, db: AsyncSession = Depends(get_async_session)):
    stmt = select(models.Payments).where(models.Payments.payment_id == payment_id)
    payment = await db.execute(stmt)
    payment = payment.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return schemas.PaymentRead.model_validate(payment)


@router.post('/payment_status',
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.PaymentStatusRead,
             description='Получение статуса платежа')
async def post_payment_status(payment_status: schemas.PaymentStatus, db: AsyncSession = Depends(get_async_session)):
    url = 'https://securepay.tinkoff.ru/v2/GetState'
    await utils.get_payment_or_404(db, payment_status.payment_id)
    payload = utils.get_payload(payment_status.model_dump())
    response = await utils.get_response_or_400(url, payload)
    return schemas.PaymentStatusRead(payment_status=response.get('Status'))


@router.post('/payment_cancel',
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.CancelPaymentRead,
             description='Отмена платежа')
async def post_payment_cancel(cancel_payment: schemas.CancelPayment, db: AsyncSession = Depends(get_async_session)):
    url = 'https://securepay.tinkoff.ru/v2/Cancel'
    payment = await utils.get_payment_or_404(db, cancel_payment.payment_id)
    payload = utils.get_payload(cancel_payment.model_dump())
    response = await utils.get_response_or_400(url, payload)
    data = cancel_payment.model_dump()
    data.pop('payment_id')
    receipt = data.pop('receipt', None)
    cancelled_payment = models.CancelledPayments(
        **data,
        payment_id=payment.id,
        status=response.get('Status'),
        original_amount=response.get('OriginalAmount'),
        new_amount=response.get('NewAmount'))
    db.add(cancelled_payment)
    await db.flush()
    await utils.create_receipt(db, cancelled_payment, receipt)
    await db.commit()
    return schemas.CancelPaymentRead.model_validate(cancelled_payment)
