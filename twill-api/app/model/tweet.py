from typing import Optional

from beanie import Document
from pydantic import BaseModel


class OrganicMetrics(BaseModel):
    reply_count: int
    retweet_count: int
    url_link_clicks: Optional[int]
    like_count: int
    impression_count: int
    user_profile_clicks: int


class Tweet(Document):
    id: int
    author_id: str
    organic_metrics: Optional[OrganicMetrics]
    conversation_id: str
    text: str
