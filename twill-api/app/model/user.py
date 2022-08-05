from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserDB(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    twitter_handle: str
    twitter_user_id: str
    twitter_followers_count: int
    twitter_verified: bool
    twitter_suspended: bool
    profile_image_url: str
