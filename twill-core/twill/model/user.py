from datetime import datetime
from typing import Any, Optional

from beanie import Document, Indexed
from pydantic import BaseModel, Field


class TwitterCredentials(BaseModel):
    access_token: str
    access_token_secret: str
    twitter_user_id: str
    twitter_request_token: Optional[Any]


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


class BetaAccess(Document):
    email: Indexed(str)


class BetaWaitlist(Document):
    email: Indexed(str)


class BetaSignupRequest(BaseModel):
    email: str
