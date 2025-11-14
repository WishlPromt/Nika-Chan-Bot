from main_app import system

from aiogram.types import FSInputFile, Message

import app.main.keyboards as kb
import app.main.control_messages as cm


def register_voting(chat_id, pm_id: int, starttime, max_votes=3):
    base = system.load_votes_base()

    base["09KH1ODF49JGNM2K0LJ5"] = {
        "chat_id": chat_id,
        "preposition_message_id": pm_id,
        "starttime": starttime,
        "max_votes": max_votes,
        "users_votes": {

        },
        "slots": {

        }
    }

    system.save_votes_base(base)


def add_user(id):
    vb = system.load_votes_base()
    if str(id) not in vb['09KH1ODF49JGNM2K0LJ5']['users_votes']:
        vb['09KH1ODF49JGNM2K0LJ5']['users_votes'][id] = []
        system.save_votes_base(vb)


async def download_vote_photo(message: Message):
    id = system.generate_id()
    path = f"{system.get_base_path()}\\data\\AvatarVote\\{id}.png"

    try:
        await message.bot.download(file=message.photo[-1].file_id, destination=path)
        await cm.reply(message, "Ваше фото сохранено!")
    except:
        await cm.reply(message, "Произошла ошибка при скачивании(((")
        return
    if message.caption:
        title = message.caption
    else:
        title = id

    try:
        new_avatar_for_vote(path, title)
    except:
        await cm.answer(message, "Ошибка при добавлении фото в базу данных")


async def download_vote_video(message: Message):
    id = system.generate_id()
    path = f"{system.get_base_path()}\\data\\AvatarVote\\{id}.mp4"

    try:
        await message.bot.download(file=message.video[-1].file_id, destination=path)
        await cm.reply(message, "Ваше видео сохранено!")
    except:
        await cm.reply(message, "Произошла ошибка при скачивании(((")
        return
    if message.caption:
        title = message.caption
    else:
        title = id

    try:
        new_avatar_for_vote(path, title)
    except:
        await cm.answer(message, "Ошибка при добавлении фото в базу данных")


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

    file_name = vb["09KH1ODF49JGNM2K0LJ5"]["slots"][key]["photo"]

    photo = FSInputFile(file_name)

    if variant:
        return{
            'markup': variant['markup'],
            'title': vb['09KH1ODF49JGNM2K0LJ5']['slots'][key]['title'],
            'votes': vb['09KH1ODF49JGNM2K0LJ5']['slots'][key]['votes'],
            'photo': photo
        }


async def vote(key, id):
    vb = system.load_votes_base()
    user_votes = vb['09KH1ODF49JGNM2K0LJ5']['users_votes'][str(id)]
    vote_key = '09KH1ODF49JGNM2K0LJ5'

    if key in vb[vote_key]['slots'] and str(id) in vb[vote_key]['users_votes']:
        if key in user_votes:
            return "Ты уже отдал голос за этот вариант"

        if len(user_votes) < vb[vote_key]['max_votes']:
            vb[vote_key]['slots'][key]['votes'] += 1
            vb[vote_key]['users_votes'][str(id)].append(key)
            system.save_votes_base(vb)

            return "Ты проголосовал за этот вариант!"
        else:
            return "У тебя закончились голоса!"

    return False
