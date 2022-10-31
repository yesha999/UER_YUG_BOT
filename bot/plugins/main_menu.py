from pyrogram import Client
from pyrogram.types import CallbackQuery

from bot.helpers.constants import REQUEST_CHANEL_ID
from bot.helpers.custom_filters import condition_is, is_user_banned
from bot.db.db_functions.change_db_functions import change_user_condition
from bot.db.db_functions.check_db_functions import check_user_phone, check_user_info
from bot.helpers.keyboards import main_menu_keyboard, app_menu_keyboard, skip_back_keyboard, back_keyboard, \
    user_settings_keyboard, communicate_method_keyboard, call_me_keyboard, end_dialog_keyboard, reply_markup_keyboard
from bot.helpers.messages import WELCOME_MESSAGE, REQUEST_MENU_MESSAGE, ADDRESS_MESSAGE, OFFER_MESSAGE, CONTACTS, \
    SETTINGS_MESSAGE, CHANGE_NAME_MESSAGE, CHANGE_PHONE_MESSAGE, CHOOSE_COMMUNICATE_METHOD_MESSAGE, \
    confirm_phone_number, DISPATCHER_WILL_CALL_MESSAGE, please_call_message, DISPATCHER_CHAT_MESSAGE


@Client.on_callback_query(condition_is('main_menu') & is_user_banned)
async def main_menu_callback(bot: Client, answer_message: CallbackQuery):
    if answer_message.data == 'app':
        await answer_message.message.reply_text(text=REQUEST_MENU_MESSAGE,
                                                reply_markup=app_menu_keyboard)

    elif answer_message.data == 'confirm_app':
        change_user_condition(answer_message.message, "address")
        await answer_message.message.reply_text(
            text=ADDRESS_MESSAGE, reply_markup=skip_back_keyboard)

    elif answer_message.data == 'offer':
        change_user_condition(answer_message.message, "offer")
        await answer_message.message.reply_text(
            text=OFFER_MESSAGE, reply_markup=back_keyboard)

    elif answer_message.data == 'back':
        await answer_message.message.reply_text(
            text=WELCOME_MESSAGE, reply_markup=main_menu_keyboard)

    elif answer_message.data == 'contacts':
        await answer_message.message.reply_text(CONTACTS, reply_markup=reply_markup_keyboard)

    elif answer_message.data == 'settings':
        await answer_message.message.reply_text(SETTINGS_MESSAGE, reply_markup=user_settings_keyboard)

    elif answer_message.data == 'change_name':
        change_user_condition(answer_message.message, "change_name_settings")
        await answer_message.message.reply_text(text=CHANGE_NAME_MESSAGE, reply_markup=reply_markup_keyboard)

    elif answer_message.data == 'change_phone':
        change_user_condition(answer_message.message, "change_phone_settings")
        await answer_message.message.reply_text(text=CHANGE_PHONE_MESSAGE, reply_markup=reply_markup_keyboard)

    elif answer_message.data == 'communicate':
        await answer_message.message.reply_text(text=CHOOSE_COMMUNICATE_METHOD_MESSAGE,
                                                reply_markup=communicate_method_keyboard)

    elif answer_message.data == 'call_me':
        phone: str = check_user_phone(answer_message.message.chat.id)
        await answer_message.message.reply_text(text=confirm_phone_number(phone), reply_markup=call_me_keyboard)

    elif answer_message.data == 'change_call_phone':
        change_user_condition(answer_message.message, "change_call_phone_settings")
        await answer_message.message.reply_text(text=CHANGE_PHONE_MESSAGE)

    elif answer_message.data == 'confirm_call':
        await answer_message.message.reply_text(text=DISPATCHER_WILL_CALL_MESSAGE)
        user_info = check_user_info(answer_message.message.chat.id)
        await bot.send_message(REQUEST_CHANEL_ID,
                               text=please_call_message(user_info["tg_username"],
                                                        user_info["full_name"],
                                                        user_info["phone"]))

    elif answer_message.data == 'chat_me':
        change_user_condition(answer_message.message,
                              "chat_with_admin")
        await answer_message.message.reply_text(text=DISPATCHER_CHAT_MESSAGE, reply_markup=end_dialog_keyboard)
