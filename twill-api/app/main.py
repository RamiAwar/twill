import aioredis
import motor.motor_asyncio
import sentry_sdk
import tweepy
from beanie import init_beanie
from beanie.operators import Set
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from sqlmodel import Session, SQLModel, create_engine, select
from tweepy.asynchronous import AsyncClient

from app.config import (
    app_settings,
    logger,
    mongo_settings,
    redis_settings,
    session_backend,
    twitter_api_settings,
)
from app.model.tweet import Tweet
from app.model.user import User, UserPublicMetrics, UserSession
from app.router.twitter_authentication import router as twitter_auth_router
from app.service.deps import auth
from app.service.starsessions import SessionMiddleware

sentry_sdk.init(
    dsn="https://709b566d47ee4311ada4f6340088897a@o1359248.ingest.sentry.io/6646638",
    integrations=[
        StarletteIntegration(),
        FastApiIntegration(),
    ],
    release=app_settings.commit_hash,
    traces_sample_rate=1.0,
    environment=app_settings.environment,
)

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    backend=session_backend,
    autoload=True,
)

app.include_router(twitter_auth_router, prefix="/twitter", tags=["twitter"])


@app.on_event("startup")
async def startup():
    # Health check redis
    try:
        redis = aioredis.from_url(redis_settings.redis_url)
        async with redis.client() as conn:
            await conn.set("health", "1")
    except aioredis.ConnectionError:
        raise Exception("Redis is not running")

    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_settings.dsn)

    # Initialize beanie
    await init_beanie(client.twill, document_models=[User, Tweet])


@app.post("/logout")
async def logout(request: Request):
    request.session.clear()
    response = Response(status_code=status.HTTP_200_OK)
    response.delete_cookie("user_id")
    return response


@app.get("/")
async def main(request: Request):
    return request.session


@app.get("/twitter/stats", response_model=UserPublicMetrics)
async def get_user_profile(session: UserSession = Depends(auth)):
    tweepy_client = AsyncClient(
        consumer_key=twitter_api_settings.consumer_key,
        consumer_secret=twitter_api_settings.consumer_secret,
        access_token=session.access_token,
        access_token_secret=session.access_token_secret,
    )

    response = await tweepy_client.get_user(
        id=session.twitter_user_id, user_fields=["public_metrics"], user_auth=True
    )

    if response.errors:
        logger.error(
            f"error encountered fetching twitter user data: \n{response.errors}"
        )
        raise HTTPException(500, "Internal error fetching twitter data")

    user_metrics = response.data
    return UserPublicMetrics(**user_metrics["public_metrics"])


@app.get("/twitter/tweets")
async def get_user_tweets(session: UserSession = Depends(auth)):
    tweepy_client = AsyncClient(
        consumer_key=twitter_api_settings.consumer_key,
        consumer_secret=twitter_api_settings.consumer_secret,
        access_token=session.access_token,
        access_token_secret=session.access_token_secret,
    )

    response = await tweepy_client.get_users_tweets(
        session.twitter_user_id,
        tweet_fields=["organic_metrics", "context_annotations", "conversation_id"],
        expansions=["author_id"],
        user_auth=True,
    )

    for res in response.data:
        tweet = Tweet(**res)
        await tweet.save()

    return tweet
