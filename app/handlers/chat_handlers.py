from aiogram import F, Router, Bot
from aiogram.types import Message
from main_app.model import model_response
import app.main.control_messages as cm


router = Router()


@router.message(F.text.contains("Ника"))
@router.message(F.text.contains("ника"))
@router.message(F.text.contains("nika"))
@router.message(F.text.contains("Nika"))
async def message_handler(message: Message):
    user_prompt = message.text

    result = await model_response(context="", user_prompt=user_prompt, username=message.from_user.username)

    if result:
        sent_message = await cm.answer(message=message, text=result)
        await cm.clear_messsages(messages=[message, sent_message], delay=300)

