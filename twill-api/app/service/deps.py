from typing import Optional

from app.model.security import UserSession, unauthorized_error
from fastapi import Request
from pydantic import ValidationError


async def auth(request: Request) -> Optional[UserSession]:
    session = request.session
    if not session:
        raise unauthorized_error

    try:
        session = UserSession(**session)
    except ValidationError:
        # Something wrong, sign user out and raise unauthorized error
        session.clear()

        raise unauthorized_error
    return session
