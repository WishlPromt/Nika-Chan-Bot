from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaAnimation
from aiogram.filters import Command

from system import system
from system.system import rares
import app.content.cards as cardslib
import app.main.keyboards as kb
import app.content.inventory as inventory
import app.content.profile as profile

router = Router()

@router.message(Command('load_card'))
async def cmd_load_card(message: Message):
    try:
        card_id = message.text.split(' ')[1]
    except:
        try:
            card_id = message.text.split('#')[1]
        except:
            card_id = False

    if card_id:
        path = cardslib.load_card(card=card_id,
                                  rare=cardslib.get_card_rare(card_id))

        if path:
            card = cardslib.make_card(card_id, path[path.find('.')+1:], f'#{card_id}\n'
                                                                      f'{cardslib.get_card_rare(card_id)}')
            if card:
                if card['type'] == 'photo':
                    await message.answer_photo(photo=card['card'])
                else:
                    await message.answer_animation(animation=card['card'])
        else:
            await message.answer('Произошла ошибка при поиске карточки в файловой системе')

    else:
        await message.answer('Карточка не найдена')


#Show cards in inventory by rare
@router.callback_query(F.data.startswith('select_cards_catalog_'))
async def cmd_select_cards_catalog(callback: CallbackQuery, bot: Bot):
    await callback.answer()

    chat_id = callback.message.chat.id

    rare = callback.data.replace('select_cards_catalog_', '')

    if rare in rares:
        user_cards = inventory.get_cards(system.get_message_data(callback, chat_id))

        if user_cards:
            card_id = user_cards[rare][0]

            card_banner = await kb.inventory_card_markup(card_id,
                                                         rare,
                                                         system.get_message_data(callback, callback.message.chat.id))
            if not card_banner['markup']:
                await callback.answer('markup error')
                return

            if not card_banner['text']:
                await callback.answer('text error')
                return

            path = cardslib.load_card(card_id, rare)

            if path:
                card = cardslib.make_card(card=card_id,
                                          extension=path[path.find('.')+1:],
                                          caption=card_banner['text']
                                          )

                if card:
                    if card['type'] == 'photo':
                        await bot.send_photo(
                            chat_id=chat_id,
                            photo=card['card'],
                            caption=card['caption'],
                            reply_markup=card_banner['markup'],
                            parse_mode='html'
                        )
                    else:
                        await bot.send_animation(
                            chat_id=chat_id,
                            animation=card['card'],
                            caption=card['caption'],
                            reply_markup=card_banner['markup'],
                            parse_mode='html'
                        )
            else:
                await callback.answer('path error')


@router.callback_query(F.data.startswith('back_inventory_cards_to_rares'))
async def cmd_back_inv_to_card_rares(callback: CallbackQuery, bot: Bot):
    message_id = callback.message.message_id
    chat_id = callback.message.chat.id

    catalog = await kb.items_inventory_markup(system.get_message_data(callback, chat_id),
                                        'cards')

    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    await bot.send_message(chat_id=chat_id,
                           text=catalog['text'],
                           reply_markup=catalog['markup'])


@router.callback_query(F.data.startswith('show_inventory_card_'))
async def cmd_swap_cards_inventory(callback: CallbackQuery, bot: Bot):
    card_id = callback.data.replace('show_inventory_card_', '')
    message_id = callback.message.message_id
    chat_id = callback.message.chat.id

    rare = cardslib.get_card_rare(card_id)

    if rare:
        card_banner = await kb.inventory_card_markup(card_id,
                                                     rare,
                                                     system.get_message_data(callback, callback.message.chat.id))

        if not card_banner['markup']:
            await callback.answer('markup error')
            return

        if not card_banner['text']:
            await callback.answer('text error')
            return

        path = cardslib.load_card(card_id, rare)

        if path:

            card = cardslib.make_card(card=card_id,
                                      extension=path[path.find('.') + 1:],
                                      caption=card_banner['text'])

            if card['type'] == 'photo':
                card['card'] = InputMediaPhoto(media=card['card'],
                                               caption=card['caption'],
                                               parse_mode='html')
            else:
                card['card'] = InputMediaAnimation(media=card['card'],
                                                   caption=card['caption'],
                                                   parse_mode='html')

            if card:
                await bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=message_id,
                    media=card['card'],
                    reply_markup=card_banner['markup']
                )
        else:
            await callback.answer('path error')


@router.callback_query(F.data.startswith('set_profile_card_'))
async def cmd_set_profile_card(callback: CallbackQuery):
    card_id = callback.data.replace('set_profile_card_', '')

    if cardslib.check_profile_card(card_id, system.get_message_data(callback, callback.message.chat.id)):
        await callback.answer('Эта карточка уже в твоем профиле')
        return

    success = profile.set_profile_card(card_id, system.get_message_data(callback, callback.message.chat.id))

    if success:
        await callback.answer(f'Карточка #{card_id} установлена в твоем профиле!',
                              show_alert=True)
    else:
        await callback.answer('Ошибка! :(',
                              show_alert=True)
