import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from bot_token import token
from parcer import parce

bot = Bot(token=token)
dp = Dispatcher()
anek_counter = 0
anek_list = []

@dp.message()
async def echo_message(message: types.Message):
    global anek_counter, anek_list
    if message.text:
        await message.answer(
            text='Wait a second...'
        )
        if message.text.startswith('Ищи:'):
            anek_counter = 0
            search_phrase = str(message.text.split('Ищи: '))
            anek_list = parce(search_phrase)
            await message.answer(text=f'{anek_counter + 1}. ' + str(anek_list[anek_counter]))
        elif message.text.startswith('Еще'):
            anek_counter += 1
            is_short = False
            while not is_short:
                anek = str(anek_list[anek_counter])
                if len(anek) >= 4096:
                    anek_counter += 1
                else:
                    is_short = True
            if anek_counter >= len(anek_list):
                await message.answer(text='Анеки на этот запрос законились')
            await message.answer(text=f'{anek_counter + 1}. ' + str(anek_list[anek_counter]))
    else:
        await message.answer('Кажется, меня не научили отвечать на это...')


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
