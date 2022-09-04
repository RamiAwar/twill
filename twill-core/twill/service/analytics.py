from datetime import datetime, time

from beanie.operators import Set
from twill.model.twitter import FollowCount


async def update_follow_count_today(user_id: str, followers_count: int):
    # Update today's follower count
    today = datetime.combine(datetime.utcnow(), time.min)
    follow_count = FollowCount(
        user_id=user_id,
        date=today,  # Calculate today's date
        followers_count=followers_count,
    )

    # Update today's follower count / insert if not exists
    await FollowCount.find_one(
        FollowCount.date == follow_count.date,
        FollowCount.user_id == follow_count.user_id,
    ).upsert(
        Set({FollowCount.followers_count: follow_count.followers_count}),
        on_insert=follow_count,
    )
