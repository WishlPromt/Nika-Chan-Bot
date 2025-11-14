import app.content.inventory as inventory
from main_app import system as sys


def fisting(user):
    sys.check_user(user)
    if inventory.use_role('Full Master', user):
        base = sys.load_base(user['chat_id'])
        id = user['id']
        datetime = user['date']

        try:
            lock_time = base[id]['lock_time']['fisting']
        except:
            base[id]['lock_time']['fisting'] = 0
            lock_time = 0

        if lock_time <= datetime:
            base[id]['credits'] += 300

            new_lock_time = 4320
            if inventory.use_role('Истинный модератор', user):
                new_lock_time -= int(new_lock_time / 100 * 20)

            base[id]['lock_time']['fisting'] = int(user['date'] + new_lock_time)

            sys.save_base(base, user['chat_id'])

            return 'full'
        else:
            return 'dungeon'

    elif inventory.use_role('Dungeon master', user):
        return 'dungeon'

    return False
