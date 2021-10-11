#!/usr/bin/env python3
"""youtube bot dl"""

import os
import telebot
import validators
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('AUTH_TOKEN')
auth_users = os.getenv('AUTH_USERS').split()

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    high level support for doing this and that.
    """
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def download(message):
    """
    high level support for doing this and that.
    """
    if  (str(message.from_user.id) in auth_users) and (validators.url(message.text)) :
        bot.reply_to(message, 'Url is OK')
        os.system("echo Hello from the other side!")
    else:
        bot.reply_to(message, 'Error')

bot.infinity_polling()