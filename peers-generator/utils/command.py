import io
import qrcode

from typing import Any
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot

from .config import BotConfig
from .wg_config import Peer

class BaseCommand(object):
    def __init__(self, bot: Any):
        self.bot = bot
        self.config: BotConfig = bot.config
        self.wg0 = bot.wg0
        self.client: AsyncTeleBot = bot.client
        # type of the self.bot.client is AsyncTeleBot

    def _check_admin_status(self, message: Message):
        return message.from_user.id in self.config.administrators_ids

    @staticmethod
    def _peer2qr(peer: Peer) -> io.BytesIO:
        peer_qr_code = qrcode.make(peer.wg_peer)
        img_byte_arr = io.BytesIO()
        peer_qr_code.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr

    @staticmethod
    def _peer2file(peer: Peer) -> io.BytesIO:
        file = io.BytesIO()
        file.write(peer.wg_peer.encode('utf-8'))
        file.seek(0)
        return file