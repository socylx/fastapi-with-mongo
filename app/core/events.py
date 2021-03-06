from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.db.events import connect_to_db, close_db_connection


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_up() -> None:
        await connect_to_db(app)

    return start_up


def create_stop_app_handler(app: FastAPI) -> Callable:
    @logger.catch
    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app
