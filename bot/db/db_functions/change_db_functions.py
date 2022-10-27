import sqlite3

from pyrogram.types import Message

from bot.db.database import database


def change_user_name(message: Message):
    try:
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        pass

    change_user_full_name = (f"""
    INSERT INTO user (tg_id, tg_username, full_name) 
    VALUES ('{message.from_user.id}','{message.from_user.username}', '{message.text}')
    ON CONFLICT (tg_id) DO UPDATE SET tg_username='{message.from_user.username}', full_name='{message.text}'
    WHERE tg_id='{message.from_user.id}';
    """)  # Юзернейм тоже обновим, вдруг изменился
    cursor.execute(change_user_full_name)
    connection.commit()
    cursor.close()


def change_user_phone(message: Message):
    """
    Меняем номер телефона в базе, а также ставим отметку о том, что пользователь зарегистрирован.
    """
    try:
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        pass

    change_user_full_name = (f"""
    UPDATE user SET phone='{message.text}',  is_registered=TRUE
    WHERE tg_id='{message.from_user.id}';
    """)
    cursor.execute(change_user_full_name)
    connection.commit()
    cursor.close()


def change_situation_address(message: Message):
    """
    Сохраняем адрес последней заявки.
    """
    try:
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        pass

    change_last_situation_address = (f"""
    UPDATE user SET situation_address='{message.text}'
    WHERE tg_id='{message.from_user.id}';
    """)
    cursor.execute(change_last_situation_address)
    connection.commit()
    cursor.close()


def set_situation_address_null(message: Message):
    try:
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        pass

    change_last_situation_address = (f"""
    UPDATE user SET situation_address=NULL 
    WHERE tg_id='{message.chat.id}';
    """)
    cursor.execute(change_last_situation_address)
    connection.commit()
    cursor.close()


def change_situation_media(message: Message):
    """
    Сохраняем адрес последней заявки.
    """
    try:
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        pass

    if message.photo:
        change_last_situation_media = (f"""
        UPDATE user SET situation_media='{message.photo.file_id}'
        WHERE tg_id='{message.from_user.id}';
        """)
    elif message.video:
        change_last_situation_media = (f"""
        UPDATE user SET situation_media='{message.video.file_id}'
        WHERE tg_id='{message.from_user.id}';
        """)
    cursor.execute(change_last_situation_media)
    connection.commit()
    cursor.close()


def set_situation_media_null(message: Message):
    try:
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        pass

    change_last_situation_address = (f"""
    UPDATE user SET situation_media=NULL 
    WHERE tg_id='{message.chat.id}';
    """)
    cursor.execute(change_last_situation_address)
    connection.commit()
    cursor.close()


def set_situation_description_null(message: Message):
    try:
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        pass

    change_last_situation_address = (f"""
    UPDATE user SET situation_description=NULL 
    WHERE tg_id='{message.chat.id}';
    """)
    cursor.execute(change_last_situation_address)
    connection.commit()
    cursor.close()


def change_situation_description(message: Message):
    """
    Сохраняем описание последней заявки.
    """
    try:
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        pass
    if message.photo:
        change_last_situation_description = (f"""
        UPDATE user SET situation_description='{message.caption}'
        WHERE tg_id='{message.from_user.id}';
        """)
    else:
        change_last_situation_description = (f"""
        UPDATE user SET situation_description='{message.text}'
        WHERE tg_id='{message.from_user.id}';
        """)
    cursor.execute(change_last_situation_description)
    connection.commit()
    cursor.close()


def change_user_condition(message: Message, new_condition: str):
    try:
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        print('База не работает')

    update_user_condition = (f"""
    UPDATE user SET bot_condition='{new_condition}'
    WHERE tg_id='{message.chat.id}'
    """)

    cursor.execute(update_user_condition)
    connection.commit()
    cursor.close()


def ban_user(user_id):
    try:
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        print('База не работает')

    update_user_condition = (f"""
    UPDATE user SET is_banned=TRUE
    WHERE tg_id='{user_id}'
    """)

    cursor.execute(update_user_condition)
    connection.commit()
    cursor.close()


def unban_user(user_id):
    try:
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
    except sqlite3.Error as error:
        print('База не работает')

    update_user_condition = (f"""
    UPDATE user SET is_banned=FALSE
    WHERE tg_id='{user_id}'
    """)

    cursor.execute(update_user_condition)
    connection.commit()
    cursor.close()
