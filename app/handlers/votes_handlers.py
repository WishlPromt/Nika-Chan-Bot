from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import app.content.votes as votes
import app.content.keyboards as kb
import app.handlers.control_messages as cm
import app.main.system as system

router = Router()


@router.message(Command('regvoting'))
async def cmd_regvoting(message: Message, bot: Bot):
    admins = await bot.get_chat_administrators(chat_id=message.chat.id)
    admin_list = [member.user.id for member in admins]

    args = message.text.split()

    starttime = 0

    if len(args) > 1:
        starttime = int(args[1])

    if message.from_user.id in admin_list:
        preposition_message = await cm.answer(message, "#Сбор_аватарок_чату\nНачинаем сбор аватарок для голосования!\nКидайте фото под это сообщение, чтобы предложить его в голосование")
        votes.register_voting(message.chat.id, int(preposition_message.message_id), starttime)
    else:
        await cm.reply(message, "У тебя нет прав")


@router.message(Command('vote'))
async def cmd_start_vote(message: Message):
    print(message.date)
    print(system.load_votes_base()["09KH1ODF49JGNM2K0LJ5"]["starttime"])
    print(system.get_message_data(message, message.chat.id)["date"])
    if system.load_votes_base()["09KH1ODF49JGNM2K0LJ5"]["starttime"] > system.get_message_data(message, message.chat.id)["date"]:
        await cm.answer(message, "Голосование еще не началось!")
        return

    if '-' not in str(message.chat.id):
        votes.add_user(message.from_user.id)
        await cm.answer(message=message,
                        text='Это голосование за аватарку для чата Коммуникабельные бабуины\n'
                        'У тебя будет 3 голоса, которые ты сможешь отдать любым понравившимся кандидатам\n'
                        'Понял(-а)? Летс го',
                        reply_markup=await kb.make_button('Летс го', 'next_variant_'))
    else:
        await cm.answer(message=message,
                        text='Голосование работает только у меня в лс @Nika_Chan_Bot')

@router.callback_query(F.data.startswith('next_variant'))
async def next_variant(callback: CallbackQuery):
    await callback.answer()

    key = callback.data.replace('next_variant_', '')

    if key != "end":
        variant = await votes.vote_variant(key)

        await callback.message.answer_photo(photo=variant["photo"],
                                            caption=variant["title"],
                                            reply_markup=variant["markup"])
    else:
        await cm.answer(callback.message,
                        "Ты просмотрел(-а) все варианты, теперь жди результаты")

@router.callback_query(F.data.startswith("vote"))
async def next_variant(callback: CallbackQuery):
    key = callback.data.replace("vote_", "")

    vote_status = await votes.vote(key, callback.from_user.id)

    if vote_status:
        await callback.answer(vote_status)
    else:
        await callback.answer("Ошибка")


@router.message(F.photo)
async def handle_save_photo(message: Message):
    right_id = system.load_votes_base()["09KH1ODF49JGNM2K0LJ5"]["preposition_message_id"]
    reply_message = message.reply_to_message

    if reply_message:
        if reply_message.message_id == right_id:
            await votes.download_vote_photo(message)


@router.message(F.video)
async def handle_save_video(message: Message):
    right_id = system.load_votes_base()["09KH1ODF49JGNM2K0LJ5"]["preposition_message_id"]
    reply_message = message.reply_to_message

    if reply_message:
        if reply_message.message_id == right_id:
            await votes.download_vote_video(message)
