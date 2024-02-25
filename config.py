from aiogram.dispatcher import Dispatcher
from aiogram import Bot
import os
from dotenv import load_dotenv
import requests


load_dotenv()  

#ip = requests.get("http://169.254.169.254/latest/meta-data/public-ipv4").content
ip = requests.get("http://checkip.amazonaws.com").text
#curl http://checkip.amazonaws.com
API_TOKEN = os.getenv('BOT_TOKEN')
ADMINS = os.getenv('ADMINS')
TESTENV = (os.getenv('TESTENV', 'False') == 'True')

# webhook settings
PUBLIC_IP = ip.replace('\n', '')
#.decode('utf-8')
WEBHOOK_HOST = f"https://{PUBLIC_IP}"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = os.getenv('PORT', default=443)

