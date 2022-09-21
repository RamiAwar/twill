from enum import Enum

from pydantic import BaseModel, Field


class BannerType(str, Enum):
    success = "success"
    error = "error"
    warning = "warning"
    info = "info"


class BannerResponse(BaseModel):
    message: str
    type: BannerType = Field(default=BannerType.info)
