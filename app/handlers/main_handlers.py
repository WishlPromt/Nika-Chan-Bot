from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command

import app.main.keyboards as kb
import app.content.shop as shop
import app.content.social_credits as sc
import app.content.profile as profile
import app.content.items_using as iu
import app.main.control_messages as cm

from system import *
from asyncio import sleep
from random import choice

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await cm.answer(message, 'Привет!')


@router.message(Command('help'))
async def cmd_start(message: Message):
    await cm.answer(message, 'Я бот для тг чатов')


@router.message(Command('economy'))
async def cmd_economy(message: Message):
    await cm.reply(message,
                   text='Команды экономики у тебя на экране',
                   reply_markup=kb.economy_markup)


@router.callback_query(F.data == 'delete_message')
async def cmd_delete_message(callback: CallbackQuery):
    await cm.delete(callback.message)


#social credits
@router.message(Command('work'))
async def cmd_work(message: Message):
    credits = sc.work(get_message_data(message, message.chat.id))
    sent_message = await cm.reply(message,
                                  text=credits,
                                  parse_mode='html')
    await cm.clear_messsages([message, sent_message])


@router.message(Command('collect'))
async def cmd_collect(message: Message):
    credits = sc.collect(get_message_data(message, message.chat.id))
    sent_message = await cm.reply(message,
                                  text=credits,
                                  parse_mode='html')
    await cm.clear_messsages([message, sent_message])


@router.message(Command('balance'))
async def cmd_balance(message: Message):
    sent_message = await message.reply(text=sc.balance(get_message_data(message,
                                                                        message.chat.id)),
                                       parse_mode='html')
    await cm.clear_messsages([message ,sent_message])


#Profile
@router.message(Command('profile'))
async def cmd_show_profile(message: Message):
    user_profile = profile.show_profile(get_message_data(message,
                                                         message.chat.id))
    if user_profile['card'] and not user_profile['gif']:
        sent_message = await message.reply_photo(photo=FSInputFile(user_profile['card']),
                                                 caption=user_profile['text'],
                                                 parse_mode='html')
    elif user_profile['card'] and user_profile['gif']:
        sent_message = await message.reply_animation(animation=FSInputFile(user_profile['card']),
                                                     caption=user_profile['text'],
                                                     parse_mode='html')
    else:
        sent_message = await message.reply(text=user_profile['text'],
                                           parse_mode='html')

    await cm.clear_messsages([message, sent_message], 300)


#shop
@router.message(Command('shop'))
async def cmd_shop(message: Message):
    sent_message = await cm.reply(message,
                                  text='Магазин',
                                  reply_markup=kb.shop_markup)
    await cm.clear_messsages([message, sent_message], 600)


#Go to general shop
@router.callback_query(F.data == 'shop_back')
async def cmd_shop_back(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text='Магазин',
                                     reply_markup=kb.shop_markup)


#Go to catalog in shop
@router.callback_query(F.data.startswith('shop_'))
async def cmd_shop_items(callback: CallbackQuery):
    catalog_id = callback.data.replace('shop_', '')
    catalog = await shop.cmd_shop_catalog(catalog_id,
                                          get_message_data(callback,
                                                         callback.message.chat.id))
    if catalog:
        await callback.answer()
        await callback.message.edit_text(text=catalog['text'],
                                         reply_markup=catalog['markup'])
    else:
        await callback.answer('Произошла ошибка', show_alert=True)
        return


#Select item to buy
@router.callback_query(F.data.startswith('buy_select_'))
async def cmd_buy_select(callback: CallbackQuery):
    select_id = str(callback.data.replace('buy_select_', ''))
    select = await shop.buy_choose(select_id, get_message_data(callback, callback.message.chat.id))
    if isinstance(select, dict):
        await callback.answer()
        await callback.message.edit_text(text=select['text'],
                                         reply_markup=select['markup'],
                                         parse_mode='html')
    elif select == 'exist':
        await callback.answer('У тебя уже есть это',
                              show_alert=True)
    else:
        await callback.answer(f'Для покупки нужна роль {select}',
                              show_alert=True)

#Buy item
@router.callback_query(F.data.startswith('buy_'))
async def cmd_buy_items(callback: CallbackQuery):
    buy_id = str(callback.data.replace('buy_', ''))
    buy_status = shop.buy(buy_id, get_message_data(callback, callback.message.chat.id))
    if not buy_status:
        await callback.answer(f'Ты купил {buy_id}',
                              show_alert=True)

    else:
        await callback.answer(buy_status)

#Back to shop catalog
@router.callback_query(F.data.startswith('back_to_'))
async def cmd_back_to_catalog(callback: CallbackQuery):
    catalog_id = callback.data.replace('back_to_', '')
    catalog = await shop.cmd_shop_catalog(catalog_id,
                                          get_message_data(callback,
                                                         callback.message.chat.id))
    if catalog:
        await callback.answer()
        await callback.message.edit_text(text=catalog['text'],
                                         reply_markup=catalog['markup'])
    else:
        await callback.answer('Произошла ошибка', show_alert=True)


@router.message(Command('fisting'))
async def cmd_fisting(message: Message, bot: Bot):
    fisting = iu.fisting(get_message_data(message, message.chat.id))

    master = message.from_user.username
    if message.reply_to_message:
        slave = message.reply_to_message.from_user.username
    else:
        slave = 'Воздух'
    answers = [f'♂{master}♂ пронзил ♂{slave}♂ своим мечом',
               f'♂{master}♂ посвятил ♂{slave}♂ в slaves',
               f'♂{slave}♂ был наказан ♂{master}♂',
               f'Кто-нибудь, скажите разрабу, что его попытки запихать гачи-мучи в бота-кошко-девку выглядят кринжово']
    if fisting == 'dungeon':
        sent_message = await message.reply(text=choice(answers),
                                           parse_mode='html')
    elif fisting == 'full':
        sent_message = await message.reply(text=choice(answers)+'\n Master получил ♂300 bucks♂ за свою работу',
                                           parse_mode='html')

    else:
        sent_message = await message.reply(text='Ты даже не ♂master♂',
                                           parse_mode='html')

    await sleep(600)
    await message.delete()
    await bot.delete_message(chat_id=sent_message.chat.id,
                             message_id=sent_message.message_id)
