import motor
from beanie import init_beanie
from twill.config import mongo_settings
from twill.model.twitter import DailyStats, FollowCount, Tweet
from twill.model.user import BetaAccess, User


async def initialize_beanie():
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_settings.dsn)

    # Initialize beanie
    await init_beanie(
        client.twill, document_models=[User, Tweet, FollowCount, DailyStats, BetaAccess]
    )
