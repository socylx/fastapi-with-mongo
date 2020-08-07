from fastapi import FastAPI
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import DATABASE_URL, MIN_CONNECTIONS_COUNT, MAX_CONNECTIONS_COUNT


async def connect_to_db(app: FastAPI) -> None:
    logger.info("Connection to {0}", repr(DATABASE_URL))

    app.state.pool = AsyncIOMotorClient(
        str(DATABASE_URL),
        maxPoolSize=MAX_CONNECTIONS_COUNT,
        minPoolSize=MIN_CONNECTIONS_COUNT
    )

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.pool.close()

    logger.info("Connection closed")
