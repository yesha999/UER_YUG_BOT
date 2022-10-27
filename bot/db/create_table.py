import sqlite3

from bot.db.database import database

with sqlite3.connect(database) as connection:
    cursor = connection.cursor()

create_user_table = ("""CREATE TABLE IF NOT EXISTS user
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  tg_id VARCHAR (20) NOT NULL UNIQUE, 
  tg_username VARCHAR (100) NOT NULL,
  full_name VARCHAR (100) NOT NULL,
  phone VARCHAR (18),
  is_banned BOOLEAN DEFAULT (FALSE),
  is_active BOOLEAN DEFAULT (TRUE),
  is_registered BOOLEAN DEFAULT (FALSE),
  is_admin BOOLEAN DEFAULT (FALSE),
  bot_condition VARCHAR (20) DEFAULT ('change_name'),
  situation_address VARCHAR (100),
  situation_media VARCHAR (100),
  situation_description VARCHAR (500)
  )
  """)  # Последние три поля нужны для запоминания сущностей из заявок/предложений
cursor.execute(create_user_table)

cursor.close()
