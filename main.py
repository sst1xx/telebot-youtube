#!/usr/bin/env python3
"""youtube bot dl"""

import os
import subprocess
import telebot
import validators
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('AUTH_TOKEN')
auth_users = os.getenv('AUTH_USERS').split()
print ('TeleBot started')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    high level support for doing this and that.
    """
    bot.reply_to(message, "Send to me youtubr link for downloading")

@bot.message_handler(func=lambda message: True)
def download(message):
    """
    high level support for doing this and that.
    """
    if  (str(message.from_user.id) in auth_users) and (validators.url(message.text)) :
        bot.reply_to(message, 'Url is OK')

        try:
            subprocess.run("cd ~/youtube && youtube-dl --extract-audio --audio-format mp3 -c '" + \
            message.text + "'", shell=True, check=True, timeout=15, capture_output=True)
        except subprocess.CalledProcessError as e:
            # print(e)  # Output: Command 'exit 1' returned non-zero exit status 1.
            bot.reply_to(message, message.text + "could not be downloaded. Try to retry")

    else:
        bot.reply_to(message, 'URL is not correct or Anonymous user')

bot.infinity_polling()
