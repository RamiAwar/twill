from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
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
    id: int
    name: str
    profile_image_url: str
    twitter_handle: str
    twitter_followers_count: int


class UserOauthResponse(BaseModel):
    new_user: bool
    user: UserOut


class UserSession(BaseModel):
    email: str
    user_id: int
    access_token: str
    access_token_secret: str
    twitter_user_id: str


class UserPublicMetrics(BaseModel):
    followers_count: Optional[int]
    following_count: Optional[int]
    tweet_count: Optional[int]
    listed_count: Optional[int] = Field(
        description="Number of lists the user is a member of"
    )
