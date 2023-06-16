import os
import re
import aioredis
import uvicorn

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, validator

app = FastAPI()
PHONE_REGEX = re.compile(r'^(\+7|8)?[\s\(]*\d{3}[\s\)]*\d{3}[-\s]*\d{2}[-\s]*\d{2}$')

class Address(BaseModel):
    """Класс для валидации адреса """
    street: str
    city: str
    state: str
    zip_code: str

class PhoneData(BaseModel):
    """Класс для входных параметров на запись """
    phone: str
    address: Address

    
    """Валидация телефона """
    @validator('phone')
    def validate_phone(cls, phone):
        if not PHONE_REGEX.match(phone):
            raise ValueError('Invalid phone number format')
        return phone

async def startup_event():
    """ функция для создания Redis-пула при запуске приложения хост и порт получаем из окружения, иначе дефолт"""
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = os.environ.get('REDIS_PORT', 6379)
    app.state.redis = await aioredis.create_redis_pool(f'redis://{redis_host}:{redis_port}')


async def shutdown_event():
    """функция для закрытия Redis-соединения при завершении приложения """
    app.state.redis.close()
    await app.state.redis.wait_closed()


@app.on_event('startup')
async def startup_wrapper():
    """добавляем обработчик события 'startup', который вызывает функцию startup_event """
    await startup_event()


@app.on_event('shutdown')
async def shutdown_wrapper():
    """добавляем обработчик события 'shutdown', который вызывает функцию shutdown_event """
    await shutdown_event()


async def get_redis():
    """функция для получения соединения Redis с помощью зависимости Depends """
    return app.state.redis

@app.post('/write_data')
async def write_data(phone_data: PhoneData, redis=Depends(get_redis)):
    """принимаем данные о телефоне и соединение Redis через зависимость Depends
    на вход json вида:
                {
                "phone": "89991234567",
                "address": {
                    "street": "321 Main St",
                    "city": "Anytown",
                    "state": "CA",
                    "zip_code": "12345"
                    }
                }
    """
    
    try:
        await redis.set(phone_data.phone, phone_data.address.json())
    except Exception as e:
        return {'message': f'Error writing data: {e}'}
    else:
        return {'message': 'Data written successfully'}

@app.get('/check_data')
async def check_data(phone: str, redis=Depends(get_redis)):
    """обработчик GET-запроса на /check_data принимаем номер телефона и соединение Redis через зависимость Depends"""
    try:
        if not PHONE_REGEX.match(phone):
            raise HTTPException(status_code=422, detail='Invalid phone number format')

        address_json = await redis.get(phone)
        if address_json:
            address = Address.parse_raw(address_json)
            return {'address': address}
        else:
            return {'message': 'Data not found'}
    except Exception as e:
        return {'message': f'Error checking data: {e}'}

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', reload=True, port=8000)