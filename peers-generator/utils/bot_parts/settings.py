from typing import Any
from telebot.types import Message

from ..command import BaseCommand


class SettingsCommand(BaseCommand):
    def __init__(self, bot: Any):
        super().__init__(bot)

        @self.client.message_handler(commands=["restart"])
        async def restart(message: Message) -> None:
            await self._restart(message)

    async def _restart(self, message: Message) -> None:
        if self._check_admin_status(message):
            message = await self.client.send_message(
                message.chat.id,
                "Restarting WireGuard...",
            )
            self.wg0.restart()
            await self.client.send_message(message.chat.id, "WireGuard restarted!")
            await self.client.delete_message(message.chat.id, message.message_id)
            return
        await self.client.send_message(
            message.chat.id,
            "You are not an administrator!",
        )
