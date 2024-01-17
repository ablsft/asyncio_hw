import asyncio

from aiohttp import ClientSession

from db import engine, Session
from models import Base, SwapiPeople
from more_itertools import chunked


CHUNK_SIZE = 10

PEOPLE_URL = 'https://swapi.dev/api/people'
PLANETS_URL = 'https://swapi.dev/api/planets'
FILMS_URL = 'https://swapi.dev/api/films'
SPECIES_URL = 'https://swapi.dev/api/species'
VEHICLES_URL = 'https://swapi.dev/api/vehicles'
STARSHIPS_URL = 'https://swapi.dev/api/starships'


async def get_data(url: str, session: ClientSession) -> dict:
    print(f'started {url=}')
    async with session.get(url) as response:
        json_data = await response.json(content_type=None)
        print(f'finished {url=}')
        return json_data


async def get_data_by_id(field_id: int, entity_url: str, session: ClientSession) -> tuple[str, dict]:
    id_url = f'{entity_url}/{field_id}/'
    json_data = await get_data(id_url, session)

    return id_url, json_data


async def get_count(url: str, session: ClientSession) -> dict:
    json_data = await get_data(url, session)
    return json_data['count']


def data_processing(data: list) -> list:
    people = []
    urls_names = {}
    for id_url, json_data in data:
        if not json_data.get('detail'):
            if 'people' in id_url:
                json_data.pop('created')
                json_data.pop('edited')
                json_data.pop('url')

                people.append(json_data)
            else:
                name = json_data.get('name') or json_data.get('title')
                urls_names[id_url] = name

    fields = ['films', 'homeworld', 'species', 'vehicles', 'starships']
    for person in people:
        for field in fields:
            urls = person.get(field)

            if not isinstance(urls, list):
                urls = [urls]
            names = [urls_names.get(url) for url in urls]

            person[field] = ', '.join(names)

    return people


async def paste_to_db(people: list):
    async with Session() as session:
        session.add_all([SwapiPeople(**person) for person in people])
        await session.commit()


async def main():

    urls = [
        PEOPLE_URL, PLANETS_URL, 
        FILMS_URL, SPECIES_URL,
        VEHICLES_URL, STARSHIPS_URL,
    ]

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()


    async with ClientSession() as session:
        coros = [get_count(url, session) for url in urls]
        count = await asyncio.gather(*coros)
        
        url_count = dict(zip(urls, count))
        url_count[STARSHIPS_URL] = 75
        url_count[VEHICLES_URL] = 75

        data = []
        for url in urls:
            coros = (get_data_by_id(i, url, session) for i in range(1, url_count[url]+1))
            for coros_chunk in chunked(coros, CHUNK_SIZE):
                chunk_data = await asyncio.gather(*coros_chunk)
                data.extend(chunk_data)

    people = data_processing(data)
    await paste_to_db(people)
    

if __name__ == '__main__':
    asyncio.run(main())
