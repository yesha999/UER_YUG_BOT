import os

from pyrogram import Client

if __name__ == '__main__':
    plugins = dict(root="bot/plugins")
    bot = Client("UER_YUG_bot", api_id=int(os.getenv("API_ID")),
                 api_hash=os.getenv("API_HASH"), bot_token=os.getenv("BOT_TOKEN"), plugins=plugins)
    print("Я работаю")
    bot.run()
