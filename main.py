from more_itertools import chunked
from fun_async import get_characters
import asyncio


if __name__ == "__main__":
    asyncio.run(get_characters(1))