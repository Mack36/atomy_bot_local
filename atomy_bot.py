#!./bin/python3.9
import logging
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData
import asyncio
# from sql import create_pool
import re
from config import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, API_TOKEN, WEBHOOK_URL, ADMINS
import texts
import shelve
import ssl

WEBHOOK_SSL_CERT = './mypublic.pem'
WEBHOOK_SSL_PRIV = './myprivate.key'

admins = []
admins = ADMINS.split(',')
lang = 0
banner = "https://jamabucket.s3.us-east-2.amazonaws.com/telegram+bot+files/img/misc/img_prod.jpg"
FILENAMEDB = "atomy_bot_db"
bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

statestmp = {}


async def store(user_id, obj):
    with shelve.open(FILENAMEDB) as storage:
        storage[str(user_id)] = obj
    storage.close()


async def get_user_data(user_id):
    with shelve.open(FILENAMEDB) as storage:
        try:
            userdata = storage.get(str(user_id))
            storage.close()
            return userdata
        except KeyError:
            storage.close()
            return None


async def del_user_data(user_id):
    with shelve.open(FILENAMEDB) as storage:
        del storage[str(user_id)]
    storage.close()


async def on_startup(dp):
    with open(WEBHOOK_SSL_CERT, 'rb') as cert_file:
        await bot.set_webhook(WEBHOOK_URL, certificate=cert_file)
    #await bot.set_webhook(WEBHOOK_URL)
    for admin in admins:
        await bot.send_message(admin, 'Bot has started')


async def on_shutdown():
    await bot.delete_webhook()


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    kb = await lang_sel_inline()
    await bot.send_photo(message.chat.id, banner, reply_markup=kb)


async def main_menu(message: types.Message):
    lang = await get_user_data(message.chat.id)
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(texts.menu_main[lang][1], callback_data='about_company'),
           InlineKeyboardButton(texts.menu_main[lang][2], callback_data='about_products'),
           InlineKeyboardButton(texts.menu_main[lang][3], callback_data='about_business'),
           InlineKeyboardButton(texts.menu_main[lang][4], callback_data='become_partner'))
    # await bot.answer_callback_query(callback_query_id=call.id)
    await bot.send_message(message.chat.id, texts.menu_main_desc[lang], reply_markup=kb, parse_mode='HTML')


async def lang_sel_inline():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("UZBEK", callback_data='uzbek'),
           InlineKeyboardButton("RUSSIAN", callback_data='russian'))
    return kb


@dp.callback_query_handler(filters.Regexp(r'(uzbek|russian)'))
async def inline_lang_sel(call: CallbackQuery):
    lang = 0
    if call.data == "uzbek":
        lang = 1  # uzb
    else:
        lang = 2  # ru
    await store(call.from_user.id, lang)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, texts.greeting[lang])
    await bot.answer_callback_query(callback_query_id=call.id)
    await main_menu(call.message)


@dp.callback_query_handler(filters.Regexp(r'about_company'))
async def inline_aboutc(call: CallbackQuery):
    lang = await get_user_data(call.message.chat.id)
    kb = InlineKeyboardMarkup(row_width=1)
    # kb.add(InlineKeyboardButton(texts.about_menu[lang][1], callback_data='cfaq'),
    #        InlineKeyboardButton(texts.about_menu[lang][2], callback_data='main_menu'))
    kb.add(InlineKeyboardButton(texts.main_btn[lang], callback_data='main_menu'))
    await bot.answer_callback_query(callback_query_id=call.id)
    # statestmp[call.from_user.id] = 10
    await bot.send_photo(call.from_user.id, banner)
    await bot.send_message(call.from_user.id, texts.about[lang], reply_markup=kb)


@dp.callback_query_handler(filters.Regexp(r'about_products'))
async def inline_aboutprod(call: CallbackQuery):
    lang = await get_user_data(call.message.chat.id)
    kb = InlineKeyboardMarkup(row_width=1)
    # kb.add(InlineKeyboardButton(texts.about_prod_menu[lang][1], callback_data='pfaq'),
    #        InlineKeyboardButton(texts.about_prod_menu[lang][2], callback_data='main_menu'))
    kb.add(InlineKeyboardButton(texts.about_prod_menu[lang][1], callback_data='sites'),
           InlineKeyboardButton(texts.about_prod_menu[lang][2], callback_data='telegram'),
           InlineKeyboardButton(texts.main_btn[lang], callback_data='main_menu'))
    await bot.answer_callback_query(callback_query_id=call.id)
    await bot.send_photo(call.from_user.id, banner)
    # statestmp[call.from_user.id] = 20
    await bot.send_message(call.from_user.id, texts.about_prod_desc[lang], reply_markup=kb)


