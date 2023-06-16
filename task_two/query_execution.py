import asyncpg
import asyncio
import time


def timeit(func):
    async def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = await func(*args, **kwargs)
        end_time = time.monotonic()
        elapsed_time = end_time - start_time
        print(f'Time taken: {elapsed_time:.2f} seconds')
        return result
    return wrapper

@timeit
async def update_full_names_from_short_names(conn_string):
    res, err = True, ''
    try:
        conn = await asyncpg.connect(conn_string)
        query = '''
                UPDATE full_names fn
                SET status = sh.status
                FROM short_names sh
                WHERE SUBSTRING(fn.name, 1, POSITION('.' IN fn.name) - 1) = sh.name;
        '''
        await conn.fetch(query)
    except Exception as e:
        res,err =False, f'ошибка при обновлении {e}'
    finally:
        await conn.close()
        return res, err

conn_string = 'postgresql://postgres:111@localhost/bobdb'
res, err =asyncio.run(update_full_names_from_short_names(conn_string))
