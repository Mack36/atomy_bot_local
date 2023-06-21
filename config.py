from aiogram.dispatcher import Dispatcher
from aiogram import Bot
import os
from dotenv_config import load_dotenv
load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')
ADMINS = os.getenv('ADMINS')
TESTENV = os.getenv('TESTENV')
#bot = Bot(token=API_TOKEN, parse_mode='HTML')
#dp = Dispatcher(bot)
# HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
PUBLIC_IP = os.getenv('PUBLIC_IP')
WEBHOOK_HOST = f"https://{PUBLIC_IP}"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = os.getenv('PORT', default=443)
# DB_URL = os.getenv('HEROKU_POSTGRESQL_SILVER_URL')

