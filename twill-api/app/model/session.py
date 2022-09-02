from pydantic import BaseModel
from starsessions import Session


class TwitterRequestToken(BaseModel):
    oauth_token: str
    oauth_token_secret: str


class LoginSession(BaseModel, Session):
    twitter_request_token: TwitterRequestToken
