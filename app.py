import asyncio
from datetime import datetime
import logging

from aiogram import Bot, Dispatcher, Router, types
from bot_token import token, db_token
from parcer import parce
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram import F
from aiogram.types import CallbackQuery
from pymongo.mongo_client import MongoClient

client = MongoClient(db_token)
db = client.AnekBot_DB
collection = db.users

bot = Bot(token=token)
dp = Dispatcher()

show_more_button = InlineKeyboardButton(
    text='Следующий Анек',
    callback_data='show_more'
)

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [show_more_button]
    ]
)


async def add_user(user_id):
    date = datetime.now().date()
    collection.insert_one({
        '_id': user_id,
        'date': str(date)
    })


async def add_user_query(user_id, key_words):
    anek_list = parce(key_words)
    collection.update_one(
        {'_id': user_id},
        {'$set':
            {
                'user_query': key_words,
                'anek_list': anek_list
            }
        }
    )


async def get_anek_for_user(user_id):
    is_one_more_anek = False
    anek_list = collection.find(
        {'_id': user_id},
        {'_id': 0, "anek_list": 1}
    )
    anek_list = anek_list[0]['anek_list']
    if not anek_list:
        return 'Анеки по вашему запросу закончились', is_one_more_anek
    else:
        is_one_more_anek = True
        anek = anek_list.pop(0)
        collection.update_one(
            {'_id': user_id},
            {'$set':
                {
                    'anek_list': anek_list
                }
            }
        )
    return anek, is_one_more_anek


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "АнекБот создан исключительно в развлекательных целях. Его разработчик не собирается коммерциализировать его "
        "работу.\nВся информация взята из открытых источников исключительно легальным образом.\nДля начала "
        "взаимодействия с ботом просто введите текст, по которому хотите выполнить поиск анекдота. В ответ вам придет "
        "сообщение с текстом анекдота и прикрепленной к нему кнопкой для просмотра следующего анекдота по уже "
        "отправленному вами запросу. Если вы хотите сформировать новый запрос, просто отправьте его."
    )
    user_id = message.chat.id
    if not collection.find_one({'_id': user_id}):
        await add_user(user_id)


@dp.callback_query(F.data == 'show_more')
async def process_buttons_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    anek, is_one_more_anek = await get_anek_for_user(user_id)
    if not is_one_more_anek:
        await callback.message.edit_reply_markup()
        await callback.message.answer(
            text=anek
        )
    else:
        await callback.message.edit_reply_markup()
        await callback.message.answer(
            text=anek,
            reply_markup=keyboard
        )


@dp.message()
async def show_first_anek(message: Message):
    if message.text:
        user_id = message.chat.id
        await message.answer(text='Wait a second...')
        await add_user_query(user_id, message.text)
        anek, is_one_more_anek = await get_anek_for_user(user_id)
        if not is_one_more_anek:
            await message.answer(
                text='По вашему запросу ничего не найдено'
            )
        else:
            await message.answer(
                text=str(anek),
                reply_markup=keyboard
            )
    else:
        await message.reply('Кажется, меня ещё не научили отвечать на это...')


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot, allowed_updates=[])


if __name__ == '__main__':
    asyncio.run(main())
