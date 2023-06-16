import os
import asyncio
import aioredis
from fastapi.testclient import TestClient
from main import app, Address, PhoneData


def test_write_data():
    """Тест для проверки записи данных в Redis"""
    client = TestClient(app)
    phone_data = {
        "phone": "89991234567",
        "address": {
            "street": "321 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip_code": "12345"
        }
    }
    response = client.post("/write_data", json=phone_data)
    assert response.status_code == 200
    assert response.json() == {'message': 'Data written successfully'}


def test_check_data():
    """Тест для проверки чтения данных из Redis"""
    client = TestClient(app)
    phone = "89991234567"
    response = client.get(f"/check_data?phone={phone}")
    assert response.status_code == 200
    assert response.json() == {"address": {"street": "321 Main St", "city": "Anytown", "state": "CA", "zip_code": "12345"}}


async def test_stress():
    """Тест для проверки производительности"""
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = os.environ.get('REDIS_PORT', 6379)
    redis = await aioredis.create_redis_pool(f'redis://{redis_host}:{redis_port}')
    phone_data = {
        "phone": "89991234567",
        "address": {
            "street": "321 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip_code": "12345"
        }
    }
    try:
        tasks = []
        for i in range(100):
            tasks.append(asyncio.ensure_future(redis.set(phone_data['phone'] + str(i), phone_data['address'])))
        await asyncio.gather(*tasks)
    except Exception as e:
        assert False, f"Error writing data: {e}"
    else:
        assert True
    finally:
        redis.close()
        await redis.wait_closed()


if __name__ == '__main__':
    test_write_data()
    test_check_data()
    asyncio.run(test_stress())