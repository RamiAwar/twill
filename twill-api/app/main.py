import datetime

import aioredis
import tweepy
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.requests import Request
from sqlmodel import SQLModel, create_engine
from starsessions import SessionMiddleware

from app import model
from app.config import twitter_api_settings
from app.model.user import User
from app.service.authentication import get_current_active_user
from app.service.session import RedisBackend
from config import postgres_settings

app = FastAPI()


engine = create_engine(
    f"postgresql://twillapi:{postgres_settings.password}@localhost:5432/postgres",
    echo=True,
)

SQLModel.metadata.create_all(engine)

# https://github.com/alex-oleshkevich/starsessions/blob/cc738b48d01ba4764107764ab755014001e39ca2/examples/fastapi_app.py
backend = RedisBackend(
    "redis://localhost",
    redis_key_func=lambda x: "session:" + x,
    expire=60 * 60 * 24 * 7,
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


# @app.post("/login")
# async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         return "Login failed"

#     request.session["username"] = user.username
#     return "success"


oauth1_user_handler = tweepy.OAuth1UserHandler(
    twitter_api_settings.consumer_key,
    twitter_api_settings.consumer_secret,
    callback="http://localhost:8000/oauth",
)


@app.get("/twitter")
async def twitter(request: Request):
    url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)

    # Save request token for verification
    request.session["oauth_token"] = url.split("=")[1]

    return {"redirect": url}


@app.get("/oauth")
async def verifier_login(request: Request, oauth_token: str, oauth_verifier: str):
    if request.session.get("oauth_token") != oauth_token:
        request.session.clear()
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error authenticating with Twitter",
        )

    # Fetch access token and secret and save in session
    access_token, access_token_secret = oauth1_user_handler.get_access_token(
        oauth_verifier
    )

    request.session["access_token"] = access_token
    request.session["access_token_secret"] = access_token_secret

    # Fetch user data and login
    auth = tweepy.OAuth1UserHandler(
        consumer_key=twitter_api_settings.consumer_key,
        consumer_secret=twitter_api_settings.consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    api = tweepy.API(auth)
    user: tweepy.User = api.verify_credentials(include_email=True)
    if not user.email:
        request.session.clear()
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error authenticating with Twitter - Email privileges needed",
        )

    # Create or update user
    # user_db = User.get(user.email)

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


# x = User(
#     id=1254087536,
#     id_str="1254087536",
#     name="Rami Awar",
#     screen_name="iamramiawar",
#     location="The Hague, The Netherlands",
#     description="Senior Backend Engineer @AiProton\n\nAuthor at https://t.co/llor0S0aXw\n\n| Golang, Python, Backend, Reflections. \n\n| Views are mine.\n\n| 🏳️\u200d🌈",
#     url="https://t.co/7IqFm0AYSB",
#     entities={
#         "url": {
#             "urls": [
#                 {
#                     "url": "https://t.co/7IqFm0AYSB",
#                     "expanded_url": "https://github.com/RamiAwar",
#                     "display_url": "github.com/RamiAwar",
#                     "indices": [0, 23],
#                 }
#             ]
#         },
#         "description": {
#             "urls": [
#                 {
#                     "url": "https://t.co/llor0S0aXw",
#                     "expanded_url": "http://softgrade.org/#/portal",
#                     "display_url": "softgrade.org/#/portal",
#                     "indices": [45, 68],
#                 }
#             ]
#         },
#     },
#     protected=False,
#     followers_count=1527,
#     friends_count=1268,
#     listed_count=3,
#     created_at=datetime.datetime(2013, 3, 9, 11, 1, 37, tzinfo=datetime.timezone.utc),
#     favourites_count=10050,
#     utc_offset=None,
#     time_zone=None,
#     geo_enabled=False,
#     verified=False,
#     statuses_count=1122,
#     lang=None,
#     contributors_enabled=False,
#     is_translator=False,
#     is_translation_enabled=False,
#     profile_background_color="000000",
#     profile_background_image_url="http://abs.twimg.com/images/themes/theme1/bg.png",
#     profile_background_image_url_https="https://abs.twimg.com/images/themes/theme1/bg.png",
#     profile_background_tile=False,
#     profile_image_url="http://pbs.twimg.com/profile_images/1138862227602247680/tz6LShEh_normal.jpg",
#     profile_image_url_https="https://pbs.twimg.com/profile_images/1138862227602247680/tz6LShEh_normal.jpg",
#     profile_banner_url="https://pbs.twimg.com/profile_banners/1254087536/1657654691",
#     profile_link_color="E81C4F",
#     profile_sidebar_border_color="000000",
#     profile_sidebar_fill_color="000000",
#     profile_text_color="000000",
#     profile_use_background_image=False,
#     has_extended_profile=True,
#     default_profile=False,
#     default_profile_image=False,
#     following=False,
#     follow_request_sent=False,
#     notifications=False,
#     translator_type="none",
#     withheld_in_countries=[],
#     suspended=False,
#     needs_phone_verification=False,
#     email="rami.awar.ra@gmail.com",
# )
