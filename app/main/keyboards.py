from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.content.inventory import *
from system.system import load_base, load_items, load_votes_base

items_base = load_items()

economy_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/shop')],
    [KeyboardButton(text='/profile'),
     KeyboardButton(text='/inventory')
     ]
])

inventory_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Предметы', callback_data='inventory_items'),
     InlineKeyboardButton(text='Роли', callback_data='inventory_roles')],
    [InlineKeyboardButton(text='Паки', callback_data='inventory_packs'),
     InlineKeyboardButton(text='Карточки', callback_data='inventory_cards')]
])


shop_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Предметы', callback_data='shop_items')],
    [InlineKeyboardButton(text='Роли', callback_data='shop_roles'),
     InlineKeyboardButton(text='Паки', callback_data='shop_packs')]
])

async def make_button(text, callback):
    markup = InlineKeyboardBuilder()
    markup.add(InlineKeyboardButton(text=text, callback_data=callback))
    return markup.as_markup()


async def items_inventory_markup(user, catalog):
    markup = InlineKeyboardBuilder()
    markup.add(InlineKeyboardButton(text='◀ Назад', callback_data='back_inventory'))

    if catalog in ['items', 'roles', 'packs', 'cards']:

        if catalog != 'cards':
            for item in get_inventory(user)[catalog]:
                markup.add(InlineKeyboardButton(text=item, callback_data='select_inventory_'+item))

            text = None
            if catalog == 'items': text = 'Твои предметы'
            elif catalog == 'roles': text = 'Твои роли'
            elif catalog == 'packs': text = 'Твои паки'

            if text:
                return {'text': text,
                        'markup': markup.adjust(2).as_markup()}
        else:
            for rare in get_card_rares(user):
                markup.add(InlineKeyboardButton(text=rare.upper(), callback_data='select_cards_catalog_'+rare))

            text = 'Твои карточки'

            if text and markup:
                return {'text': text,
                        'markup': markup.adjust(2).as_markup()}

    return False


async def item_inventory_select(item, type, user):
    if item in items_base[type]:
        if type != 'packs':
            text = (f'<b>{item}</b>\n'
                    f'{items_base[type][item]["description"]}')

            markup = InlineKeyboardBuilder()
            markup.add(InlineKeyboardButton(text='◀ Назад',
                                            callback_data='back_inventory_to_'+type))
            markup.add(InlineKeyboardButton(text=f'🛒Продать[{int(items_base[type][item]["price"]/2)}]',
                                            callback_data='sell_inventory_item_'+item))
            markup.add(InlineKeyboardButton(text=f'👤В профиль',
                                            callback_data='set_profile_item'+item))
        else:
            text = (f'<b>{item}[{get_inventory(user)["packs"][item]}]</b>\n'
                    f'{items_base[type][item]["description"]}')

            markup = InlineKeyboardBuilder()
            markup.add(InlineKeyboardButton(text='◀ Назад',
                                            callback_data='back_inventory_to_' + type))
            markup.add(InlineKeyboardButton(text=f'🛒Продать[{int(items_base[type][item]["price"] / 2)}]',
                                            callback_data='sell_inventory_item_' + item))
            markup.add(InlineKeyboardButton(text=f'🎁Открыть',
                                            callback_data='open_pack_' + item))

        return {'text': text,
                'markup': markup.adjust(2).as_markup()}
    return False


async def items_shop_markup(user):
    markup = InlineKeyboardBuilder()
    markup.add(InlineKeyboardButton(text='◀ Назад', callback_data='shop_back'))
    for item in items_base['items']:
        access = items_base['items'][item]['access']
        if access in get_inventory(user)['roles']\
                or access == 'standart':
            markup.add(InlineKeyboardButton(text=item, callback_data='buy_select_' + item))
    return markup.adjust(2).as_markup()


async def roles_shop_markup(user):
    markup = InlineKeyboardBuilder()
    markup.add(InlineKeyboardButton(text='◀ Назад', callback_data='shop_back'))
    for role in items_base['roles']:
        access = items_base['roles'][role]['access']
        if access in get_inventory(user)['roles']\
                or access == 'standart':
            markup.add(InlineKeyboardButton(text=role, callback_data='buy_select_' + role))
    return markup.adjust(2).as_markup()


async def packs_shop_markup(user):
    markup = InlineKeyboardBuilder()
    markup.add(InlineKeyboardButton(text='◀ Назад', callback_data='shop_back'))
    for pack in items_base['packs']:
        access = items_base['packs'][pack]['access']
        if access in get_inventory(user)['roles']\
                or access == 'standart':
            markup.add(InlineKeyboardButton(text=pack, callback_data='buy_select_' + pack))
    return markup.adjust(2).as_markup()


async def buy_choose_markup(catalog, item):
    items_base = load_items()
    markup = InlineKeyboardBuilder()

    price = items_base[catalog][item]['price']

    markup.add(InlineKeyboardButton(text='❌Отмена', callback_data=f'back_to_{catalog}'))
    markup.add(InlineKeyboardButton(text=f'✔Купить[{price}]', callback_data=f'buy_{item}'))

    return markup.adjust(2).as_markup()


async def inventory_card_markup(card, rare, user):
    check_user(user)
    base = load_base(user['chat_id'])

    markup = InlineKeyboardBuilder()
    text: str = ''

    full_cards = base[user['id']]['cards'][rare]
    cards = list(dict.fromkeys(full_cards))

    for i in range(len(cards)):
        if cards[i] == card:
            previous_card = InlineKeyboardButton(text='◀Предыдущая', callback_data='show_inventory_card_'+cards[i-1])

            if i < len(cards)-1:
                next_card = InlineKeyboardButton(text='Следующая▶', callback_data='show_inventory_card_'+cards[i+1])
            else:
                next_card = InlineKeyboardButton(text='Следующая▶', callback_data='show_inventory_card_' + cards[0])
            markup.row(previous_card, next_card)

            markup.add(InlineKeyboardButton(text='🛒Продать', callback_data='sell_card_' + cards[i]))
            markup.add(InlineKeyboardButton(text='👤В профиль', callback_data='set_profile_card_' + cards[i]))

            text = (f'Карточка <b>#{card}</b> (x{full_cards.count(card)}) из инвентаря @{user["username"]}\n'
                    f'<b>{rare}</b>')
            break

    markup.add(InlineKeyboardButton(text='❌Закрыть', callback_data='delete_message'))

    return {'markup': markup.adjust(2).as_markup(),
            'text': text}


async def vote_variant_markup(key):
    markup = InlineKeyboardBuilder()
    vb = load_votes_base()
    keys = list(dict.fromkeys(vb['09KH1ODF49JGNM2K0LJ5']['slots']))
    print(keys)

    if len(keys) == 0:
        print(len(keys))
        return False

    variant = ''
    next_variant = 'end'

    if key == '':
        key = keys[0]
        variant = keys[0]
        if len(keys) > 1:
            next_variant = keys[1]
            print(next_variant)

    else:
        for i in keys:
            if i == key:
                variant = i
                if keys.index(i)+1 < len(keys)-1:
                    next_variant = keys[keys.index(i)+1]
                    print(keys[keys.index(i) + 1])

    markup.add(InlineKeyboardButton(text='Отдать голос👍', callback_data='vote_'+variant))
    markup.add(InlineKeyboardButton(text='Дальше', callback_data='next_variant_' + next_variant))

    return {
        'markup': markup.as_markup(),
        'key': key
    }
