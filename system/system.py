import json
import datetime
import time
import string
import random

def load_base(chat_id):
    with open('../data/DataBase.json', 'r', encoding='utf-8') as file:
        base = json.load(file)
        file.close()
        return base[chat_id]


def load_fullbase():
    fullbase = json.load(open('../data/DataBase.json', 'r', encoding='utf-8'))
    return fullbase

def load_votes_base():
    return json.load(open('../data/VotesBase.json', 'r', encoding='utf-8'))

def save_votes_base(base):
    with open('../data/VotesBase.json', 'w', encoding='utf-8') as file:
        json.dump(base, file, indent=4, ensure_ascii=False)
        file.close()


def save_base(base, chat_id):
    fullbase = load_fullbase()

    fullbase[chat_id] = base
    with open('../data/DataBase.json', 'w', encoding='utf-8') as file:
        json.dump(fullbase, file, indent=4, ensure_ascii=False)
        file.close()

def save_fullbase(base):
    with open('../data/DataBase.json', 'w', encoding='utf-8') as file:
        json.dump(base, file, indent=4, ensure_ascii=False)
        file.close()


def load_items():
    with open('../data/items.json', 'r', encoding='utf-8') as file:
        items_base = json.load(file)
        return items_base


def get_item_type(item):
    items_base = load_items()
    type: str = ''
    if item in items_base['items']:
        type = 'items'
    if item in items_base['roles']:
        type = 'roles'
    if item in items_base['packs']:
        type = 'packs'
    return type


def get_message_data(data, chat_id):
    id = str(data.from_user.id)

    username = data.from_user.username
    if not username:
        username = data.from_user.first_name
    try:
        msg_date = str(data.date)[:str(data.date).find('+')]
        date = int(datetime.datetime.strptime(msg_date, '%Y-%m-%d %H:%M:%S').timestamp())
    except:
        date = 0

    return {'id': id,
            'chat_id': str(chat_id),
            'username': username,
            'date': date}


def create_user(user):
    base = load_base(user['chat_id'])
    base[user['id']] = {
        'username': user['username'],
        'credits': 0,
        'lock_time': {
            'work': 0,
            'collect': 0
        },
        'favorite_item': 'Нет предмета',
        'role': 'Нет роли',
        'favorite_card': 'Нет карты',
        'inventory': {
            'items': [],
            'roles': [],
            'packs': {}
        },
        'cards': {
            'common': [],
            'rare': [],
            'epic': [],
            'legendary': [],
            'secret': []
        },
        'new_cards': [],
        'cur_card': 0,
        'selled_cards': []
    }
    save_base(base, user['chat_id'])


def check_user(user):
    fullbase = load_fullbase()
    if user['chat_id'] not in fullbase:
        fullbase[user['chat_id']] = {}
        save_base(fullbase[user['chat_id']], user['chat_id'])

    base = load_base(user['chat_id'])

    if user['id'] not in base.keys():
        create_user(user)

def generate_id():
    all_symbols = string.ascii_uppercase + string.digits
    result = ''.join(random.choice(all_symbols) for _ in range(20))
    return result


def convert_time(dttm):
    return time.strftime('%H:%M:%S %d.%m.%Y', time.localtime(dttm))
