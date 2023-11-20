from aiogram import Router
from config.config import load_config, Config
from services.functions import load_users_id

config: Config = load_config()
router = Router()
users_id = load_users_id()