from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgresql import get_async_session
from schemas.payments import PaymentRead, PaymentCreate, bad_request_with_404, CancelPaymentCreate, PaymentStatusRead, \
    PaymentStatusCreate, bad_request_common
from services.get_service import get_payment_service
from services.payment import PaymentService

router = APIRouter(tags=['Платежи'])


@router.post('/init',
             status_code=status.HTTP_201_CREATED,
             summary='Создание платежа',
             response_model=PaymentRead,
             responses=bad_request_common,
             description='Создание платежа')
async def post_init(payment_create: PaymentCreate,
                    payment_service: PaymentService = Depends(get_payment_service)):
    payment = await payment_service.create_payment(payment_create)
    return PaymentRead.model_validate(payment)
    # print(123)
    # url = 'https://securepay.tinkoff.ru/v2/Init'
    # payload = utils.get_payload(payment_create.model_dump())
    # response = await utils.get_response_or_400(url, payload)
    # data = payment_create.model_dump()
    # receipt = data.pop('receipt', None)
    # payment = models.Payments(
    #     **data,
    #     payment_id=int(response.get('PaymentId')),
    #     payment_url=response.get('PaymentURL'),
    #     payment_status=response.get('Status'))
    # db.add(payment)
    # await db.flush()
    # await utils.create_receipt(db, payment, receipt)
    # await db.commit()
    # return schemas.PaymentRead.model_validate(payment)


@router.get('/payment_url',
            response_model=PaymentRead,
            responses=bad_request_with_404,
            description='Получение ссылки платежа')
async def get_payment_url(payment_id: int, db: AsyncSession = Depends(get_async_session)):
    print(123)
    # payment = await utils.get_payment_or_404(db, payment_id)
    # return schemas.PaymentRead.model_validate(payment)


@router.post('/payment_status',
             status_code=status.HTTP_201_CREATED,
             response_model=PaymentStatusRead,
             responses=bad_request_with_404,
             description='Получение статуса платежа')
async def post_payment_status(payment_status: PaymentStatusCreate,
                              db: AsyncSession = Depends(get_async_session)):
    print(123)
    # url = 'https://securepay.tinkoff.ru/v2/GetState'
    # payment = await utils.get_payment_or_404(db, payment_status.payment_id)
    # if payment.payment_status in ('CANCELED', 'REVERSED', 'REFUNDED'):
    #     return schemas.PaymentStatusRead(payment_status=payment.payment_status)
    # payload = utils.get_payload(payment_status.model_dump())
    # response = await utils.get_response_or_400(url, payload)
    # await utils.update_payment_status_or_none(db, payment, response.get('Status'))
    # return schemas.PaymentStatusRead(payment_status=payment.payment_status)


@router.post('/payment_cancel',
             status_code=status.HTTP_201_CREATED,
             response_model=PaymentStatusRead,
             responses=bad_request_with_404,
             description='Отмена платежа')
async def post_payment_cancel(cancel_payment: CancelPaymentCreate,
                              db: AsyncSession = Depends(get_async_session)):
    print(123)
    # url = 'https://securepay.tinkoff.ru/v2/Cancel'
    # payment = await utils.get_payment_or_404(db, cancel_payment.payment_id)
    # payload = utils.get_payload(cancel_payment.model_dump())
    # response = await utils.get_response_or_400(url, payload)
    # data = cancel_payment.model_dump()
    # data.pop('payment_id')
    # receipt = data.pop('receipt', None)
    # cancelled_payment = models.CancelledPayments(
    #     **data,
    #     payment_id=payment.id,
    #     payment_status=response.get('Status'),
    #     original_amount=response.get('OriginalAmount'),
    #     new_amount=response.get('NewAmount'))
    # db.add(cancelled_payment)
    # await db.flush()
    # await utils.create_receipt(db, cancelled_payment, receipt)
    # await db.commit()
    # return schemas.PaymentStatusRead.model_validate(cancelled_payment)
