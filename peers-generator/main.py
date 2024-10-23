import os
import telebot

from utils import *

with open(os.environ.get('TOKEN')) as token_file:
    token = token_file.read().strip()

telebot = telebot.TeleBot(token=token)

path = "/config" if os.path.exists("/config") else "./config"
config = WG0(path)

@telebot.message_handler(commands=['start', 'new'])
def start(message):
    new_peer = config.new_peer()
    new_peer()

    config.update()
    
    telebot.send_message(message.chat.id, new_peer.wg_peer)

if __name__ == '__main__':
    print("STARTING BOT")
    telebot.polling(non_stop=True)
