import asyncio
import functools
from datetime import datetime, time, timedelta
from typing import List

from beanie.operators import Set
from tqdm import tqdm
from tweepy.asynchronous import AsyncClient
from twill.config import TwitterAPISettings, logger
from twill.database.mongo import initialize_beanie
from twill.model.twitter import DailyStats, EngagementAggregation, FollowCount, Tweet, UserPublicMetrics
from twill.model.user import User
from twill.service.analytics import update_follow_count_today

twitter_api_settings = TwitterAPISettings()

LAST_PERIOD_DAYS = 30


async def ingest_tweets(user_id: str):
    await initialize_beanie()

    # Get user twitter access details
    user = await User.get(user_id)
    if user is None:
        raise Exception("User not found")

    tweepy_client = AsyncClient(
        consumer_key=twitter_api_settings.consumer_key,
        consumer_secret=twitter_api_settings.consumer_secret,
        access_token=user.access_token,
        access_token_secret=user.access_token_secret,
    )

    # Get tweets since last tweet or from last 3 months
    get_user_tweets = functools.partial(
        tweepy_client.get_users_tweets,
        user.twitter_user_id,
        tweet_fields=[
            "organic_metrics",
            "context_annotations",
            "conversation_id",
            "created_at",
            "in_reply_to_user_id",
        ],
        expansions=["author_id"],
        user_auth=True,
        max_results=100,
    )

    tweets = []
    response = await get_user_tweets(start_time=datetime.now() - timedelta(days=LAST_PERIOD_DAYS))

    if response.data:
        tweets.extend(response.data)

    while response.meta.get("next_token"):
        response = await get_user_tweets(pagination_token=response.meta.get("next_token"))
        if response.data:
            tweets.extend(response.data)

    # Save tweets to database and update user last tweet id
    for i, res in enumerate(tqdm(tweets)):
        tweet = Tweet(**res)
        await tweet.save()


async def calculate_stats(user_id: str):
    await initialize_beanie()

    # Get user
    user = await User.get(user_id)

    # Get user public metrics
    tweepy_client = AsyncClient(
        consumer_key=twitter_api_settings.consumer_key,
        consumer_secret=twitter_api_settings.consumer_secret,
        access_token=user.access_token,
        access_token_secret=user.access_token_secret,
    )
    response = await tweepy_client.get_user(id=user.twitter_user_id, user_fields=["public_metrics"], user_auth=True)

    if response.errors:
        logger.error(f"error encountered fetching twitter user data: \n{response.errors}")
        return

    user_metrics = response.data
    user_metrics = UserPublicMetrics(**user_metrics["public_metrics"])

    # Update today's follower count
    await update_follow_count_today(user_id, user_metrics.followers_count)

    # Update last period's engagement total
    last_period_start = datetime.combine(datetime.utcnow() - timedelta(days=LAST_PERIOD_DAYS), time.min)
    engagement_aggregation_pipeline = EngagementAggregation.get_engagement_aggregation_pipeline(last_period_start)

    aggregations: List[EngagementAggregation] = await Tweet.aggregate(
        engagement_aggregation_pipeline, projection_model=EngagementAggregation
    ).to_list()

    for agg in aggregations:
        agg_dict = agg.dict(exclude={"id", "date"})
        day = datetime.strptime(agg.date, "%Y-%m-%d")
        stats = DailyStats(user_id=user_id, date=day, **agg_dict)

        # Update daily stats / insert if not exists
        await DailyStats.find_one(DailyStats.date == stats.date, DailyStats.user_id == stats.user_id,).upsert(
            Set(agg_dict),
            on_insert=stats,
        )


def main(params):
    # Local user test
    asyncio.run(ingest_tweets("6314b1032ece9a4d48bfaa8a"))
    asyncio.run(calculate_stats("6314b1032ece9a4d48bfaa8a"))

    print("parameters:", params)
