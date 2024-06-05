from django.db import models

from core.models import BaseModel


# Create your models here.
class Button(BaseModel):
    text = models.TextField()
    callback_data = models.TextField()


class Message(BaseModel):
    message = models.TextField()
    max_actions = models.IntegerField(null=True)
    buttons = models.ManyToManyField(Button)





