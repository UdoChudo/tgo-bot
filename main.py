import os
import logging
import requests
from aiogram import Bot, Dispatcher, types, BaseMiddleware
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import asyncio
# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение токена из переменной окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
LOG_LEVEL = os.getenv("LOG_LEVEL")
CAT_API = os.getenv('CAT_TOKEN')
DOG_API = os.getenv('DOG_TOKEN')
BOT_OWNER_ID = os.getenv('BOT_OWNER')
if not BOT_TOKEN:
    raise ValueError("No API_TOKEN provided. Please set the API_TOKEN environment variable.")
if not CAT_API:
    raise ValueError("No CAT_TOKEN provided. Please set the CAT_TOKEN environment variable.")
if not DOG_API:
    raise ValueError("No DOG_TOKEN provided. Please set the DOG_TOKEN environment variable.")
if not BOT_OWNER_ID:
    raise ValueError("No BOT_OWNER_ID provided. Please set the BOT_OWNER_ID environment variable.")
FILE_PATH = "/app/data/users.txt"
FILE_PATH_WINDOWS = "./users.txt"
# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Middleware для ограничения частоты запросов
class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit=1.0):
        self.rate_limit = rate_limit
        self.last_time = {}
        super().__init__()

    async def __call__(self, handler, event, data):
        if isinstance(event, types.Message):
            user_id = event.from_user.id
            now = asyncio.get_event_loop().time()
            if user_id in self.last_time and now - self.last_time[user_id] < self.rate_limit:
                await event.answer("Подождите немного перед повторным нажатием!")
                return
            self.last_time[user_id] = now
        return await handler(event, data)

# Регистрируем middleware
dp.message.middleware(ThrottlingMiddleware())


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
    response = requests.get('https://api.thecatapi.com/api/images/get?api_key=' + CAT_API + '&format=json')
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
    response = requests.get('https://api.thedogapi.com/api/images/get?api_key=' + DOG_API + '&format=json')
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

@dp.message(Command("census"))
async def start_census(message: types.Message):
    if message.from_user.id != int(BOT_OWNER_ID):  # Убедитесь, что BOT_OWNER_ID это строка, конвертируем в int
        await message.answer("Только владелец бота может запускать перепись!")
        return

    # Исправленное создание клавиатуры
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Принять участие", callback_data="census_join")]
    ])

    await message.answer("Перепись участников начата! Нажмите кнопку ниже, чтобы участвовать.", reply_markup=keyboard)



@dp.callback_query(lambda c: c.data == "census_join")
async def register_user(callback_query: types.CallbackQuery):
    user = callback_query.from_user
    chat_id = callback_query.message.chat.id
    username = user.username or user.full_name

    try:
        with open("/app/data/users.txt", "r", encoding="utf-8") as file:
            existing_users = file.readlines()
    except FileNotFoundError:
        existing_users = []

    user_entry = f"{user.id}, @{username}\n"
    if user_entry in existing_users:
        await callback_query.answer("Вы уже записаны в перепись!")
        return

    with open("/app/data/users.txt", "a", encoding="utf-8") as file:
        file.write(user_entry)

    await callback_query.answer("Вы записаны в перепись!")

# Обработчик команды /sendfile
@dp.message(Command(commands=["sendfile"]))
async def send_file(message: Message):
    document = ""
    # Проверка, является ли отправитель владельцем бота
    if message.from_user.id != int(BOT_OWNER_ID):
        await message.answer("Только владелец бота может отправить файл!")
        return
    if os.path.exists(FILE_PATH):
        document = FSInputFile(FILE_PATH)
    elif os.path.exists(FILE_PATH_WINDOWS):
        document = FSInputFile(FILE_PATH_WINDOWS)
    else:
        await message.answer("Файл не найден на сервере")
    await bot.send_document(message.chat.id, document, caption="Вот ваш файл!")


@dp.message()
async def default_message(message: types.Message):
    pass

async def main():
    # Запуск polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
