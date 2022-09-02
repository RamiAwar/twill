from datetime import datetime
from typing import Optional

from app.model.session import TwitterRequestToken
from beanie import Document, Indexed
from pydantic import BaseModel, Field
from starsessions import Session


class TwitterCredentials(BaseModel):
    access_token: str
    access_token_secret: str
    twitter_user_id: str
    twitter_request_token: Optional[TwitterRequestToken]


class User(Document, TwitterCredentials):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    name: str
    email: str = Field()
    twitter_handle: str
    twitter_user_id: str
    twitter_followers_count: int
    twitter_verified: bool
    twitter_suspended: bool
    profile_image_url: str


class UserOut(BaseModel):
    name: str
    profile_image_url: str
    twitter_handle: str
    twitter_followers_count: int


class UserOauthResponse(BaseModel):
    user: UserOut


class UserSession(TwitterCredentials, Session):
    email: str
    user_id: str


class UserPublicMetrics(BaseModel):
    followers_count: Optional[int]
    following_count: Optional[int]
    tweet_count: Optional[int]
    listed_count: Optional[int] = Field(
        description="Number of lists the user is a member of"
    )
