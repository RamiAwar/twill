from pydantic import BaseModel


class TwitterRequestToken(BaseModel):
    oauth_token: str
    oauth_token_secret: str


class LoginSession(BaseModel):
    twitter_request_token: TwitterRequestToken
