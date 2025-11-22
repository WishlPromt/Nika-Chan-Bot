import os

from app.main import system
from app.main.config import config
from aiogram.types import FSInputFile

def change_ids():
    base = system.load_fullbase()
    for chat in base.keys():
        for user in base[chat].keys():
            for rare in base[chat][user]['cards']:
                for card in base[chat][user]['cards'][rare]:
                    print(card)
                    index = base[chat][user]['cards'][rare].index(card)
                    base[chat][user]['cards'][rare][index] = card.split('.')[0]

    system.save_fullbase(base)


def load_card(card, rare):
    if rare not in config.CARD_RARES:
        return False

    card = card.strip()
    if '.' in card:
        card = card.split('.')[0]
    for c in os.listdir(f'{system.get_base_path()}/cards/{rare}'):
        current_card = c.split('.')[0].strip()
        if current_card == card:
            return f'{system.get_base_path()}/cards/{rare}/{c}'

    return False


def make_card(card, extension, caption):
    rare = get_card_rare(card)
    if not rare:
        return

    if extension in ['png', 'jpg', 'jpeg']:
        card = FSInputFile(f'{system.get_base_path()}/cards/{rare}/{card}.{extension}')
        return {'card': card,
                'caption': caption,
                'type': 'photo'}

    elif extension == 'gif':
        card = FSInputFile(f'{system.get_base_path()}/cards/{rare}/{card}.{extension}')
        return {'card': card,
                'caption': caption,
                'type': 'animation'}

    else:
        return False


def get_card_rare(card):
    if card.find('.') != -1:
        card = card[:card.find('.')]

    try:
        for rare in config.CARD_RARES:
            for c in os.listdir(f'{system.get_base_path()}/cards/{rare}'):
                if card == c[:c.find('.')]:
                    return rare
    except:
        return False


def get_card_extension(card):
    for rare in os.listdir(f'{system.get_base_path()}/cards/'):
        for c in os.listdir(f'{system.get_base_path()}/cards/{rare}/'):
            if card == c.split('.')[0]:
                return c.split('.')[1]


def check_profile_card(card, user):
    system.check_user(user)
    base = system.load_base(user['chat_id'])
    fav_card = base[user['id']]['favorite_card']

    if fav_card.find('.'):
        fav_card = fav_card.split('.')[0]

    if card == fav_card:
        return True
