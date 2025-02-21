from random import randint
from system.system import *
import app.content.inventory as inventory

def work(user):
    chat_id = user['chat_id']
    check_user(user)
    base = load_base(chat_id)
    id = user['id']
    username = user['username']

    lock_time = base[id]['lock_time']['work']
    datetime = user['date']

    if lock_time <= datetime:
        credits = randint(30, 45)
        if inventory.use_role('Работяга', user):
            credits += int(credits / 100 * 40)

        base[id]['credits'] += credits

        new_lock_time = 7200
        if inventory.use_role('Липовый модератор', user):
            new_lock_time -= int(new_lock_time / 100 * 15)
        if inventory.use_role('Истинный модератор', user):
            new_lock_time -= int(new_lock_time / 100 * 20)

        base[id]['lock_time']['work'] = int(datetime + new_lock_time)

        save_base(base, chat_id)

        lock_time = base[id]['lock_time']['work']
        return (f'{username}, ты заработал(-а) <b>{credits}</b> кредитов\n'
                f'В следующий раз ты сможешь воркать в <i>{str(convert_time(lock_time))}(UTC)</i>')

    else:
        return (f'{username}, не так быстро!\n'
                f'Ты сможешь воркать только в <b>{str(convert_time(lock_time))}(UTC)</b>')


def collect(user):
    check_user(user)
    base = load_base(user['chat_id'])
    items_base = load_items()
    id = user['id']
    user_inventory = base[id]['inventory']

    text = f'{user["username"]}, ты заработал(-а): <b><collects></b>\n'
    collects = 0

    lock_time = base[id]['lock_time']['collect']
    datetime = user['date']

    if lock_time <= datetime:
        if not user_inventory['items'] and not user_inventory['roles']:
            text = f'{user["username"]}, твой инвентарь пустой, но ты можешь пополнить его в /shop'

        else:

            if user_inventory['items']:
                for item in user_inventory['items']:
                    item_collect = items_base['items'][item]['collects']
                    collects += item_collect
                    text += f'<i>{item}</i> - {item_collect}\n'

            if user_inventory['roles']:
                for role in user_inventory['roles']:
                    role_collect = items_base['roles'][role]['collects']
                    if role_collect not in ['random', 'bonus']:
                        collects += role_collect
                    else:
                        if role_collect == 'random':
                            role_collect = randint(-30, 45)
                            collects += role_collect
                        elif role_collect == 'bonus':
                            role_collect = '+15%'
                    text += f'<i>{role}</i> - {role_collect}\n'

            if inventory.use_role('Предприниматель', user):
                collects += int(collects / 100 * 15)

            base[id]['credits'] += collects

            new_lock_time = 43200
            if inventory.use_role('Липовый модератор', user):
                new_lock_time -= int(new_lock_time / 100 * 15)
            if inventory.use_role('Истинный модератор', user):
                new_lock_time -= int(new_lock_time / 100 * 20)

            base[id]['lock_time']['collect'] = int(datetime + new_lock_time)

            save_base(base, user['chat_id'])
            text = text.replace('<collects>', str(collects))
            text += f'Ты снова сможешь использовать /collect только в {str(convert_time(lock_time))}(UTC)'

    else:
        text = (f'{user["username"]}, не так быстро!\n'
                f'Ты снова сможешь использовать /collect только в {str(convert_time(lock_time))}(UTC)')

    return text


def balance(user):
    chat_id = user['chat_id']
    check_user(user)
    base = load_base(chat_id)
    id = user['id']
    username = user['username']

    return (f'{username}, твои социальные кредиты:\n'
            f'<b>{base[id]["credits"]}</b>')
