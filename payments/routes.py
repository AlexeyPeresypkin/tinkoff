from fastapi import APIRouter

router = APIRouter(prefix='/payments', tags=['Платежи'])


@router.get('/')
def get_operations():
    return {'result': 'it works'}
