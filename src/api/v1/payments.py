from fastapi import APIRouter, Depends, status

from schemas.payments import (
    PaymentRead,
    PaymentCreate,
    bad_request_with_404,
    CancelPaymentCreate,
    PaymentStatusRead,
    PaymentStatusCreate,
    bad_request_common,
)
from services.get_service import get_payment_service
from services.payment_service import PaymentService

router = APIRouter(tags=["Платежи"])


@router.post(
    "/init",
    status_code=status.HTTP_201_CREATED,
    response_model=PaymentRead,
    responses=bad_request_common,
    summary="Создание платежа",
    description="Создание платежа",
)
async def post_init(
    payment_create_schema: PaymentCreate,
    payment_service: PaymentService = Depends(get_payment_service),
):
    payment = await payment_service.create_payment(payment_create_schema)
    return PaymentRead.model_validate(payment)


@router.get(
    "/payment_url",
    response_model=PaymentRead,
    responses=bad_request_with_404,
    summary="Получение ссылки платежа",
    description="Получение ссылки платежа",
)
async def get_payment_url(
    payment_id: int, payment_service: PaymentService = Depends(get_payment_service)
):
    payment = await payment_service.get_payment_or_404(payment_id)
    return PaymentRead.model_validate(payment)


@router.post(
    "/payment_status",
    status_code=status.HTTP_201_CREATED,
    response_model=PaymentStatusRead,
    responses=bad_request_with_404,
    summary="Получение статуса платежа",
    description="Получение статуса платежа",
)
async def post_payment_status(
    payment_status_schema: PaymentStatusCreate,
    payment_service: PaymentService = Depends(get_payment_service),
):
    payment = await payment_service.update_status_if_need(payment_status_schema)
    return PaymentStatusRead.model_validate(payment)


@router.post(
    "/payment_cancel",
    status_code=status.HTTP_201_CREATED,
    response_model=PaymentStatusRead,
    responses=bad_request_with_404,
    summary="Отмена платежа/Частичный возврат",
    description="Отмена платежа/Частичный возврат",
)
async def post_payment_cancel(
    cancel_payment_schema: CancelPaymentCreate,
    payment_service: PaymentService = Depends(get_payment_service),
):
    cancelled_payment = await payment_service.cancel_payment(cancel_payment_schema)
    return PaymentStatusRead.model_validate(cancelled_payment)
