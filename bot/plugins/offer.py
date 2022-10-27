from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from bot.helpers.constants import REQUEST_CHANEL_ID
from bot.helpers.custom_filters import condition_is, is_user_banned
from bot.db.db_functions.change_db_functions import change_user_condition, change_situation_media, \
    set_situation_media_null, \
    change_situation_description, set_situation_description_null
from bot.db.db_functions.check_db_functions import check_user_situation
from bot.helpers.keyboards import app_menu_keyboard
from bot.helpers.messages import REQUEST_MENU_MESSAGE, OFFER_THANKS, offer_chat_message


@Client.on_message((filters.text | filters.photo) & filters.private & condition_is('offer') & is_user_banned)
async def user_offer(bot: Client, message: Message):
    change_user_condition(message, "main_menu")
    change_situation_description(message)
    if message.photo:
        change_situation_media(message)
    await message.reply_text(OFFER_THANKS)

    user_situation_info: dict = check_user_situation(message)
    if user_situation_info["situation_media"]:
        await bot.send_photo(REQUEST_CHANEL_ID, user_situation_info["situation_media"],
                             caption=offer_chat_message(user_situation_info["tg_username"],
                                                        user_situation_info["full_name"],
                                                        user_situation_info["phone"],
                                                        user_situation_info["situation_description"]))

    else:
        await bot.send_message(REQUEST_CHANEL_ID,
                               text=offer_chat_message(user_situation_info["tg_username"],
                                                       user_situation_info["full_name"],
                                                       user_situation_info["phone"],
                                                       user_situation_info[
                                                           "situation_description"]))
    # После отправки обнулим значения в базе данных
    set_situation_media_null(message)
    set_situation_description_null(message)


@Client.on_callback_query(condition_is('offer') & is_user_banned)
async def back_from_offer(bot: Client, answer_message: CallbackQuery):
    data = answer_message.data
    if data == "back":
        change_user_condition(answer_message.message, "main_menu")
        await answer_message.message.reply_text(
            text=REQUEST_MENU_MESSAGE,
            reply_markup=app_menu_keyboard)
