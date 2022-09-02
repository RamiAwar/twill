from typing import Tuple

import tweepy
from app.config import twitter_api_settings
from app.model.session import LoginSession
from app.model.user import User, UserOut, UserSession
from beanie.operators import Set
from fastapi import HTTPException, status


def get_twitter_oauth_handler():
    return tweepy.OAuth1UserHandler(
        twitter_api_settings.consumer_key,
        twitter_api_settings.consumer_secret,
        callback=twitter_api_settings.callback_url,
    )


def get_twitter_oauth_handler_user(session: UserSession):
    return tweepy.OAuth1UserHandler(
        twitter_api_settings.consumer_key,
        twitter_api_settings.consumer_secret,
        access_token=session.access_token,
        access_token_secret=session.access_token_secret,
    )


async def get_twitter_access_token(
    session: LoginSession, oauth_verifier: str
) -> Tuple[str, str]:
    # Fetch access token and secret and save in session
    oauth1_user_handler = get_twitter_oauth_handler()
    oauth1_user_handler.request_token = session.twitter_request_token.dict()
    access_token, access_token_secret = oauth1_user_handler.get_access_token(
        oauth_verifier
    )

    return access_token, access_token_secret


async def login_user_with_twitter(
    session: UserSession, access_token: str, access_token_secret: str
) -> User:
    # TODO: Handle error here
    # Fetch user data and login
    auth = tweepy.OAuth1UserHandler(
        consumer_key=twitter_api_settings.consumer_key,
        consumer_secret=twitter_api_settings.consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    api = tweepy.API(auth)
    tweepy_user: tweepy.User = api.verify_credentials(include_email=True)

    # TODO: Handle users with no email - Get email form
    if not tweepy_user.email:
        session.clear()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error authenticating with Twitter - Email privileges needed",
        )

    # Create new user object
    user = User(
        name=tweepy_user.name,
        email=tweepy_user.email,
        twitter_handle=tweepy_user.screen_name,
        twitter_user_id=tweepy_user.id_str,
        twitter_followers_count=tweepy_user.followers_count,
        twitter_verified=tweepy_user.verified,
        twitter_suspended=tweepy_user.suspended,
        profile_image_url=tweepy_user.profile_image_url,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    # Check if user exists using twitter user ID
    user_dict = user.dict(exclude={"id", "created_at"})
    db_user = await User.find_one(User.twitter_user_id == user.twitter_user_id)

    if db_user:
        # Update user
        await db_user.update(Set(user_dict))
        user = db_user
    else:
        # Create user
        user = await user.insert()

    return user
