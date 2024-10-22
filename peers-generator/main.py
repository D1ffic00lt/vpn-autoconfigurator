import os
import telebot

from utils import *

telebot = telebot.TeleBot(token=os.environ['TELEGRAM_TOKEN'])

path = "/config" if os.path.exists("/config") else "./config"
config = WG0(path)

@telebot.message_handler(commands=['start', 'new'])
def start(message):
    new_peer = config.new_peer()
    new_peer()
    telebot.send_message(message.chat.id, new_peer.wg_peer)
    config.update()

if __name__ == '__main__':
    print("STARTING BOT")
    telebot.polling(non_stop=True)
