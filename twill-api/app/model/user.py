from beanie import PydanticObjectId
from pydantic import BaseModel
from starsessions import Session
from twill.model.user import TwitterCredentials


class UserOut(BaseModel):
    id: PydanticObjectId
    name: str
    profile_image_url: str
    twitter_handle: str
    twitter_followers_count: int


class UserOauthResponse(BaseModel):
    user: UserOut


class UserSession(TwitterCredentials, Session):
    email: str
    user_id: str
