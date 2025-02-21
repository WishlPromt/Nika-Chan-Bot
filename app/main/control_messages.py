from aiogram import Bot
from aiogram.types import Message

import app.traffic_capture.traffic_capture as tc

from asyncio import sleep

async def answer(message: Message, text='', reply_markup=None, parse_mode=''):
    await tc.process_request()
    sent_message = await message.answer(text=text,
                                        reply_markup=reply_markup,
                                        parse_mode=parse_mode)
    await tc.clear_limit()
    return sent_message


async def reply(message: Message, text='', reply_markup=None, parse_mode=''):
    await tc.process_request()
    sent_message = await message.reply(text=text,
                                       reply_markup=reply_markup,
                                       parse_mode=parse_mode)
    await tc.clear_limit()
    return sent_message


async def edit_text(message: Message, text='', reply_markup=None, parse_mode=''):
    await tc.process_request()
    await message.edit_text(text=text,
                            reply_markup=reply_markup,
                            parse_mode=parse_mode)
    await tc.clear_limit()


async def delete_message(bot: Bot, chat_id: int | str, message_id: int):
    await tc.process_request()
    try:
        await bot.delete_message(chat_id=chat_id,
                                 message_id=message_id)
    except:
        print('message to delete not found')
    await tc.clear_limit()

async def delete(message: Message):
    await tc.process_request()
    try:
        await message.delete()
    except:
        print('message to delete not found')
    await tc.clear_limit()


async def clear_messsages(messages: list, delay=30):
    await sleep(delay)
    for message in messages:
        await delete(message)
