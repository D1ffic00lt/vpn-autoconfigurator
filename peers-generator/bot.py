from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

from utils import (
    BotConfig,
    WG0,
    StartCommand,
    SettingsCommand
)


class VPNBot(object):
    def __init__(self, token: str, config: BotConfig, wg0: WG0):
        self.client = AsyncTeleBot(token, state_storage=StateMemoryStorage())
        self.client.add_custom_filter(asyncio_filters.StateFilter(self.client))
        self.config = config
        self.wg0 = wg0

        self.start_command = StartCommand(self)
        self.settings_command = SettingsCommand(self)

    async def run(self, *args, **kwargs):
        print("PROGRAM STARTED")
        await self.client.infinity_polling(*args, **kwargs)
