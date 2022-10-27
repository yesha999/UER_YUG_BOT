import sqlite3
from sqlite3 import Cursor

from pyrogram.types import Message

from bot.db.database import database


def data_base_connection() -> Cursor:
    try:
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        print('База не работает')

    return cursor


def check_user_is_registered(message: Message) -> bool:
    """
    Проверка для /start, чтобы не просить имя и телефон повторно
    """
    cursor = data_base_connection()

    select_query = f"""
    SELECT is_registered from user WHERE tg_id={message.from_user.id}
    """
    cursor.execute(select_query)
    records = cursor.fetchone()
    try:
        is_registered = records[0]
    except:
        is_registered = False  # Если пользователь не найден, будет false

    cursor.close()
    return is_registered


def check_user_condition(message: Message) -> str:
    """
    Проверка состояния пользователя
    """
    cursor = data_base_connection()

    select_query = f"""
        SELECT bot_condition from user WHERE tg_id={message.from_user.id}
        """
    cursor.execute(select_query)
    records = cursor.fetchone()
    try:
        bot_condition = records[0]
    except:
        bot_condition = "change_name"  # Если пользователь не найден, будет стартовое состояние (изменение имени)

    cursor.close()
    return bot_condition


def check_user_info(user_id) -> dict:
    cursor = data_base_connection()

    select_query = f"""
        SELECT tg_id, tg_username, full_name, phone
         from user WHERE tg_id={user_id}
        """
    cursor.execute(select_query)
    r = cursor.fetchone()
    user_info = {"tg_id": r[0], "tg_username": r[1], "full_name": r[2], "phone": r[3]}
    cursor.close()
    return user_info


def check_user_situation(message: Message) -> dict:
    cursor = data_base_connection()

    select_query = f"""
        SELECT tg_id, tg_username, full_name, phone, situation_address, situation_media, situation_description
         from user WHERE tg_id={message.from_user.id}
        """
    cursor.execute(select_query)
    r = cursor.fetchone()
    user_situation_info = {"tg_id": r[0], "tg_username": r[1], "full_name": r[2], "phone": r[3],
                           "situation_address": r[4], "situation_media": r[5],
                           "situation_description": r[6]}
    cursor.close()
    return user_situation_info


def check_user_phone(user_id) -> str:
    cursor = data_base_connection()

    select_query = f"""
        SELECT phone from user WHERE tg_id={user_id}
        """
    cursor.execute(select_query)
    r = cursor.fetchone()
    phone = r[0]
    cursor.close()
    return phone


def check_user_is_admin(user_id) -> bool:
    cursor = data_base_connection()

    select_query = f"""
        SELECT is_admin from user WHERE tg_id={user_id}
        """
    cursor.execute(select_query)
    r = cursor.fetchone()
    if r:
        is_admin = r[0]
    else:
        is_admin = False
    cursor.close()
    return is_admin


def check_user_is_banned(user_id) -> bool:
    cursor = data_base_connection()

    select_query = f"""
        SELECT is_banned from user WHERE tg_id={user_id}
        """
    cursor.execute(select_query)
    r = cursor.fetchone()
    if r:
        is_banned = r[0]
    else:
        is_banned = False
    cursor.close()
    return is_banned


def select_all_users_id() -> list:
    cursor = data_base_connection()

    select_query = f"""
    SELECT tg_id from user"""
    cursor.execute(select_query)
    all_user_id = cursor.fetchall()
    cursor.close()
    return all_user_id


def select_all_users_info() -> list:
    cursor = data_base_connection()

    select_query = f"""
    SELECT tg_id, tg_username, full_name, phone from user"""
    cursor.execute(select_query)
    all_user_id = cursor.fetchall()
    cursor.close()
    return all_user_id
