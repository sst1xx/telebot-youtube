"""
YouTube Download Bot
"""

import os
import telebot
import validators
import yt_dlp
from threading import Thread
from queue import Queue

# Read environment variables directly
TOKEN = os.environ.get('AUTH_TOKEN')
AUTH_USERS = os.environ.get('AUTH_USERS', '').split()  # List of authorized user IDs as strings

print('Bot is starting...')
bot = telebot.TeleBot(TOKEN)

# Queue to handle downloads
download_queue = Queue()

def process_download_queue():
    while True:
        url, chat_id = download_queue.get()
        try:
            bot.send_message(chat_id, "Starting download...")
            ydl_opts = {
                'format': 'bestaudio/best',
                'addmetadata': True,
                'quiet': True,
                'outtmpl': 'youtube/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '128',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            bot.send_message(chat_id, "Download completed!")
        except Exception as e:
            bot.send_message(chat_id, f"Error during download: {e}")
        download_queue.task_done()

# Start a background thread for processing the download queue
Thread(target=process_download_queue, daemon=True).start()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Send me a YouTube link to download the audio.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = str(message.from_user.id)
    url = message.text
    if user_id in AUTH_USERS and validators.url(url):
        bot.reply_to(message, "URL is valid. Adding to the download queue...")
        download_queue.put((url, message.chat.id))
    else:
        bot.reply_to(message, "Invalid URL or you are not authorized to use this bot.")

bot.infinity_polling()
