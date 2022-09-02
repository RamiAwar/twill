import tweepy
from app.config import twitter_api_settings
from app.model.session import LoginSession
from app.model.user import UserOut, UserSession
from app.service.authentication import get_twitter_access_token, login_user_with_twitter
from app.service.deps import login
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse

router = APIRouter()


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


@router.get("/login")
async def twitter(request: Request):
    """Returns twitter redirect url for authentication"""
    oauth1_user_handler = get_twitter_oauth_handler()
    url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)

    # Save request token to session for verification
    oauth_token = url.split("=")[1]
    request.session["twitter_request_token"] = {
        "oauth_token": oauth_token,
        "oauth_token_secret": oauth1_user_handler.request_token["oauth_token_secret"],
    }
    return {"redirect_url": url}


@router.get("/auth", response_model=UserOut)
async def verifier_login(
    request: Request,
    oauth_token: str,
    oauth_verifier: str,
    response: Response,
    session: LoginSession = Depends(login),
):
    # Validate that oauth token is the same as the one in the session
    if session.twitter_request_token.oauth_token != oauth_token:
        request.session.clear()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error authenticating with Twitter",
        )

    access_token, access_token_secret = await get_twitter_access_token(
        session, oauth_verifier
    )

    # Fetch user data and login
    user = await login_user_with_twitter(session, access_token, access_token_secret)

    # Save user details in session
    request.session["access_token"] = access_token
    request.session["access_token_secret"] = access_token_secret
    request.session["email"] = user.email
    request.session["user_id"] = str(user.id)
    request.session["twitter_user_id"] = user.twitter_user_id

    return UserOut(**user.dict())


@router.get("/dev/login")
async def twitter_dev(request: Request):
    oauth1_user_handler = tweepy.OAuth1UserHandler(
        twitter_api_settings.consumer_key,
        twitter_api_settings.consumer_secret,
        callback="http://localhost:8000/twitter/auth",
    )
    url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)

    # Save request token for verification
    oauth_token = url.split("=")[1]
    request.session["twitter_request_token"] = {
        "oauth_token": oauth_token,
        "oauth_token_secret": oauth1_user_handler.request_token["oauth_token_secret"],
    }
    return RedirectResponse(url=url)
