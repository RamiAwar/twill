from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import BaseModel, Field
from pymongo import IndexModel


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
    created_at: datetime
    in_reply_to_user_id: Optional[str]


class UserPublicMetrics(BaseModel):
    followers_count: Optional[int]
    following_count: Optional[int]
    tweet_count: Optional[int]
    listed_count: Optional[int] = Field(description="Number of lists the user is a member of")


class FollowCount(Document):
    user_id: str
    date: datetime
    followers_count: int

    class Settings:
        indexes = [
            # Unique index on date and user_id
            IndexModel(
                [("user_id", 1), ("date", 1)],
                unique=True,
                name="user_id_date_unique",
            )
        ]


class DailyStats(Document, OrganicMetrics):
    user_id: str
    date: datetime

    class Settings:
        indexes = [
            # Unique index on date and user_id
            IndexModel(
                [("user_id", 1), ("date", 1)],
                unique=True,
                name="user_id_date_unique",
            ),
            IndexModel(
                [("user_id", 1)],
                name="user_id",
            ),
            IndexModel(
                [("date", -1)],
                name="date",
            ),
        ]


class HourlyStats(Document, OrganicMetrics):
    user_id: str
    date: datetime

    class Settings:
        indexes = [
            # Unique index on date and user_id
            IndexModel(
                [("user_id", 1), ("date", 1)],
                unique=True,
                name="user_id_date_unique",
            ),
            IndexModel(
                [("user_id", 1)],
                name="user_id",
            ),
            IndexModel(
                [("date", -1)],
                name="date",
            ),
        ]


class EngagementAggregation(BaseModel):
    date: str
    reply_count: int
    retweet_count: int
    like_count: int
    impression_count: int
    url_link_clicks: int
    user_profile_clicks: int

    @classmethod
    def get_daily_engagement_aggregation_pipeline(cls, date: datetime):
        return [
            {"$match": {"created_at": {"$gte": date}}},
            {
                "$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}},
                    "reply_count": {"$sum": "$organic_metrics.reply_count"},
                    "retweet_count": {"$sum": "$organic_metrics.retweet_count"},
                    "impression_count": {"$sum": "$organic_metrics.impression_count"},
                    "like_count": {"$sum": "$organic_metrics.like_count"},
                    "url_link_clicks": {"$sum": "$organic_metrics.url_link_clicks"},
                    "user_profile_clicks": {"$sum": "$organic_metrics.user_profile_clicks"},
                }
            },
            {"$addFields": {"date": "$_id"}},
            {"$sort": {"_id": 1}},
        ]

    @classmethod
    def get_hourly_engagement_aggregation_pipeline(cls, date: datetime):
        return [
            {"$match": {"created_at": {"$gte": date}}},
            {
                "$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m-%d %H", "date": "$created_at"}},
                    "reply_count": {"$sum": "$organic_metrics.reply_count"},
                    "retweet_count": {"$sum": "$organic_metrics.retweet_count"},
                    "impression_count": {"$sum": "$organic_metrics.impression_count"},
                    "like_count": {"$sum": "$organic_metrics.like_count"},
                    "url_link_clicks": {"$sum": "$organic_metrics.url_link_clicks"},
                    "user_profile_clicks": {"$sum": "$organic_metrics.user_profile_clicks"},
                }
            },
            {"$addFields": {"date": "$_id"}},
            {"$sort": {"_id": 1}},
        ]
