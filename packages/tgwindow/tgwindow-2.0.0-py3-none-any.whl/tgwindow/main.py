import asyncio
import logging
from typing import Type

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message

from tgwindow.example import Hello
from tgwindow.middleware import UserMiddleware

dp = Dispatcher()
dp.message.middleware(UserMiddleware())
bot = Bot(token="6330365155:AAFUaRIDmsoKPnsr60r5ohkHOTG7xQHM19c", default=DefaultBotProperties(parse_mode="HTML"))


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

@dp.message(F.text == "/start")
async def start_m(msg: Message, hello: Hello, lang: str):
    hello.start(msg, lang=lang)
    # await msg.answer(**hello.start(lang=lang))

@dp.message()
async def one(msg: Message, hello: Type[Hello], lang: str):
    await msg.answer_photo(**hello.hello(lang=lang))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        logging.info("Бот запущен!")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен!")


