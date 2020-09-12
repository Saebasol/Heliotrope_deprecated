import os

from tortoise import Tortoise
from .models import User


async def init():
    await Tortoise.init(
        db_url=f"mysql://{os.environ['DB_UNAME']}:{os.environ['DB_PW']}@{os.environ['DB_HOST']}:3306/{os.environ['DB_DBNAME']}",
        modules={"models": ["database.models"]},
    )

    await Tortoise.generate_schemas(safe=True)


__all__ = ["User"]
