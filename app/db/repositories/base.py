from typing import Callable, Type

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import DATABASE
from app.models.domain.rwmodel import DateTimeRWModel


class BaseRepository:
    __DATABASE__ = DATABASE
    __collection__ = ""

    def __init__(self, conn: AsyncIOMotorClient) -> None:
        self._conn = conn
        self.collection = self._conn.get_database(self.__DATABASE__).get_collection(self.__collection__)

    @property
    def connection(self) -> AsyncIOMotorClient:
        return self._conn

    def create(self, *, CREATE_MODEL: Type[DateTimeRWModel], RETURN_MODEL: Type[DateTimeRWModel]) -> Callable:
        async def _create(create: CREATE_MODEL) -> RETURN_MODEL:
            async with await self.connection.start_session() as s:
                async with s.start_transaction():
                    result = await self.collection.insert_one(create.dict())

            return RETURN_MODEL(id_=result.inserted_id, **create.dict())

        return _create
