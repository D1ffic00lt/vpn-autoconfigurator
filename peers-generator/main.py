import os
import asyncio

from utils import BotConfig, WG0
from bot import VPNBot

os.environ["TOKEN"] = "../secrets/telegram-token.txt"
os.environ["PUID"]= "1000"
os.environ["PGID"] = "1000"
os.environ["TZ"] = "Europe/Moscow"
os.environ["SERVERURL"] = "109.172.94.36"
os.environ["SERVERPORT"] = "51820"
os.environ["PEERS"] = "0"
os.environ["PEERDNS"] = "true"
os.environ["INTERNAL_SUBNET"] = "10.13.13.0"

with open(os.environ.get('TOKEN')) as token_file:
    token = token_file.read().strip()

with BotConfig("./config") as config:
    wg0 = WG0("./config")
    bot = VPNBot(token, config, wg0)
    asyncio.run(bot.run())
