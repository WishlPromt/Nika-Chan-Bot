import app.main.keyboards as kb
from system import *


async def cmd_shop_catalog(catalog, user):
    text = None
    markup = None
    if catalog == 'items':
        text = 'Магазин предметов'
        markup = await kb.items_shop_markup(user)

    elif catalog == 'roles':
        text = 'Магазин ролей'
        markup = await kb.roles_shop_markup(user)

    elif catalog == 'packs':
        text = 'Магазин паков'
        markup = await kb.packs_shop_markup(user)

    if text and markup:
        return {'text': text,
                'markup': markup}

    else:
        return False


async def buy_choose(item, user):
    check_user(user)
    base = load_base(user['chat_id'])

    items_base = load_items()
    type = get_item_type(item)
    inventory = base[user['id']]['inventory']

    if item not in inventory[type] or type == 'packs':

        if items_base[type][item]['access'] != 'standart' and (
            items_base[type][item]['access'] not in inventory[type]):
            return items_base[type][item]['access']
        markup = await kb.buy_choose_markup(type, item)

        description = items_base[type][item]['description']

        text = (f'<b>{item}</b>\n'
                f'{description}')

        return {'text': text,
                'markup': markup}

    else:
        return 'exist'

def buy(item, user):
    check_user(user)
    chat_id = user['chat_id']
    base = load_base(user['chat_id'])
    items_base = load_items()
    id = user['id']
    credits = base[id]['credits']

    type = get_item_type(item)
    if not type:
        return False

    inventory = base[id]['inventory']
    price = items_base[type][item]['price']

    if type != 'packs':
        if credits >= price:
            if item not in inventory[type]:
                if items_base[type][item]['access'] != 'standart' and (
                        items_base[type][item]['access'] not in inventory[type]):
                    return f'Для покупки нужна роль {items_base[type][item]["access"]}'
                inventory[type].append(item)
                base[id]['credits'] -= price
                save_base(base, chat_id)
                return False
            else:
                return 'У тебя уже есть это'
        else:
            return 'У тебя нет денег'

    else:
        if credits >= price:
            if item not in inventory[type]:
                inventory[type][item] = 0
            inventory[type][item] += 1
            base[id]['credits'] -= price
            save_base(base, chat_id)
            return False
        else:
            return 'У тебя нет денег'

    return 'Произошла ошибка'
