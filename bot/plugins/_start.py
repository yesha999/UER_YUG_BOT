import re

from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup

from bot.helpers.custom_filters import condition_is, is_user_banned
from bot.db.db_functions.change_db_functions import change_user_name, change_user_condition, change_user_phone
from bot.db.db_functions.check_db_functions import check_user_is_registered
from bot.helpers.keyboards import main_menu_keyboard, reply_markup_keyboard
from bot.helpers.messages import WELCOME_MESSAGE, FIRST_MESSAGE, PHONE_NUMBER_MESSAGE, NAME_ERROR_MESSAGE, \
    PHONE_ERROR_MESSAGE


# Файл называется _start чтобы быть первым в папке plugins, это позволяет выйти из любой ситуации командой /start

@Client.on_message((filters.command("start") | filters.regex("^Главное меню$")) & filters.private & is_user_banned)
async def start_bot(bot: Client, message: Message):
    is_registered = check_user_is_registered(message)
    if is_registered:
        change_user_condition(message, 'main_menu')
        await message.reply_text(text=WELCOME_MESSAGE, reply_markup=main_menu_keyboard)
    else:
        await message.reply_text(text=FIRST_MESSAGE)


@Client.on_message(filters.text & filters.private & condition_is('change_name') & is_user_banned)
async def name_registration(bot: Client, message: Message):
    check_name_regular = re.fullmatch('^[A-ЯЁ][а-яё]+\s[A-ЯЁ][а-яё]+$', message.text)
    if check_name_regular:
        change_user_name(message)
        change_user_condition(message, 'change_phone')
        await message.reply_text(PHONE_NUMBER_MESSAGE)
    else:
        await message.reply_text(text=NAME_ERROR_MESSAGE)


@Client.on_message(filters.text & filters.private & condition_is('change_phone') & is_user_banned)
async def phone_registration(bot: Client, message: Message):
    check_phone_regular1 = re.fullmatch('^((\+7)([0-9]){10})$', message.text)  # Слитно
    check_phone_regular2 = re.fullmatch('^\+7 ?\(\d{3}\) ?\d\d\d[- .]\d\d[- .]\d\d$',
                                        message.text)  # В формате +7 (908) 190-54-26 и похожих
    if check_phone_regular1 or check_phone_regular2:
        change_user_phone(message)
        change_user_condition(message, 'main_menu')
        await message.reply_text(text='Регистрация успешно завершена!', reply_markup=reply_markup_keyboard)
        await start_bot(bot, message)
    else:
        await message.reply_text(text=PHONE_ERROR_MESSAGE)
