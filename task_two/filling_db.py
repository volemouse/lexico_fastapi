import asyncpg
import asyncio
import random

db_params = {
    "host": "localhost",
    "port": 5432,
    "database": "bobdb",
    "user": "postgres",
    "password": "111"
}



file_extensions = [".mp3", ".wav", ".flac", ".aac"]

async def fill_short_names():
    conn = await asyncpg.connect(**db_params)
    await conn.execute("TRUNCATE TABLE short_names")
    short_names_data = [("nazvanie" + str(i), random.choice([0, 1])) for i in range(1, 700001)]
    for name, status in short_names_data:
        await conn.execute("INSERT INTO short_names (name, status) VALUES ($1, $2)", name, status)
    await conn.close()


async def fill_full_names():
    conn = await asyncpg.connect(**db_params)
    await conn.execute("TRUNCATE TABLE full_names")
    short_names = await conn.fetch("SELECT name FROM short_names")
    full_names_data = []
    for name in random.sample(short_names, 500000):
        extension = random.choice(file_extensions)
        full_names_data.append((name["name"] + extension, None))
    for name, status in full_names_data:
        await conn.execute("INSERT INTO full_names (name, status) VALUES ($1, $2)", name, status)
    await conn.close()

async def main():
    await fill_short_names()
    await fill_full_names()

    
    
asyncio.run(main())