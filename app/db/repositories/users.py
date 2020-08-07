from typing import Type, Callable

from app.core.config import USERS_COLLECTION_NAME
from app.db.errors import EntityDoesNotExist
from app.db.repositories.base import BaseRepository

from app.models.schemas.users import UserInDB, UserInCreate
from app.resources import format_strings


class UsersRepository(BaseRepository):
    __collection__ = USERS_COLLECTION_NAME

    async def get_user_by_username(self, *, username: str) -> UserInDB:
        user_row = await self.collection.find_one({"username": username})

        if user_row:
            return UserInDB(**user_row)

        raise EntityDoesNotExist(format_strings.USER_DOES_NOT_EXIST_WITH_USERNAME.format(username))

    async def get_user_by_email(self, *, email: str) -> UserInDB:
        user_row = await self.collection.find_one({"email": email})

        if user_row:
            return UserInDB(**user_row)

        raise EntityDoesNotExist(format_strings.USER_DOES_NOT_EXIST_WITH_EMAIL.format(email))

    def create(self, *, CREATE_MODEL: Type[UserInCreate], RETURN_MODEL: Type[UserInDB]) -> Callable:
        async def _create(create: CREATE_MODEL) -> RETURN_MODEL:
            create.change_password()
            async with await self.connection.start_session() as s:
                async with s.start_transaction():
                    result = await self.collection.insert_one(create.dict())

            return RETURN_MODEL(id_=result.inserted_id, **create.dict())

        return _create
