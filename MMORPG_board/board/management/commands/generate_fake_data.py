from django.core.management.base import BaseCommand
from faker import Faker
from board.models import Announcement, UserResponse
from subaccount_system.models import User
import random


class Command(BaseCommand):
    help = "Команда для генерации фейковых данных"

    def handle(self, *args, **options):
        faker = Faker(locale="ru-RU")
        users, announcements, user_responses = [], [], []
        rand = random.Random()

        # Генерация пользователей
        for i in range(10):
            password = "pepega123"
            username = faker.user_name().replace(' ', '')
            user = User.objects.create_user(password=password, username=username , email=faker.email())
            users.append(user)

        # Генерация постов
        for i in range(25):
            announcement = Announcement.objects.create(
                author=rand.choice(users),
                title=faker.text(rand.randint(10, 50)),
                text=faker.text(rand.randint(350, 800)),
                category=rand.choice(Announcement.CATEGORIES)[0],
                active=bool(rand.getrandbits(1))
                )
            announcements.append(announcement)

        # Генерация откликов
        for i in range(50):
            accpt = bool(rand.getrandbits(1))
            rejected = False
            if accpt is False:
                rejected = True
            user_response = UserResponse.objects.create(
                responder=rand.choice(users),
                announcement=rand.choice(announcements),
                text=faker.text(rand.randint(150, 500)),
                accepted=bool(rand.getrandbits(1)),
                rejected=rejected,
            )
            user_responses.append(user_response)

        # Сохранение
        for user in users:
            user.save()

        for announcement in announcements:
            announcement.save()

        for user_response in user_responses:
            user_response.save()