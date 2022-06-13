import functools
import json
from datetime import datetime
import aioredis
import httpx
from aioredis.exceptions import ResponseError
import asyncio
from time import sleep
DEFAULT_KEY_PREFIX = "iot-gate"

DATA = [
        "192.168.14.32-8.8.8.8",
        "192.168.14.45-192.168.14.22",
        "192.168.14.45-8.8.8.8",
        "192.168.14.22-1.1.1.1",
        "192.168.14.22-142.251.37.174",
        "192.168.14.32-142.251.37.174",
        "192.168.14.45-98.137.11.164",
        ]

def prefixed_key(f):
    """
    A method decorator that prefixes return values.

    Prefixes any string that the decorated method `f` returns with the value of
    the `prefix` attribute on the owner object `self`.
    """

    def prefixed_method(*args, **kwargs):
        self = args[0]
        key = f(*args, **kwargs)
        return f'{self.prefix}:{key}'

    return prefixed_method

class Config():
    # The default URL expects the app to run using Docker and docker-compose.
    redis_url = 'redis://localhost:6379'

config = Config()
redis = aioredis.from_url(config.redis_url, decode_responses=True)

class Keys:
    """Methods to generate key names for Redis data structures."""

    def __init__(self, prefix: str = DEFAULT_KEY_PREFIX):
        self.prefix = prefix

    @prefixed_key
    def timeseries_flows_key(self) -> str:
        """A time series containing 10-second flows on the network."""
        return f'flows:10s'

    @prefixed_key
    def cache_key(self) -> str:
        return f'cache'

async def make_timeseries(key):
    """
    Create a timeseries with the Redis key `key`.

    We'll use the duplicate policy known as "first," which ignores
    duplicate pairs of timestamp and values if we add them.

    Because of this, we don't worry about handling this logic
    ourselves -- but note that there is a performance cost to writes
    using this policy.
    """
    try:
        await redis.execute_command(
            'TS.CREATE', key,
            'DUPLICATE_POLICY', 'LAST',
        )
    except ResponseError as e:
        # Time series probably already exists
        print('Could not create timeseries %s, error: %s', key, e)

async def initialize_redis(keys: Keys):
    await make_timeseries(keys.timeseries_flows_key())

async def flow_add(key, ts, flow):
    await redis.execute_command("TS.ADD",key, ts, flow)



async def main():
    keys = Keys()
    for flow in DATA:
        await flow_add(keys.timeseries_flows_key(), int(datetime.utcnow().timestamp()*1000), flow)

if __name__ == "__main__":
    asyncio.run(main())