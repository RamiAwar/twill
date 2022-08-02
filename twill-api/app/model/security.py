from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel


class UserSession(BaseModel):
    username: str


unauthorized_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not Authenticated",
)
