import os
import asyncio

from utils import BotConfig, WG0
from bot import VPNBot

with open(os.environ.get('TOKEN')) as token_file:
    token = token_file.read().strip()

with BotConfig("./config") as config:
    wg0 = WG0("./config")
    bot = VPNBot(token, config, wg0)
    asyncio.run(bot.run())
