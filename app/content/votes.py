from system import system

from aiogram.types import FSInputFile

import app.main.keyboards as kb


def add_user(id):
    vb = system.load_votes_base()
    if str(id) not in vb['09KH1ODF49JGNM2K0LJ5']['users_votes']:
        vb['09KH1ODF49JGNM2K0LJ5']['users_votes'][id] = 3
        system.save_votes_base(vb)


def new_avatar_for_vote(file, title):
    vb = system.load_votes_base()

    vb['09KH1ODF49JGNM2K0LJ5']['slots'][system.generate_id()] = {
            "photo": file,
            "title": title,
            "votes": 0
        }
    system.save_votes_base(vb)


async def vote_variant(key=None):
    vb = system.load_votes_base()

    variant = await kb.vote_variant_markup(key)
    key = variant['key']

    if variant:
        return{
            'markup': variant['markup'],
            'title': vb['09KH1ODF49JGNM2K0LJ5']['slots'][key]['title'],
            'votes': vb['09KH1ODF49JGNM2K0LJ5']['slots'][key]['votes'],
            'photo': FSInputFile(f'data/AvatarVote/{vb["09KH1ODF49JGNM2K0LJ5"]["slots"][key]["photo"]}')
        }


async def vote(key, id):
    vb = system.load_votes_base()
    if key in vb['09KH1ODF49JGNM2K0LJ5']['slots'] and str(id) in vb['09KH1ODF49JGNM2K0LJ5']['users_votes']:
        if vb['09KH1ODF49JGNM2K0LJ5']['users_votes'][str(id)] > 0:
            vb['09KH1ODF49JGNM2K0LJ5']['slots'][key]['votes'] += 1
            vb['09KH1ODF49JGNM2K0LJ5']['users_votes'][str(id)] -= 1
            system.save_votes_base(vb)

            return True
    return False
