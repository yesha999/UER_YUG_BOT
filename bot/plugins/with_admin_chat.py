from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from bot.helpers.constants import ADMIN_CHANEL_ID
from bot.helpers.custom_filters import condition_is, is_user_banned
from bot.db.db_functions.change_db_functions import change_user_condition
from bot.db.db_functions.check_db_functions import check_user_info
from bot.helpers.keyboards import main_menu_keyboard
from bot.helpers.messages import chat_with_user_message, WELCOME_MESSAGE, chat_with_user_end_message


@Client.on_message(filters.text & filters.private &
                   (condition_is('chat_with_admin') | condition_is(
                       'chat_with_admin1')) & is_user_banned)  # Два состояния для отправки первого и последующих сообщений
async def chat_with_admin(bot: Client, message: Message):
    user_info = check_user_info(message.from_user.id)
    change_user_condition(message, "chat_with_admin1")  # Меняем состояние после 1го сообщения
    await bot.send_message(ADMIN_CHANEL_ID,
                           text=chat_with_user_message(user_info["tg_username"],
                                                       user_info["full_name"], user_info["tg_id"], message.text))


@Client.on_message(filters.text & filters.group & filters.reply & is_user_banned)
async def admin_answer(bot: Client, message: Message):
    user_id = message.reply_to_message.text.split()[1:2][0]  # В нашем сообщении id будет всегда вторым словом
    await bot.send_message(chat_id=user_id, text=message.text)


@Client.on_callback_query(condition_is('chat_with_admin1') & is_user_banned)
async def end_chat_with_admin1(bot: Client, answer_message: CallbackQuery):
    """
    Если хотя бы одно сообщение было отправлено, отправим в нашу админ группу что диалог завершен.
    """
    change_user_condition(answer_message.message, "main_menu")
    await answer_message.answer("❌📞Диалог с администратором завершен...")
    await answer_message.message.reply_text(text=WELCOME_MESSAGE, reply_markup=main_menu_keyboard)
    user_info = check_user_info(answer_message.message.chat.id)
    await bot.send_message(ADMIN_CHANEL_ID,
                           text=chat_with_user_end_message(user_info["tg_username"],
                                                           user_info["full_name"]))


@Client.on_callback_query(condition_is('chat_with_admin') & is_user_banned)
async def end_chat_with_admin(bot: Client, answer_message: CallbackQuery):
    change_user_condition(answer_message.message, "main_menu")
    await answer_message.answer("❌📞Диалог с администратором завершен...")
    await answer_message.message.reply_text(text=WELCOME_MESSAGE, reply_markup=main_menu_keyboard)
