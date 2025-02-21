from aiogram import Router, F, Bot

from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from system import *
import app.main.keyboards as kb
import app.content.inventory as inventory
import app.main.control_messages as cm
from asyncio import sleep

router = Router()


@router.message(Command('inventory'))
async def cmd_inventory(message: Message, bot: Bot):
    sent_message = await cm.reply(message,
                                  text='Твой инвентарь',
                                  reply_markup=kb.inventory_markup)

    await cm.clear_messsages([message, sent_message], 600)


#Go to general inventory
@router.callback_query(F.data == 'back_inventory')
async def cmd_inventory(callback: CallbackQuery):
    await callback.message.edit_text(text='Твой инвентарь',
                                     reply_markup=kb.inventory_markup)


#Go to inventory catalog
@router.callback_query(F.data.startswith('inventory_'))
async def cmd_inventory_items(callback: CallbackQuery):
    catalog_id = callback.data.replace('inventory_', '')
    catalog = await kb.items_inventory_markup(get_message_data(callback,
                                                               callback.message.chat.id),
                                              catalog_id)
    if catalog:
        await callback.answer()
        await callback.message.edit_text(text=catalog['text'],
                                         reply_markup=catalog['markup'])
    else:
        await callback.answer('Произошла ошибка', show_alert=True)


#Select inventory item
@router.callback_query(F.data.startswith('select_inventory_'))
async def cmd_choose_inventory_item(callback: CallbackQuery):
    item_id = callback.data.replace('select_inventory_', '')
    item = await kb.item_inventory_select(item_id,
                                          get_item_type(item_id),
                                          get_message_data(callback,
                                                           callback.message.chat.id))
    if item:
        await callback.answer()
        await callback.message.edit_text(text=item['text'],
                                         reply_markup=item['markup'],
                                         parse_mode='html')
    else:
        await callback.answer('Произошла ошибка', show_alert=True)


#Back to inventory catalog
@router.callback_query(F.data.startswith('back_inventory_to'))
async def cmd_back_inventory_catalog(callback: CallbackQuery):
    catalog_id = callback.data.replace('back_inventory_to_', '')
    catalog = await kb.items_inventory_markup(get_message_data(callback,
                                                               callback.message.chat.id),
                                              catalog_id)
    if catalog:
        await callback.answer()
        await callback.message.edit_text(text=catalog['text'],
                                         reply_markup=catalog['markup'])
    else:
        await callback.answer('Произошла ошибка', show_alert=True)


#Sell item
@router.callback_query(F.data.startswith('sell_inventory_item'))
async def cmd_sell_inventory_item(callback: CallbackQuery):
    item_id = callback.data.replace('sell_inventory_item_', '')
    status = inventory.sell_item(item_id, get_message_data(callback,
                                                           callback.message.chat.id))

    if status:
        await callback.answer(f'{item_id} продан',
                              show_alert=True)
    else:
        await callback.answer('Произошла ошибка')


#Set item to profile
@router.callback_query(F.data.startswith('set_profile_item'))
async def cmd_sell_inventory_item(callback: CallbackQuery):
    item_id = callback.data.replace('set_profile_item', '')
    print(item_id)
    status = inventory.set_item_to_profile(item_id, get_message_data(callback,
                                                                     callback.message.chat.id))
    if status:
        await callback.answer(f'{item_id} теперь в профиле(/profile)',
                              show_alert=True)
    else:
        await callback.answer('Произошла ошибка')
