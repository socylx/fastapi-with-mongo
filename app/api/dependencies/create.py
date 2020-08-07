from typing import Type, Callable

from fastapi import Body

from app.models.domain.rwmodel import DateTimeRWModel


def get_create(CREATE_MODEL: Type[DateTimeRWModel], alias: str, embed=True) -> Callable:
    def _get_create(create: CREATE_MODEL = Body(..., embed=embed, alias=alias)) -> DateTimeRWModel:
        create.set_datetime()
        return create

    return _get_create
