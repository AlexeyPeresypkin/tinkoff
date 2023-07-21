import json
from datetime import datetime, date, time
from enum import Enum
from hashlib import sha256

TERMINAL_PASSWORD = 'TinkoffBankTest'


# TERMINAL_PASSWORD = os.getenv('TERMINAL_PASSWORD')

def default(obj):
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    elif isinstance(obj, Enum):
        return obj.value
    return obj


def normalize_value(value):
    if isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, Enum):
        return value.value  # noqa
    elif isinstance(value, int):
        return str(value)
    return value


def get_token(data: dict):
    data = data.copy()
    # exclude_keys = ('receipt', 'data')
    data.update({"Password": TERMINAL_PASSWORD})
    token_fields = ('TerminalKey', 'Amount', 'OrderId', 'Amount', 'Password', 'Description')
    list_data = [(key, normalize_value(v)) for key, v in data.items() if key in token_fields]
    # list_data = [normalize_value(v) for key, v in data.items() if key not in exclude_keys and v]
    list_data = [x[1] for x in sorted(list_data, key=lambda x: x[0])]
    # list_data = [x[1] for x in list_data]
    print(f'sorted list => {list_data}')
    data_for_token = ''.join(list_data)
    print(f'data_for_token => {data_for_token}')
    token = sha256(data_for_token.encode('utf-8')).hexdigest()
    return token


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() if word not in ('url', 'data', 'ip') else word.upper() for word in string.split('_'))


def get_camel_case_data(data: dict) -> dict:
    # Конвертируем ключи в кэмелкейс для запроса
    for key in list(data):
        data[to_camel(key)] = data.pop(key)
    return data


def get_payload_init(data: dict) -> json:
    data = {k: v for k, v in data.items() if v}
    return json.dumps(data, default=default)