@dp.callback_query_handler(filters.Regexp(r'sites'))
async def inline_sites(call: CallbackQuery):
    lang = await get_user_data(call.message.chat.id)
    await bot.answer_callback_query(callback_query_id=call.id)
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton('🇺🇿 Atomy Uzbekistan', url=texts.site_urls[0]),
           #InlineKeyboardButton('рџ‡№рџ‡· Atomy Turkey', url=texts.site_urls[1]),
           InlineKeyboardButton('🇰🇷 Atomy Korea', url=texts.site_urls[2]),
           InlineKeyboardButton(texts.main_btn[lang], callback_data='main_menu'))
    await bot.send_message(call.message.chat.id, texts.sites_desc[lang], reply_markup=kb)


@dp.callback_query_handler(filters.Regexp(r'telegram'))
async def inline_telegram(call: CallbackQuery):
    lang = await get_user_data(call.message.chat.id)
    await bot.answer_callback_query(callback_query_id=call.id)
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton('https://t.me/atomybeautygroup', url='https://t.me/atomybeautygroup'),
           InlineKeyboardButton(texts.main_btn[lang], callback_data='main_menu'))
    await bot.send_message(call.message.chat.id, texts.telegram_desc[lang], reply_markup=kb)


@dp.callback_query_handler(filters.Regexp(r'main_menu'))
async def inline_main_menu(call: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=call.id)
    await main_menu(call.message)


@dp.callback_query_handler(filters.Regexp(r'cfaq'))
async def inline_faq_about(call: CallbackQuery):
    lang = await get_user_data(call.message.chat.id)
    await bot.answer_callback_query(callback_query_id=call.id)
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(texts.faq_about_menu[lang][1], callback_data='ans1'),
           InlineKeyboardButton(texts.faq_about_menu[lang][2], callback_data='ans2'),
           InlineKeyboardButton(texts.faq_about_menu[lang][3], callback_data='ans3'),
           InlineKeyboardButton(texts.faq_about_menu[lang][4], callback_data='ans4'),
           InlineKeyboardButton(texts.faq_about_menu[lang][5], callback_data='ans5'),
           InlineKeyboardButton(texts.faq_about_menu[lang][6], callback_data='ans6'),
           InlineKeyboardButton(texts.faq_about_menu[lang][7], callback_data='main_menu'))
    global statestmp
    statestmp[call.from_user.id] = 10
    await bot.send_message(call.message.chat.id, texts.faq_about_desc[lang], reply_markup=kb)


@dp.callback_query_handler(filters.Regexp(r'about_business'))
async def inline_aboutbus(call: CallbackQuery):
    lang = await get_user_data(call.message.chat.id)
    await bot.answer_callback_query(callback_query_id=call.id)
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(texts.faq_menu[lang], callback_data='cfaq'),
           InlineKeyboardButton(texts.faq_about_menu[lang][7], callback_data='main_menu'))
    await bot.send_message(call.message.chat.id, texts.about[lang], reply_markup=kb)


@dp.callback_query_handler(filters.Regexp(r'ans[0-9].*'))
async def inline_faq_ans(call: CallbackQuery):
    lang = await get_user_data(call.message.chat.id)
    tmpcalldata = call.data.split('ans')
    answer_id = int(tmpcalldata[1])
    await bot.answer_callback_query(callback_query_id=call.id)
    # await bot.send_message(call.message.chat.id, texts.faq_about_menu[lang][answer_id])
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(texts.menu_back[lang][1], callback_data='back'),
           InlineKeyboardButton(texts.menu_back[lang][2], callback_data='main_menu'))
    await bot.send_message(call.message.chat.id, texts.faq_answers[lang][answer_id], reply_markup=kb)


@dp.callback_query_handler(filters.Regexp(r'back'))
async def inline_main_menu(call: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=call.id)
    global statestmp
    if call.from_user.id in statestmp:
        if statestmp[call.from_user.id] == 10:
            await inline_faq_about(call)
        if statestmp[call.from_user.id] == 20:
            await inline_aboutprod(call)
    else:
        await main_menu(call.message)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        ssl_context=ssl_context
    )
    # executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)

