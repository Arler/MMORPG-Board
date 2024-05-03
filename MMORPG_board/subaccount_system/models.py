from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    send_news = models.BooleanField(default=False)
    authorized = models.BooleanField(default=False)
