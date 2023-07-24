from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgresql import get_async_session
from services.payment import PaymentService


def get_payment_service(pg_db: AsyncSession = Depends(get_async_session)):
    return PaymentService(pg_db)
