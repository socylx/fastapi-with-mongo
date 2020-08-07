from typing import Type, Callable

from fastapi import Depends

from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request

from app.db.repositories.base import BaseRepository


def _get_connection_from_pool(request: Request) -> AsyncIOMotorClient:
    return request.app.state.pool


def get_repository(repo_type: Type[BaseRepository]) -> Callable[[AsyncIOMotorClient], BaseRepository]:
    def _get_repo(conn: AsyncIOMotorClient = Depends(_get_connection_from_pool)) -> BaseRepository:
        return repo_type(conn)

    return _get_repo
