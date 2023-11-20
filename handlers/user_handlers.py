from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.keyboards import new_pagination_kb
from config.config import load_config, Config
from services.functions import load_users_id

config: Config = load_config()
router = Router()
users_id = load_users_id()

@router.message(CommandStart())
async def proccess_start_command(message: Message) -> None:
    await message.answer(text='text',
                         reply_markup=new_pagination_kb(15, 115))
