import asyncio

from aiogram import Bot
from aiogram.types import Update
from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from telegram.services.dispatcher import dispatcher


# Create your views here.

class TelegramCallbackViewSet(GenericViewSet):

    @action(methods=['POST'], detail=False)
    def webhook(self, request, *args, **kwargs):
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        update = Update(**request.data)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(dispatcher.feed_update(bot, update))
        loop.close()
        return Response(status=status.HTTP_200_OK)
