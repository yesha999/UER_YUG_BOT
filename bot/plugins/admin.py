from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from bot.helpers.custom_filters import condition_is, admin_filter, is_user_banned
from bot.db.db_functions.change_db_functions import change_user_condition, ban_user, unban_user, give_user_admin
from bot.db.db_functions.check_db_functions import select_all_users_id, select_all_users_info, check_user_is_banned
from bot.helpers.keyboards import main_menu_keyboard, admin_keyboard, back_keyboard, ban_keyboard, unban_keyboard
from bot.helpers.messages import WELCOME_MESSAGE, WELCOME_ADMIN_PANEL_MESSAGE


@Client.on_message(filters.command("admin") & filters.private & admin_filter & is_user_banned)
async def admin_panel(bot: Client, message: Message):
    change_user_condition(message, "admin")
    await message.reply_text(WELCOME_ADMIN_PANEL_MESSAGE, reply_markup=admin_keyboard)


@Client.on_message(filters.text & filters.private & condition_is("admin_mail") & is_user_banned)
async def admin_mailing(bot: Client, message: Message):
    change_user_condition(message, "admin")
    all_user_id = select_all_users_id()  # Список кортежей с 1 значением - юзер id
    for user_id in all_user_id:
        await bot.send_message(user_id[0], message.text)
    await message.reply_text(WELCOME_ADMIN_PANEL_MESSAGE, reply_markup=admin_keyboard)


@Client.on_message(filters.text & filters.private & condition_is("check_user") & is_user_banned)
async def check_user(bot: Client, message: Message):
    all_users_info = select_all_users_info()
    users = []
    for user in all_users_info:
        if message.text in user:
            users.append(message.text)
            is_banned = check_user_is_banned(user[0])
            if is_banned:
                await message.reply_text(
                    f"id: <b>{user[0]}</b>\n username: <b>{user[1]}</b>\n"
                    f"Имя и Фамилия: <b>{user[2]}</b>\n Номер телефона: <b>{user[3]}</b>", reply_markup=unban_keyboard)
            else:
                await message.reply_text(
                    f"id: <b>{user[0]}</b> \n username: <b>{user[1]}</b>\n"
                    f"Имя и Фамилия: <b>{user[2]}</b>\n Номер телефона: <b>{user[3]}</b>", reply_markup=ban_keyboard)
    if not users:
        await message.reply_text("Пользователь не найден.")


@Client.on_callback_query(admin_filter & condition_is("admin_mail") & is_user_banned)
async def back_from_admin_mail(bot: Client, answer_message: CallbackQuery):
    if answer_message.data == "back":
        change_user_condition(answer_message.message, "admin")
        await answer_message.message.reply_text(WELCOME_ADMIN_PANEL_MESSAGE, reply_markup=admin_keyboard)
    if answer_message.data == "back_menu":
        change_user_condition(answer_message.message, "main_menu")
        await answer_message.message.reply_text(WELCOME_MESSAGE, reply_markup=main_menu_keyboard)


@Client.on_callback_query(admin_filter & condition_is("check_user") & is_user_banned)
async def check_user_callbacks(bot: Client, answer_message: CallbackQuery):
    if answer_message.data == "back":
        change_user_condition(answer_message.message, "admin")
        await answer_message.message.reply_text(WELCOME_ADMIN_PANEL_MESSAGE, reply_markup=admin_keyboard)
    if answer_message.data == "back_menu":
        change_user_condition(answer_message.message, "main_menu")
        await answer_message.message.reply_text(WELCOME_MESSAGE, reply_markup=main_menu_keyboard)
    if answer_message.data == "ban_user":
        user_id = answer_message.message.text.split()[1:2][0]  # Второе слово в тексте сообщения было юзер id
        ban_user(user_id)
        await answer_message.answer("⛔❌Пользователь заблокирован")
        await bot.send_message(user_id, "⛔❌Администратор Вас заблокировал")
    if answer_message.data == "unban_user":
        user_id = answer_message.message.text.split()[1:2][0]  # Второе слово в тексте сообщения было юзер id
        unban_user(user_id)
        await answer_message.answer("▶✅Пользователь разблокирован")
        await bot.send_message(user_id, "▶✅Администратор Вас разблокировал")
    if answer_message.data == "give_admin":
        user_id = answer_message.message.text.split()[1:2][0]  # Второе слово в тексте сообщения было юзер id
        give_user_admin(user_id)
        await answer_message.answer("▶✅Пользователь стал администратором")
        await bot.send_message(user_id, "▶✅Вы стали администратором")


@Client.on_callback_query(admin_filter & condition_is("admin") & is_user_banned)
async def admin_panel_callbacks(bot: Client, answer_message: CallbackQuery):
    if answer_message.data == "mailing":
        change_user_condition(answer_message.message, "admin_mail")
        await answer_message.message.reply_text("Введите текст рассылки:", reply_markup=back_keyboard)
    if answer_message.data == "back":
        await answer_message.message.reply_text(WELCOME_ADMIN_PANEL_MESSAGE, reply_markup=admin_keyboard)
    if answer_message.data == "back_menu":
        change_user_condition(answer_message.message, "main_menu")
        await answer_message.message.reply_text(WELCOME_MESSAGE, reply_markup=main_menu_keyboard)
    if answer_message.data == "check_user":
        change_user_condition(answer_message.message, "check_user")
        await answer_message.message.reply_text("Введите никнейм/id/Имя и Фамилию/номер телефона пользователя,"
                                                " и я напишу полную информацию, если такой пользователь есть в базе.\n"
                                                "В этом разделе также можно блокировать и"
                                                " разблокировать пользователей.",
                                                reply_markup=back_keyboard)
