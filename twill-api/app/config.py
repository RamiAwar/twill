from enum import Enum

from pydantic import BaseSettings, Field


class TwitterAPISettings(BaseSettings):
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str = Field(env="token_secret")


class JWTAlgorithm(str, Enum):
    HS256 = "HS256"
    RS256 = "RS256"
    ES256 = "ES256"


class AuthenticationSettings(BaseSettings):
    jwt_secret: str
    jwt_algorithm: JWTAlgorithm = JWTAlgorithm.HS256
    jwt_expiration_minutes: int = 30
    jwt_refresh_expiration_delta: int = 86400


twitter_api_settings = TwitterAPISettings()
authentication_settings = AuthenticationSettings()
