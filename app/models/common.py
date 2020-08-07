from typing import Optional, Any

from pydantic import BaseModel, Field


class IDModelMixin(BaseModel):
    id_: Optional[Any] = Field(None, alias="_id")
