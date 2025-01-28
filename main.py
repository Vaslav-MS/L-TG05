import asyncio, random, requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from datetime import datetime, timedelta
from config import TOKEN, CATAPIKEY, NASAAPIKEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_cat_breeds():
    url = 'https://api.thecatapi.com/v1/breeds'
    headers = {'x-api-key': CATAPIKEY}
    response = requests.get(url, headers=headers)
    return response.json()


def get_cat_image_by_breed(breed_id):
    url = f'https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}'
    headers = {'x-api-key': CATAPIKEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url']

def get_breed_info(breed_name):
    breeds = get_cat_breeds()
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():
            return breed
    return None

def get_random_apod():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    random_date = start_date + (end_date - start_date) * random.random()
    date_str = random_date.strftime("%Y-%m-%d")

    url = f'https://api.nasa.gov/planetary/apod?api_key={NASAAPIKEY}&date={date_str}'
    response = requests.get(url)
    return response.json()

@dp.message(Command('apod'))
async def random_apod(message: Message):
    apod = get_random_apod()
    photo_url = apod['url']
    title = apod['title']
    await message.answer_photo(photo=photo_url, caption=f'{title}')

@dp.message(CommandStart())
async def start(message: Message):
   await message.answer('Напиши название породы кошки, и я пришлю тебе её фото и описание.')

@dp.message()
async def cat_info(message: Message):
    breed_name = message.text
    if breed_name.isdigit():
        number_info = f'http://numbersapi.com/{breed_name}/math'
        response = requests.get(number_info)
        await message.answer(response.text)
    else:
        breed_info = get_breed_info(breed_name)
        if breed_info:
            cat_image_url = get_cat_image_by_breed(breed_info['id'])
            info = (
                f"Порода - {breed_info['name']}\n"
                f"Описание - {breed_info['description']}\n"
                f"Продолжительность жизни - {breed_info['life_span']} лет"
            )
            await message.answer_photo(photo=cat_image_url, caption=info)
        else:
            await message.answer('Порода не найдена. Попробуйте ещё раз.')

async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())