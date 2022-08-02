import datetime
from datetime import timedelta

import aioredis
from fastapi import Depends, FastAPI
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from starsessions import SessionMiddleware

from app.model.user import User
from app.service.authentication import (
    authenticate_user,
    fake_users_db,
    get_current_active_user,
    get_current_user,
)
from app.service.session import RedisBackend

app = FastAPI()


# https://github.com/alex-oleshkevich/starsessions/blob/cc738b48d01ba4764107764ab755014001e39ca2/examples/fastapi_app.py
backend = RedisBackend(
    "redis://localhost", redis_key_func=lambda x: "session:" + x, expire=10
)
app.add_middleware(
    SessionMiddleware, backend=backend, secret_key="12aesj09290ale", autoload=True
)


@app.on_event("startup")
async def startup():
    # Health check redis
    try:
        redis = aioredis.from_url("redis://localhost")
        async with redis.client() as conn:
            await conn.set("health", "1")
    except aioredis.ConnectionError:
        raise Exception("Redis is not running")


@app.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        return "Login failed"

    request.session["username"] = user.username
    return "success"


@app.get("/")
async def main(request: Request):
    return request.session


@app.get("/profile")
async def get_user_profile(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/set")
async def set_time(request: Request):
    request.session["date"] = datetime.datetime.now().isoformat()
    return "success"
