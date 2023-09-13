from config_db import engine, Base
import aiohttp
from pprint import pprint


async def async_drop_table_characters():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

async def async_create_table_characters():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def get_characters(character_id: int):
    url = "https://swapi.dev/api/people/"
    session = aiohttp.ClientSession()
    response = await session.get(f"{url}{character_id}")
    json_data = await response.json()
    await session.close()
    pprint(json_data)
    return json_data