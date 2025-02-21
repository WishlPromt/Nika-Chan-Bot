from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command

import app.content.votes as votes
import app.main.keyboards as kb
import app.main.control_messages as cm

router = Router()

@router.message(Command('vote'))
async def cmd_start_vote(message: Message):
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

    if key != 'end':
        variant = await votes.vote_variant(key)

        await callback.message.answer_photo(photo=variant['photo'],
                                            caption=variant['title'],
                                            reply_markup=variant['markup'])
    else:
        await cm.answer(callback.message,
                        'Ты просмотрел(-а) все варианты, теперь жди результаты')

@router.callback_query(F.data.startswith('vote'))
async def next_variant(callback: CallbackQuery):
    key = callback.data.replace('vote_', '')

    vote_status = await votes.vote(key, callback.from_user.id)

    if vote_status:
        await callback.answer("Ты проголосовал(-а) за этот вариант!")
    else:
        await callback.answer("Не получилось проголовать почему-то")
