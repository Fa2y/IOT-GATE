DEFAULT_KEY_PREFIX = "iot-gate"
DEBUG = False

class Config():
    if DEBUG:
        redis_url = 'redis://localhost:6379/?password=a740457a0ea017d4cd784c9ac9cb6a7724866df9'
    else:
        redis_url = 'redis://redis_streams:6379/?password=a740457a0ea017d4cd784c9ac9cb6a7724866df9'

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


class Keys:
    """Methods to generate key names for Redis data structures."""

    def __init__(self, prefix: str = DEFAULT_KEY_PREFIX):
        self.prefix = prefix

    @prefixed_key
    def flows_stream_key(self) -> str:
        """A stream containing 5-second flows on the network."""
        return f'stream:netview:5s'

    def alerts_stream_key(self) -> str:
        """A stream that stores network IDS alerts"""
        return f'stream:alerts'

    @prefixed_key
    def cache_key(self) -> str:
        return f'cache'


