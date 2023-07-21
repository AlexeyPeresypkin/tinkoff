import aiohttp
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from payments import schemas, utils, models

router = APIRouter(prefix='/payments', tags=['Платежи'])

headers = {'content-type': 'application/json'}


@router.get('/')
def get_operations():
    return {'result': 'it works'}


# {"Success":false,"ErrorCode":"9999","Message":"Неверные параметры.","Details":"Поле TerminalKey не должно быть пустым."}
@router.post('/init', status_code=201, description='Создание платежа') #, response_model=schemas.PaymentRead
async def post_init(payment_create: schemas.PaymentCreate, db: AsyncSession = Depends(get_async_session)):
    url = 'https://securepay.tinkoff.ru/v2/Init'
    camel_case_data = utils.get_camel_case_data(payment_create.model_dump())
    token = utils.get_token(camel_case_data)
    camel_case_data.update({'Token': token})
    # payload = json.dumps(payment_create.model_dump(), default=default)
    payload = utils.get_payload_init(camel_case_data)
    print(f'payload ==============> {payload}')
    print(f'token ==============> {token}')
    # print(payment_create.model_dump())
    # print(type(payment_create.model_dump()))
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as resp:
            print(resp.status)
            print(await resp.json())

    payment = models.Payments(**payment_create.model_dump())
    # payment.pay_type = 'SINGLE_STAGE'
    db.add(payment)
    await db.commit()
    return schemas.PaymentRead.model_validate(payment)
