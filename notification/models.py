from django.db import models

from core.models import BaseModel


# Create your models here.

class Notification(BaseModel):
    class ActionType(models.TextChoices):
        ACCEPT = 'ACCEPT'
        DECLINE = 'DECLINE'

    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey('message.Message', on_delete=models.CASCADE, related_name='notifications')
    action = models.CharField(choices=ActionType.choices, null=True)

