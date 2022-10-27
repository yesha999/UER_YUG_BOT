import re

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.helpers.custom_filters import condition_is, is_user_banned
from bot.db.db_functions.change_db_functions import change_user_name, change_user_condition, change_user_phone
from bot.db.db_functions.check_db_functions import check_user_phone
from bot.helpers.keyboards import call_me_keyboard
from bot.helpers.messages import NAME_ERROR_MESSAGE, PHONE_ERROR_MESSAGE, \
    CHANGE_NAME_SUCCESS_MESSAGE, CHANGE_PHONE_SUCCESS_MESSAGE, confirm_phone_number


@Client.on_message(filters.text & filters.private & condition_is('change_name_settings') & is_user_banned)
async def change_name_settings(bot: Client, message: Message):
    check_name_regular = re.fullmatch('^[A-ЯЁ][а-яё]+\s[A-ЯЁ][а-яё]+$', message.text)
    if check_name_regular:
        change_user_name(message)
        change_user_condition(message, "main_menu")
        await message.reply_text(CHANGE_NAME_SUCCESS_MESSAGE)
    else:
        await message.reply_text(text=NAME_ERROR_MESSAGE)


@Client.on_message(filters.text & filters.private & condition_is('change_phone_settings') & is_user_banned)
async def change_phone_settings(bot: Client, message: Message):
    check_phone_regular1 = re.fullmatch('^((\+7)([0-9]){10})$', message.text)  # Слитно
    check_phone_regular2 = re.fullmatch('^\+7 ?\(\d{3}\) ?\d\d\d[- .]\d\d[- .]\d\d$',
                                        message.text)  # В формате +7 (908) 190-54-26 и похожих
    if check_phone_regular1 or check_phone_regular2:
        change_user_phone(message)
        change_user_condition(message, "main_menu")
        await message.reply_text(CHANGE_PHONE_SUCCESS_MESSAGE)
    else:
        await message.reply_text(text=PHONE_ERROR_MESSAGE)


@Client.on_message(filters.text & filters.private & condition_is('change_call_phone_settings') & is_user_banned)
async def change_call_phone_settings(bot: Client, message: Message):
    check_phone_regular1 = re.fullmatch('^((\+7)([0-9]){10})$', message.text)  # Слитно
    check_phone_regular2 = re.fullmatch('^\+7 ?\(\d{3}\) ?\d\d\d[- .]\d\d[- .]\d\d$',
                                        message.text)  # В формате +7 (908) 190-54-26 и похожих
    if check_phone_regular1 or check_phone_regular2:
        change_user_phone(message)
        change_user_condition(message, "main_menu")
        await message.reply_text(CHANGE_PHONE_SUCCESS_MESSAGE)
        phone: str = check_user_phone(message.from_user.id)
        await message.reply_text(text=confirm_phone_number(phone), reply_markup=call_me_keyboard)
    else:
        await message.reply_text(text=PHONE_ERROR_MESSAGE)
