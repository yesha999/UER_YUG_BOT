from pyrogram import filters
from pyrogram.types import Message

from bot.db.db_functions.check_db_functions import check_user_condition, check_user_is_admin, check_user_is_banned


def condition_is(condition: str):
    """
    Динамический фильтр на текущее состояние пользователя
    """

    async def condition_is_some(_, __, message: Message) -> bool:
        bot_condition = check_user_condition(message)
        return bot_condition == condition

    return filters.create(condition_is_some)


async def is_admin_filter(_, __, message: Message) -> bool:
    """
    Проверка на администратора
    """
    is_admin: bool = check_user_is_admin(message.from_user.id)
    return is_admin


admin_filter = filters.create(is_admin_filter)


async def is_user_banned(_, __, message: Message) -> bool:
    """
    Проверка на бан
    """
    is_banned: bool = check_user_is_banned(message.from_user.id)
    return not is_banned  # Если пользователь забанен (True), нужно вернуть False

is_user_banned = filters.create(is_user_banned)