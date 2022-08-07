import datetime

import aioredis
import tweepy
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.requests import Request
from sqlmodel import Session, SQLModel, create_engine, select
from starsessions import SessionMiddleware

from app import model
from app.config import postgres_settings, session_backend, twitter_api_settings
from app.model.user import User, UserDB, UserOut
from app.service.authentication import get_current_active_user

app = FastAPI()


engine = create_engine(
    f"postgresql://twillapi:{postgres_settings.postgres_password}@localhost:5432/postgres",
    echo=True,
)

SQLModel.metadata.create_all(engine)

app.add_middleware(
    SessionMiddleware,
    backend=session_backend,
    secret_key="12aesj09290ale",
    autoload=True,
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


def get_twitter_oauth_handler():
    return tweepy.OAuth1UserHandler(
        twitter_api_settings.consumer_key,
        twitter_api_settings.consumer_secret,
        callback="http://localhost:5173/auth/oauth",
    )


@app.get("/twitter")
async def twitter(request: Request):
    oauth1_user_handler = get_twitter_oauth_handler()
    url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)

    # Save request token for verification
    oauth_token = url.split("=")[1]
    request.session["twitter_request_token"] = {
        "oauth_token": oauth_token,
        "oauth_token_secret": oauth1_user_handler.request_token["oauth_token_secret"],
    }
    return {"redirect_url": url}


@app.get("/oauth")
async def verifier_login(
    request: Request, oauth_token: str, oauth_verifier: str, response: Response
):
    if (
        request.session.get("twitter_request_token", {}).get("oauth_token")
        != oauth_token
    ):
        request.session.clear()
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error authenticating with Twitter",
        )

    # Fetch access token and secret and save in session
    oauth1_user_handler = get_twitter_oauth_handler()
    oauth1_user_handler.request_token = request.session.get("twitter_request_token")
    access_token, access_token_secret = oauth1_user_handler.get_access_token(
        oauth_verifier
    )

    request.session["access_token"] = access_token
    request.session["access_token_secret"] = access_token_secret

    # TODO: Handle error here
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

    # Create new user object
    user_db = UserDB(
        name=user.name,
        email=user.email,
        twitter_handle=user.screen_name,
        twitter_user_id=user.id_str,
        twitter_followers_count=user.followers_count,
        twitter_verified=user.verified,
        twitter_suspended=user.suspended,
        profile_image_url=user.profile_image_url,
    )

    with Session(engine) as session:
        res = session.exec(select(UserDB).where(UserDB.email == user.email)).first()

        if res:
            # User already exists, only update fields
            user_db = res
            user_db.name = user.name
            user_db.email = user.email
            user_db.twitter_handle = user.screen_name
            user_db.twitter_user_id = user.id_str
            user_db.twitter_followers_count = user.followers_count
            user_db.twitter_verified = user.verified
            user_db.twitter_suspended = user.suspended
            user_db.profile_image_url = user.profile_image_url

        session.add(user_db)
        session.commit()
        session.refresh(user_db)  # Fetch new id if any

    response.set_cookie("user_id", str(user_db.id))
    return UserOut(**user_db.dict())


@app.post("/logout")
async def logout(request: Request):
    request.session.clear()
    response = Response(status_code=status.HTTP_200_OK)
    response.delete_cookie("user_id")
    return response


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
