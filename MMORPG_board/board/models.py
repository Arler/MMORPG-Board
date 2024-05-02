from django.db import models

from subaccount_system.models import User


class Announcement(models.Model):
    CATEGORIES = [
        ('Tanks', 'Танки'),
        ('Healers', 'Хилы'),
        ('DDs', 'ДД'),
        ('Merchants', 'Торговцы'),
        ('Guildmasters', 'Гилдмастеры'),
        ('Questgivers', 'Квестгиверы'),
        ('Blacksmiths', 'Кузнецы'),
        ('Leatherworkers', 'Кожевники'),
        ('Potions Masters', 'Зельевары'),
        ('Spellmasters', 'Мастера заклинаний'),
    ]
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=30, choices=CATEGORIES)
    active = models.BooleanField(default=True)


class UserResponse(models.Model):
    responder = models.OneToOneField(User, on_delete=models.CASCADE)
    announcement = models.OneToOneField(Announcement, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
