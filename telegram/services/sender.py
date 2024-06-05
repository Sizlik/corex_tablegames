import asyncio

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.conf import settings

from notification.models import Notification
from user.models import User

from message.models import Message, Button


class TelegramSender:
    def __init__(self, message: Message):
        self.message = message
        self.buttons = Button.objects.filter(message=message)

    def send_all_users(self):
        users = list(User.objects.all())

        buttons = []
        if self.buttons:
            for button in self.buttons:
                buttons.append(InlineKeyboardButton(text=button.text, callback_data=button.callback_data))

        keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons]) if buttons else None

        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.send(users, keyboard))
        loop.close()

    async def send(self, users: list[User], keyboard):
        notifications = []
        for user in users:
            await self._send(user.telegram_id, self.message.message, keyboard)
            await Notification(user=user, message=self.message).asave()
            await asyncio.sleep(10)

        await Notification.objects.abulk_create(notifications, batch_size=2000)

    async def _send(self, chat_id, text, keyboard):
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        try:
            await bot.send_message(chat_id, text, reply_markup=keyboard)
        except Exception as e:
            print(e)
