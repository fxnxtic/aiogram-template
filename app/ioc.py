from typing import AsyncIterable

from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from app.core import cfg
from app.database import Database


class ServicesProvider(Provider):
    def __init__(self) -> None:
        super().__init__(scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def database(self) -> AsyncIterable[Database]:
        autoupgrade = False # or make it depend from cfg.debug
        db = Database(cfg.db_url, autoupgrade)
        await db.startup()
        try:
            yield db
        finally:
            await db.shutdown()

    @provide(scope=Scope.APP)
    async def redis(self) -> AsyncIterable[Redis]:
        redis = Redis.from_url(cfg.redis_url)
        yield redis