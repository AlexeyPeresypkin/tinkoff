import os
from typing import AsyncGenerator

# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
# from sqlalchemy.orm import sessionmaker


db_host = os.environ.get('POSTGRES_HOST')
db_port = os.environ.get('POSTGRES_PORT')
db_name = os.environ.get('POSTGRES_DB')
db_user = os.environ.get('POSTGRES_USER')
db_pwd = os.environ.get('POSTGRES_PASSWORD')
# SQLALCHEMY_DATABASE_URL = "postgresql://sv:123@192.168.100.49/profticket"
# ASYNC_SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://sv:123@192.168.100.49/profticket"

# SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
SQLALCHEMY_DATABASE_URL = f'postgresql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'

# SQLALCHEMY_DATABASE_URL = "postgresql://sv:123@192.168.100.49/test_tabakov"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# dbsession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# async def get_db():
#     db = dbsession()
#     try:
#         yield db
#     finally:
#         db.close()


async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


