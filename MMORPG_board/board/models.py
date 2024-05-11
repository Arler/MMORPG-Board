from django.db import models
from django.urls import reverse
from tinymce import models as tinymce_models


class Announcement(models.Model):
    CATEGORIES = [
        ('Танки', 'Танки'),
        ('Хилы', 'Хилы'),
        ('ДД', 'ДД'),
        ('Торговцы', 'Торговцы'),
        ('Гилдмастеры', 'Гилдмастеры'),
        ('Квестгиверы', 'Квестгиверы'),
        ('Кузнецы', 'Кузнецы'),
        ('Кожевники', 'Кожевники'),
        ('Зельевары', 'Зельевары'),
        ('Мастера заклинаний', 'Мастера заклинаний'),
    ]
    author = models.ForeignKey('subaccount_system.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    text = tinymce_models.HTMLField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=30, choices=CATEGORIES)
    active = models.BooleanField(default=True)


class UserResponse(models.Model):
    responder = models.ForeignKey('subaccount_system.User', on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    text = tinymce_models.HTMLField()
    accepted = models.BooleanField(default=False)
