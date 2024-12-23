from typing import Any
from telebot.types import Message

from ..command import BaseCommand
from ..wg_config import Peer


class StartCommand(BaseCommand):
    def __init__(self, bot: Any):
        super().__init__(bot)

        @self.client.message_handler(commands=["start"])
        async def start(message: Message) -> None:
            await self._start(message)

        @self.client.message_handler(commands=["new"])
        async def new(message: Message) -> None:
            await self._new(message)

    async def _start(self, message: Message) -> None:
        if not self.config.administrators_ids:
            self.config.administrators_ids.append(message.from_user.id)
            self.config.commit()
        await self.bot.client.send_message(message.chat.id, "Welcome to VPN Bot!")

    async def _new(self, message: Message) -> None:
        if self._check_admin_status(message):
            message = await self.client.send_message(
                message.chat.id,
                "Creating new peer...",
            )
            new_peer = self.wg0.new_peer()  # type: Peer
            new_peer()
            self.wg0.update()

            await self.client.send_document(
                message.chat.id,
                self._peer2file(new_peer),
                caption="Here is your new peer!",
                visible_file_name="peer.txt",
            )

            await self.client.send_photo(
                message.chat.id,
                self._peer2qr(new_peer),
                caption="Here is your new peer qr!",
            )
            await self.client.delete_message(message.chat.id, message.message_id)
            return
        await self.client.send_message(
            message.chat.id,
            "You are not an administrator!",
        )
