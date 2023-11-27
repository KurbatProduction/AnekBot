import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot_token import token
from parcer import parce
from aiogram.filters import Command

bot = Bot(token=token)
dp = Dispatcher()
anek_counter = 0
anek_list = []


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(
        "АнекБот создан исключительно в развлекательных целях. Его разработчик не собирается коммерциализировать его работу.\nВся информация взята из открытых источников исключительно легальным образом.\nДля начала взаимодействия с ботом просто введите текст, по которому хотите выполнить поиск анекдот. В ответ вам придет сообщение с текстом анекдота и прикрепленной к нему кнопкой для просмотра следующего анекдота по уже отправленному вами запросу. Если вы хотите сформировать новый запрос, просто отправьте его."
    )


@dp.message()
async def echo_message(message: types.Message):
    global anek_counter, anek_list
    if message.text:
        await message.answer(text='Wait a second...')
        anek_counter = 0
        search_phrase = str(message.text.split('Ищи: '))
        anek_list = parce(search_phrase)
        await message.answer(
            text=f'{anek_counter + 1}. ' + str(anek_list[anek_counter]),
            reply_markup=more_btn
        )
    else:
        await message.answer('Кажется, меня не научили отвечать на это...')


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
