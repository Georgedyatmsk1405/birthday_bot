import aioredis


class Redis:
    async def set(self, key, value):
        redis = aioredis.from_url(
            "redis://localhost", encoding="utf-8", decode_responses=True
        )
        await redis.set(key, value, ex=60 * 60 * 24)

    async def get(self, key):
        redis = aioredis.from_url(
            "redis://localhost", encoding="utf-8", decode_responses=True
        )
        return await redis.get(key)


redis = Redis()
