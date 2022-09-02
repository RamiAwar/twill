from typing import Optional

from app.config import logger

# TODO: Refactor errors into error
from app.model.security import unauthorized_error
from app.model.session import LoginSession
from app.model.user import UserSession
from fastapi import Depends, Request
from pydantic import ValidationError

from starsessions import Session


async def session(request: Request) -> Session:
    session = request.session
    if not session:
        raise unauthorized_error
    return session


async def login(session=Depends(session)) -> Optional[LoginSession]:
    """This dep is used throughout the login flow"""
    try:
        session = LoginSession(**session)
    except ValidationError as e:
        # Session missing necessary details, sign user out and raise unauthorized error
        logger.error(f"error creating LoginSession from session object: {e}")
        session.clear()

        raise unauthorized_error
    return session


async def auth(session=Depends(session)) -> Optional[UserSession]:
    """This dep is used for all authenticated routes after login"""
    try:
        session = UserSession(**session)
    except ValidationError as e:
        # Session missing necessary details, sign user out and raise unauthorized error
        logger.error(f"error creating UserSession from session object: {e}")
        session.clear()

        raise unauthorized_error
    return session
