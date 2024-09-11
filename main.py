import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import os
import asyncio

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение токена из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_LEVEL = os.getenv("LOG_LEVEL")
API_TOKEN_CATS = os.getenv("CATS_TOKEN")
API_TOKEN_DOGS = os.getenv("DOGS_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN provided. Please set the API_TOKEN environment variable.")

# Настраиваем логирование
logging.basicConfig(level=logging.ERROR)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик команды /boobs
@dp.message(Command(commands=['boobs'], prefix="!/"))
async def send_boobs(message: Message):
    # Выполнение запроса к API oboobs
    response = requests.get('http://api.oboobs.ru/boobs/1/1/random')
    if response.status_code == 200:
        data = response.json()
        if data:
            # Получение значения preview
            preview = data[0]['preview']

            # Убираем подстроку "_preview" из пути
            img_path = preview.replace("_preview", "")

            # Формируем полный URL
            img_url = f'https://media.oboobs.ru/{img_path}'
            # Отправка картинки и сообщения в групповой чат
            await bot.send_photo(
                chat_id=message.chat.id,  # Отправка в тот же чат, где была вызвана команда
                photo=img_url,
                has_spoiler=True,
                caption=f"{message.from_user.username} заказал сиськи!"
            )
        else:
            await message.answer("Не удалось получить данные с сервера.")
    else:
        await message.answer("Ошибка при выполнении запроса к API.")

# Обработчик команды /boobs
@dp.message(Command(commands=['butts'], prefix="!/"))
async def send_butts(message: Message):
    # Выполнение запроса к API oboobs
    response = requests.get('http://api.obutts.ru/butts/1/1/random')
    if response.status_code == 200:
        data = response.json()
        if data:
            # Получение значения preview
            preview = data[0]['preview']

            # Убираем подстроку "_preview" из пути
            img_path = preview.replace("_preview", "")

            # Формируем полный URL
            img_url = f'http://media.obutts.ru/{img_path}'
            # Отправка картинки и сообщения в групповой чат
            await bot.send_photo(
                chat_id=message.chat.id,  # Отправка в тот же чат, где была вызвана команда
                photo=img_url,
                has_spoiler=True,
                caption=f"{message.from_user.username} заказал жопки!"
            )
        else:
            await message.answer("Не удалось получить данные с сервера.")
    else:
        await message.answer("Ошибка при выполнении запроса к API.")

@dp.message(Command(commands=['cats'], prefix="!/"))
async def send_cats(message: Message):
    response = requests.get('https://api.thecatapi.com/api/images/get?api_key=API_TOKEN_CATS&format=json')
    if response.status_code == 200:
        data = response.json()
        if data:
            img_url = str(data[0]['url'])
            await bot.send_photo(
                chat_id=message.chat.id,  # Отправка в тот же чат, где была вызвана команда
                photo=img_url,
                has_spoiler=False,
                caption=f"{message.from_user.username} заказал котиков!"
            )
        else:
            await message.answer("Не удалось получить данные с сервера.")
    else:
        await message.answer("Ошибка при выполнении запроса к API.")

@dp.message(Command(commands=['dogs'], prefix="!/"))
async def send_dogs(message: Message):
    response = requests.get('https://api.thedogapi.com/api/images/get?api_key=API_TOKEN_DOGS&format=json')
    if response.status_code == 200:
        data = response.json()
        if data:
            img_url = str(data[0]['url'])
            await bot.send_photo(
                chat_id=message.chat.id,  # Отправка в тот же чат, где была вызвана команда
                photo=img_url,
                has_spoiler=False,
                caption=f"{message.from_user.username} заказал пёсиков!"
            )
        else:
            await message.answer("Не удалось получить данные с сервера.")
    else:
        await message.answer("Ошибка при выполнении запроса к API.")
@dp.message()
async def default_message(message: types.Message):
    pass

async def main():
    # Регистрация обработчиков
    dp.message.register(send_boobs)
    dp.message.register(send_butts)
    dp.message.register(send_cats)
    dp.message.register(send_dogs)

    # Запуск polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
