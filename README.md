Первые три задачи находятся в файле [extra_tasks.py](extra_tasks.py)

Деплой проекта
============
1. Создать файл `.env` по примеру [env_example](env_example)
2. Запустить контейнеры командой `docker-compose up -d --build`

Приложение готово, документация проекта доступна по адресу http://localhost:8001/docs#/

Тестовые данные для создания платежа:

`{
    "terminal_key": "TinkoffBankTest",
    "amount": 140000,
    "order_id": "65612365566545",
    "language": "ru",
    "description": "description_test",
    "ip": "127.0.0.1",
    "customer_key": "87899546",
    "redirect_due_date": "2023-07-27T09:33:22.476Z",
    "notification_url": "www.notification.url",
    "success_url": "www.success.ru",
    "fail_url": "www.fail.ru",
    "pay_type": "O",
    "data": {
        "phone": "+71234567890",
        "email": "a@test.com"
    },
    "receipt": {
        "email": "a@test.ru",
        "phone": "+79031234567",
        "taxation": "osn",
        "items": [
            {
                "name": "Наименование товара 1",
                "price": 10000,
                "quantity": 1.00,
                "amount": 10000,
                "payment_method": "full_prepayment",
                "payment_object": "commodity",
                "tax": "vat10",
                "ean13": "0123456789",
                "agent": {
                    "agent_sign": "bank_paying_agent",
                    "operation_name": "operation_name",
                    "phones": ["+79255319607", "+79255319607"],
                    "receiver_phones": ["+79255319607", "+79255319607"],
                    "transfer_phones": ["+79255319607", "+79255319607"],
                    "operator_name": "operator_name",
                    "operator_address": "operator_address",
                    "operator_inn": "1234567891"
                },
                "supplier": {
                    "phones": ["+79255319603", "+79255319607"],
                    "name": "Ivan Pupkin",
                    "inn": "1234567891"
                }
            },
            {
                "name": "Наименование товара 2",
                "price": 20000,
                "quantity": 2.00,
                "amount": 40000,
                "payment_method": "prepayment",
                "payment_object": "service",
                "tax": "vat20"
            },
            {
                "name": "Наименование товара 3",
                "price": 30000,
                "quantity": 3.00,
                "amount": 90000,
                "tax": "vat10"
            }
        ],
        "receipt_payment": {
            "cash": 0,
            "electronic": 140000,
            "advance_payment": 0,
            "credit": 0,
            "provision": 0
        }
    }
}`

Данные для получения статуса платежа (**payment_id необходимо изменить на свой**):

`{
  "terminal_key": "TinkoffBankTest",
  "payment_id": 3032730208
}`

Данные для отмены платежа (**payment_id необходимо изменить на свой**)

`{
  "terminal_key": "TinkoffBankTest",
  "payment_id": 3029120892,
  "amount": 140000
}`

Данные для отмены платежа (расширенные) (**payment_id необходимо изменить на свой**)

`{
    "terminal_key": "TinkoffBankTest",
    "payment_id": 3032730208,
    "amount": 100,
    "receipt": {
        "email": "a@test.ru",
        "phone": "+79031234567",
        "taxation": "osn",
        "items": [
            {
                "name": "Наименование товара 1",
                "price": 100,
                "quantity": 1.00,
                "amount": 100,
                "payment_method": "full_prepayment",
                "payment_object": "commodity",
                "tax": "vat10",
                "ean13": "0123456789"
            }
        ]
    }
}`