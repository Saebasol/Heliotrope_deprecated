import os

from tortoise import Tortoise
from .models import User
from .user_management import check_user, user_register


async def init():
    await Tortoise.init(
        db_url=f"mysql://{os.environ['DB_UNAME']}:{os.environ['DB_PW']}@{os.environ['DB_HOST']}:3306/{os.environ['DB_DBNAME']}",
        modules={"models": ["Heliotrope.utils.database.models"]},
    )

    await Tortoise.generate_schemas(safe=True)


async def close():
    await Tortoise.close_connections()


__all__ = ["User", "check_user", "user_register"]
