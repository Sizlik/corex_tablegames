from threading import Thread

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from message.models import Message, Button
from message.serializers import MessageSerializer, ButtonSerializer
from telegram.services.sender import TelegramSender


# Create your views here.

class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        # print(serializer.instance)
        serializer.save()
        Thread(target=TelegramSender(serializer.instance).send_all_users).start()


class ButtonViewSet(ModelViewSet):
    queryset = Button.objects.all()
    serializer_class = ButtonSerializer
