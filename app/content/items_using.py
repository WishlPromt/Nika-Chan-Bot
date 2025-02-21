import app.content.inventory as inventory
from system import system as sys


def fisting(user):
    sys.check_user(user)
    if inventory.use_role('Full Master', user):
        base = sys.load_base(user['chat_id'])
        id = user['id']
        base[id]['credits'] += 300

        new_lock_time = 4320
        if inventory.use_role('Истинный модератор', user):
            new_lock_time -= int(new_lock_time / 100 * 20)

        base[id]['lock_time']['collect'] = int(user['date'] + new_lock_time)

        sys.save_base(base, user['chat_id'])

        return 'full'

    elif inventory.use_role('Dungeon master', user):
        return 'dungeon'

    return False
