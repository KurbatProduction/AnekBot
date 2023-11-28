import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from bot_token import token
from parcer import parce
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram import F
from aiogram.types import CallbackQuery

bot = Bot(token=token)
dp = Dispatcher()
anek_counter = 0
anek_list = []

show_more_button = InlineKeyboardButton(
    text='Следующий Анек',
    callback_data='show_more'
)

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [show_more_button]
    ]
)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "АнекБот создан исключительно в развлекательных целях. Его разработчик не собирается коммерциализировать его "
        "работу.\nВся информация взята из открытых источников исключительно легальным образом.\nДля начала "
        "взаимодействия с ботом просто введите текст, по которому хотите выполнить поиск анекдота. В ответ вам придет "
        "сообщение с текстом анекдота и прикрепленной к нему кнопкой для просмотра следующего анекдота по уже "
        "отправленному вами запросу. Если вы хотите сформировать новый запрос, просто отправьте его."
    )


@dp.callback_query(F.data == 'show_more')
async def process_buttons_press(callback: CallbackQuery):
    global anek_counter, anek_list
    anek_counter += 1
    if len(anek_list) <= anek_counter:
        await callback.message.answer(text='Анеки по вашему запросу закончились')
    else:
        await callback.message.answer(
            text=str(anek_list[anek_counter]),
            reply_markup=keyboard
        )


@dp.message()
async def show_first_anek(message: Message):
    global anek_counter, anek_list
    if message.text:
        await message.answer(text='Wait a second...')
        anek_counter = 0
        anek_list = parce(message.text)
        if not anek_list:
            await message.answer(
                text='По вашему запросу ничего не найдено'
            )
        else:
            await message.answer(
                text=str(anek_list[anek_counter]),
                reply_markup=keyboard
            )
    else:
        await message.reply('Кажется, меня ещё не научили отвечать на это...')


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot, allowed_updates=[])


if __name__ == '__main__':
    asyncio.run(main())
