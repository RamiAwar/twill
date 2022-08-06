from typing import Optional

from app.config import session_backend
from app.model.security import UserSession, unauthorized_error
from fastapi import Depends, Request
from pydantic import ValidationError


async def session(request: Request):
    session = request.session
    if not session:
        raise unauthorized_error

    exists = await session_backend.exists(session)
    if not exists:
        request.session.clear()
        raise unauthorized_error

    return session


async def auth(session=Depends(session)) -> Optional[UserSession]:
    try:
        session = UserSession(**session)
    except ValidationError:
        # Something wrong, sign user out and raise unauthorized error
        session.clear()

        raise unauthorized_error
    return session
