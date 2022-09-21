import aioredis
import sentry_sdk
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.requests import Request
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from starsessions import InMemoryStore, SessionAutoloadMiddleware, SessionMiddleware
from tweepy.asynchronous import AsyncClient
from twill.config import logger, twitter_api_settings
from twill.database.mongo import initialize_beanie
from twill.model.twitter import Tweet, UserPublicMetrics

from app.config import app_settings, setup_logging
from app.model.user import UserSession
from app.router.beta import router as beta_router
from app.router.twitter_authentication import router as twitter_auth_router
from app.service.deps import auth

setup_logging()

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

store = InMemoryStore()
app.add_middleware(SessionAutoloadMiddleware)
app.add_middleware(
    SessionMiddleware,
    store=store,
    lifetime=60 * 60 * 24 * 7,  # 1 week
)

app.include_router(twitter_auth_router, prefix="/twitter", tags=["twitter"])
app.include_router(beta_router, prefix="/beta", tags=["beta"])


@app.on_event("startup")
async def startup():
    # Health check redis
    # try:
    #     redis = aioredis.from_url(redis_settings.redis_url)
    #     async with redis.client() as conn:
    #         await conn.set("health", "1")
    # except aioredis.ConnectionError:
    #     raise Exception("Redis is not running")

    # Initialize beanie
    await initialize_beanie()


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
