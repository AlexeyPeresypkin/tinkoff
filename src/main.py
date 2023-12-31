from fastapi import FastAPI

from api.v1.payments import router as payment_routes

tags_metadata = [{"name": "Платежи", "description": "Работа с платежами"}]

app = FastAPI(
    title="Система платежей Tinkoff",
    description="Сервер REST API Tinkoff",
    version="1.0",
    openapi_tags=tags_metadata,
)
app.include_router(payment_routes, prefix="/api/v1/payments")
