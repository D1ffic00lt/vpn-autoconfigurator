import asyncio

from typing import Any
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from ..command import BaseCommand
from ..wg_config import Peer

class Validator(BaseCommand):
    def __init__(self, bot: Any):
        super().__init__(bot)

        @self.client.message_handler(content_types=["photo", "document"])
        async def validate(message: Message):
            await self._validate(message)

        @self.client.callback_query_handler(func=lambda call: True)
        async def handle_query(call: CallbackQuery):
            await self._handle(call)

    async def _validate(self, message: Message):
        for administrator_id in self.config.administrators_ids:
            markup = InlineKeyboardMarkup()
            accept = InlineKeyboardButton(
                "Accept", callback_data=f'accept_{message.from_user.id}'
            )
            reject = InlineKeyboardButton(
                "Reject", callback_data=f'reject_{message.from_user.id}'
            )
            markup.add(accept, reject)

            await self.client.forward_message(
                chat_id=administrator_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            await self.client.send_message(
                chat_id=administrator_id,
                text=f"New request from @{message.from_user.username}",
                reply_markup=markup
            )
            await asyncio.sleep(1)

        await self.client.reply_to(
            message, "Your receipt has been forwarded to the administrators!"
        )

    async def _handle(self, call: CallbackQuery):

        if call.data.startswith("accept"):
            client_id = int(call.data.split("accept_")[1])

            new_peer = self.wg0.new_peer()  # type: Peer
            new_peer()

            await self.client.send_document(
                client_id, self._peer2file(new_peer),
                caption="Here is your new peer!",
                visible_file_name="peer.txt"
            )

            await self.client.send_photo(
                client_id, self._peer2qr(new_peer),
                caption="Here is your new peer qr!"
            )
            await self.client.send_message(call.message.chat.id, "Authorisation data has been sent.")
            await self.client.answer_callback_query(call.id)
        elif call.data.startswith("reject"):
            client_id = int(call.data.split("reject_")[1])
            await self.client.send_message(call.message.chat.id, "Rejected")
            await self.client.send_message(client_id, "Your request has been rejected.")
            await self.client.answer_callback_query(call.id)
