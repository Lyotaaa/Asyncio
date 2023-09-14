import asyncio
from aiohttp import ClientSession
from more_itertools import chunked
from config_db import engine, Base
from config_db import Session
from models import CharactersModels


async def async_drop_create_table_characters():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


async def get_information(url: str, client):
    response = await client.get(url)
    json_data = await response.json()
    return json_data


async def get_title_and_name(json_data: dict, client):
    for key, value in json_data.items():
        if type(value) == list:
            url_coro = [client.get(url) for url in value]
            url_list = await asyncio.gather(*url_coro)
            json_coro = [i.json() for i in url_list]
            json_list = await asyncio.gather(*json_coro)
            result_list = []
            for title_name in json_list:
                if title_name.get("title") is None:
                    result_list.append(title_name.get("name"))
                elif title_name.get("name") is None:
                    result_list.append(title_name.get("title"))
            json_data[key] = ", ".join(result_list)
    url = json_data.get("homeworld")
    if url is None:
        json_data["homeworld"] = None
    else:
        request = await client.get(url)
        response = await request.json()
        json_data["homeworld"] = response.get("name")
    return json_data


async def writing_database(json_data):
    async with Session() as session:
        list_character = []
        for json_character in json_data:
            new_character = CharactersModels(
                birth_year=json_character.get("birth_year"),
                eye_color=json_character.get("eye_color"),
                films=json_character.get("films"),
                gender=json_character.get("gender"),
                hair_color=json_character.get("hair_color"),
                height=json_character.get("height"),
                homeworld=json_character.get("homeworld"),
                mass=json_character.get("mass"),
                name=json_character.get("name"),
                skin_color=json_character.get("skin_color"),
                species=json_character.get("species"),
                starships=json_character.get("starships"),
                vehicles=json_character.get("vehicles"),
            )
            list_character.append(new_character)
            session.add(new_character)
            await session.commit()


async def main():
    await async_drop_create_table_characters()
    async with ClientSession() as client:
        max_requests = 5
        url = "https://swapi.dev/api/people/"
        for characters_id in chunked(range(1, 101), max_requests):
            characters_task = [
                get_information(f"{url}{i}", client=client) for i in characters_id
            ]
            characters = await asyncio.gather(*characters_task)
            coro_for_orm = [
                get_title_and_name(dict_, client=client) for dict_ in characters
            ]
            list_for_orm = await asyncio.gather(*coro_for_orm)
            paste_in_orm = writing_database(list_for_orm)
            asyncio.create_task(paste_in_orm)

    main_task = asyncio.current_task()
    insets_tasks = asyncio.all_tasks() - {main_task}
    for task in insets_tasks:
        await task
