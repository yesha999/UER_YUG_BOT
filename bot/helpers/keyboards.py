from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("📛 Оставить заявку", callback_data="app"),
    InlineKeyboardButton("📞 Связаться", callback_data="communicate")],
    [InlineKeyboardButton("⚙ Настройки", callback_data="settings")],
    [InlineKeyboardButton("☎ Полезные контакты", callback_data="contacts")]])

app_menu_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("📛 Оставить заявку", callback_data="confirm_app"),
    InlineKeyboardButton("💡 Поделиться предложением", callback_data="offer")],
    [InlineKeyboardButton("🔙 Назад", callback_data="back")]])

skip_back_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("▶ Пропустить", callback_data="skip")],
    [InlineKeyboardButton("🔙 Назад", callback_data="back")]])

back_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 Назад", callback_data="back")]])

user_settings_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("🛠 Поменять имя", callback_data="change_name"),
    InlineKeyboardButton("🛠 Сменить номер", callback_data="change_phone")],
    [InlineKeyboardButton("🔙 Назад", callback_data="back")]])

communicate_method_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("📞 Перезвоните мне", callback_data="call_me")],
    [InlineKeyboardButton("📞 Свяжитесь со мной в чат-боте", callback_data="chat_me")],
    [InlineKeyboardButton("🔙 Назад", callback_data="back")]
])

call_me_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("✅ Да", callback_data="confirm_call"),
    InlineKeyboardButton("🛠 Изменить номер телефона", callback_data="change_call_phone")]])

end_dialog_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("❌📞 Завершить диалог", callback_data="end_dialog")]])

admin_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("✉ Выполнить рассылку", callback_data="mailing"),
    InlineKeyboardButton("👥 Найти пользователя", callback_data="check_user")],
    [InlineKeyboardButton("🔙 Вернуться в главное меню", callback_data="back_menu")]
])

unban_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("▶✅Разбанить", callback_data="unban_user")]
])

ban_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("⛔❌Забанить", callback_data="ban_user")]
])
