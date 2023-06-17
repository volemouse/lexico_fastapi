import asyncpg
import asyncio

async def correct_test(conn_string):
    error_dict = []
    try:
        conn = await asyncpg.connect(conn_string)
        query_short = 'SELECT name, status FROM public.short_names'
        query_full = 'select name, status from public.full_names'
        rows_short = await conn.fetch(query_short)
        rows_full = await conn.fetch(query_full)
        short_names_dict = {row['name']: row['status'] for row in rows_short}
        full_names_dict = {row['name'].split('.')[0]: row['status'] for row in rows_full}
        for k,v in full_names_dict.items():
            if k not in short_names_dict:
                error_dict.append({k:v})
                continue
            if full_names_dict[k] != short_names_dict[k]:
                error_dict.append({k:v})
    except Exception as e:
        print(f"Error while getting short names: {e}")
    finally:
        await conn.close()
        return error_dict




conn_string = 'postgresql://postgres:111@localhost/bobdb'
error_dict =asyncio.run(correct_test(conn_string))
print(error_dict)