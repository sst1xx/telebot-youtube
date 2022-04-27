#!/usr/bin/env python3
"""youtube bot dl"""

from __future__ import unicode_literals
from dotenv import load_dotenv

import os
import telebot
import validators
import youtube_dl


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
        ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': '/home/syncthing/youtube/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])

    else:
        bot.reply_to(message, 'Error')

bot.infinity_polling()
