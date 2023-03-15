from aiogram.dispatcher import Dispatcher
from aiogram import Bot
import os
from dotenv_config import load_dotenv
load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')
ADMINS = os.getenv('ADMINS')
#bot = Bot(token=API_TOKEN, parse_mode='HTML')
#dp = Dispatcher(bot)
# HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = 'https://your.domain'
WEBHOOK_PATH = '/path/to/api'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 3001
# DB_URL = os.getenv('HEROKU_POSTGRESQL_SILVER_URL')

