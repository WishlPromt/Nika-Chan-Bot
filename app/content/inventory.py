from system import *

def get_inventory(user):
    check_user(user)
    base = load_base(user['chat_id'])
    id = user['id']

    inventory = base[id]['inventory']
    items = {}

    for type in inventory:
        if type != 'packs':
            items[type] = []
            for item in inventory[type]:
                items[type].append(item)
        else:
            items[type] = {}
            for item in inventory[type]:
                items[type][item] = inventory[type][item]
    return items


def get_card_rares(user):
    check_user(user)
    base = load_base(user['chat_id'])
    id = user['id']

    cards_rares = base[id]['cards']

    return cards_rares


def get_cards(user):
    check_user(user)
    base = load_base(user['chat_id'])
    id = user['id']

    cards_rares = base[id]['cards']
    cards = {}

    for rare in cards_rares:
        cards[rare] = []
        for card in cards_rares[rare]:
            cards[rare].append(card)
    return cards


def use_role(role, user):
    if role in get_inventory(user)['roles']:
        return True


def sell_item(item, user):
    check_user(user)
    base = load_base(user['chat_id'])
    items_base = load_items()

    for catalog in items_base:
        if item in items_base[catalog]:
            base[user['id']]['credits'] += int(items_base[catalog][item]['price'] / 2)
            base[user['id']]['inventory'][catalog].remove(item)
            save_base(base, user['chat_id'])
            return True

    return False


def set_item_to_profile(item, user):
    check_user(user)
    base = load_base(user['chat_id'])
    id = user['id']

    for catalog in base[id]['inventory']:
        if item in base[id]['inventory'][catalog]:
            if catalog == 'items':
                base[id]['favorite_item'] = item
                save_base(base, user['chat_id'])
                return True

            elif catalog == 'roles':
                base[id]['role'] = item
                save_base(base, user['chat_id'])
                return True
    return False
