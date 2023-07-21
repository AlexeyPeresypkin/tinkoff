import uvicorn
# from blanks.routers import router as blanks_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from payments.routes import router as payment_routes

tags_metadata = [{"name": "Платежи", "description": "Работа с платежами"}]

app = FastAPI(title="Система платежей Tinkoff",
              description="Сервер REST API Tinkoff", version="1.0",
              openapi_tags=tags_metadata)
app.include_router(payment_routes)
# app.include_router(lists.router)
# app.include_router(seatmap.router)
# app.include_router(settings.router)
# app.include_router(other.router)
# app.include_router(options.router)
# app.include_router(tools.router)
# app.include_router(atl.router)
# app.include_router(repertoire.router)
# app.include_router(pos_sber.router)
# app.include_router(datamax_printer.router)
# app.include_router(users_router)
# app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=['auth/users'])
# app.include_router(fastapi_users.get_users_router(UserReadAfterUpdate, UserUpdate), prefix='/users',
#                    tags=['auth/users'])
# app.include_router(blanks_router)
# app.include_router(operations_tickets_router)


# @app.on_event("startup")
# async def startup_event():
#     conn = db.get_db()
#     print('Загрузка зрителей')


# @app.exception_handler(SQLAlchemyError)
# async def sql_alchemy_error(request: Request, exc):
#     print('===================')
#     print(exc)
#     print(f'PARAMS: {exc.params.values()}')
#     print('===================')
#     error = exc.orig.args[0].split('\n')[0]
#     return JSONResponse(status_code=500, content={'detail': f'{error}'})


app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5555, log_level='info')
