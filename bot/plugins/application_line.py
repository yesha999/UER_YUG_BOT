from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from bot.helpers.constants import REQUEST_CHANEL_ID
from bot.helpers.custom_filters import condition_is, is_user_banned
from bot.db.db_functions.change_db_functions import change_user_condition, change_situation_address, \
    change_situation_media, set_situation_address_null, set_situation_media_null, \
    change_situation_description, set_situation_description_null
from bot.db.db_functions.check_db_functions import check_user_situation
from bot.helpers.keyboards import app_menu_keyboard, skip_back_keyboard, back_keyboard
from bot.helpers.messages import REQUEST_MENU_MESSAGE, ADDRESS_MESSAGE, MEDIA_MESSAGE, MEDIA_ERROR_MESSAGE, DESCRIPTION_MESSAGE, \
    REQUEST_THANK_YOU_MESSAGE, request_chat_message


@Client.on_message(filters.text & filters.private & condition_is('address') & is_user_banned)
async def problem_address(bot: Client, message: Message):
    change_user_condition(message, "problem_media")
    change_situation_address(message)
    await message.reply_text(MEDIA_MESSAGE, reply_markup=skip_back_keyboard)


@Client.on_callback_query(condition_is('address') & is_user_banned)
async def skip_address(bot: Client, answer_message: CallbackQuery):
    data = answer_message.data
    if data == "skip":
        change_user_condition(answer_message.message, "problem_media")
        set_situation_address_null(answer_message.message)
        await answer_message.message.reply_text(MEDIA_MESSAGE,
                                                reply_markup=skip_back_keyboard)
    if data == "back":
        change_user_condition(answer_message.message, "main_menu")
        await answer_message.message.reply_text(
            text=REQUEST_MENU_MESSAGE,
            reply_markup=app_menu_keyboard)


@Client.on_message(filters.private & condition_is('problem_media') & is_user_banned)
async def problem_media(bot: Client, message: Message):
    if message.photo or message.video:
        change_user_condition(message, "problem_description")
        change_situation_media(message)
        await message.reply_text(DESCRIPTION_MESSAGE, reply_markup=back_keyboard)
    else:
        await message.reply_text(MEDIA_ERROR_MESSAGE)


@Client.on_callback_query(condition_is('problem_media') & is_user_banned)
async def skip_media(bot: Client, answer_message: CallbackQuery):
    data = answer_message.data
    if data == "skip":
        change_user_condition(answer_message.message, "problem_description")
        set_situation_media_null(answer_message.message)
        await answer_message.message.reply_text(DESCRIPTION_MESSAGE,
                                                reply_markup=back_keyboard)
    if data == "back":
        change_user_condition(answer_message.message, "address")
        await answer_message.message.reply_text(text=ADDRESS_MESSAGE,
                                                reply_markup=skip_back_keyboard)


@Client.on_message(filters.text & filters.private & condition_is('problem_description') & is_user_banned)
async def problem_description(bot: Client, message: Message):
    change_user_condition(message, "main_menu")
    change_situation_description(message)
    await message.reply_text(REQUEST_THANK_YOU_MESSAGE)
    user_situation_info: dict = check_user_situation(message)
    if user_situation_info["situation_media"]:
        try:
            await bot.send_photo(REQUEST_CHANEL_ID, user_situation_info["situation_media"],
                                 caption=request_chat_message(user_situation_info["tg_username"],
                                                              user_situation_info["full_name"],
                                                              user_situation_info["phone"],
                                                              user_situation_info["situation_address"],
                                                              user_situation_info["situation_description"]))
        except ValueError as e:
            await bot.send_video(REQUEST_CHANEL_ID, user_situation_info["situation_media"],
                                 caption=request_chat_message(user_situation_info["tg_username"],
                                                              user_situation_info["full_name"],
                                                              user_situation_info["phone"],
                                                              user_situation_info["situation_address"],
                                                              user_situation_info["situation_description"]))
    else:
        await bot.send_message(REQUEST_CHANEL_ID,
                               text=request_chat_message(user_situation_info["tg_username"],
                                                         user_situation_info["full_name"],
                                                         user_situation_info["phone"],
                                                         user_situation_info["situation_address"],
                                                         user_situation_info[
                                                             "situation_description"]))
    # После отправки обнулим значения в базе данных
    set_situation_media_null(message)
    set_situation_address_null(message)
    set_situation_description_null(message)


@Client.on_callback_query(condition_is('problem_description') & is_user_banned)
async def back_to_media(bot: Client, answer_message: CallbackQuery):
    data = answer_message.data
    if data == "back":
        change_user_condition(answer_message.message, "problem_media")
        await answer_message.message.reply_text(text=MEDIA_MESSAGE,
                                                reply_markup=skip_back_keyboard)
