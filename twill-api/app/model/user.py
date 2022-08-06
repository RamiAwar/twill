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
