from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel


class UserManager(BaseUserManager):

    def create_superuser(self, email, first_name, last_name, phone, password):
        user = User.objects.create(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            is_superuser=True,
            is_staff=True
        )
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser, BaseModel):
    username = models.CharField(null=True, unique=True, max_length=150)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    telegram_id = models.CharField(max_length=255, null=True)
    objects = UserManager()

    REQUIRED_FIELDS = ['telegram_id']
    USERNAME_FIELD = 'username'
    groups = None
    user_permissions = None

    class Meta:
        ordering = ['id']
