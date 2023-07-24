import json
from datetime import datetime, date, time
from enum import Enum
from hashlib import sha256

from core.config import settings


def default(obj):
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat(timespec='seconds')
    elif isinstance(obj, Enum):
        return obj.value
    return obj


def get_payload(data: dict) -> json:
    camel_case_data = get_camel_case_data(data)
    token = get_token(camel_case_data)
    camel_case_data.update({'Token': token})
    data = {k: v for k, v in camel_case_data.items() if v}
    return json.dumps(data, default=default)


def normalize_value(value):
    if isinstance(value, datetime):
        return value.isoformat(timespec='seconds')
    elif isinstance(value, Enum):
        return value.value  # noqa
    elif isinstance(value, int):
        return str(value)
    return value


def get_token(data: dict) -> str:
    data = data.copy()
    exclude_keys = ('Receipt', 'DATA')
    data.update({"Password": settings.terminal_password})
    list_data = [(key, normalize_value(v)) for key, v in data.items() if key not in exclude_keys and v]
    list_data = [x[1] for x in sorted(list_data, key=lambda x: x[0])]
    data_for_token = ''.join(list_data)
    token = sha256(data_for_token.encode('utf-8')).hexdigest()
    return token


def to_camel(string: str) -> str:
    camel_cases = {'receipt_payment': 'Payments', 'agent': 'AgentData', 'supplier': 'SupplierInfo'}
    return camel_cases.get(string) or ''.join(word.capitalize() if word not in ('url', 'data', 'ip')
                                              else word.upper() for word in string.split('_'))


def get_camel_case_data(data: dict) -> dict:
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
