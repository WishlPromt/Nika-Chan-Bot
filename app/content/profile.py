from system import *
from app.content.cards import load_card, get_card_rare, get_card_extension

def show_profile(user):
    check_user(user)
    base = load_base(user['chat_id'])
    username = user['username']
    id = user['id']

    favorite_card = load_card(base[id]['favorite_card'], get_card_rare(base[id]['favorite_card']))

    text = (f'<b>{username}</b> — <b>{base[id]["role"]}</b>\n'
            f'Социальные кредиты: <b>{base[id]["credits"]}</b>\n'
            f'Любимый предмет: <b>{base[id]["favorite_item"]}</b>\n'
            f'Любимая карточка: <b>{base[id]["favorite_card"]}</b>')

    if not favorite_card:
        return {'text': text,
                'card': False,
                'gif': False}

    elif get_card_extension(base[id]['favorite_card']) != 'gif':
        return {'text': text,
                'card': favorite_card,
                'gif': False}

    else:
        return {'text': text,
                'card': favorite_card,
                'gif': True}


def set_profile_card(card, user):
    check_user(user)
    base = load_base(user['chat_id'])
    id = user['id']

    if '.' in card:
        card = card.split('.')[0]
    print(card)

    if card in base[id]['cards'][get_card_rare(card)]:
        base[id]['favorite_card'] = card
        save_base(base, user['chat_id'])

        return card

    else:
        return False
