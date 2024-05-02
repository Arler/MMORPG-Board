from django.core.mail import send_mail
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.core.cache import cache
import random
import string
import time


def create_one_time_code():
    code = ''
    random.seed(time.time())
    for _ in range(16):
        code += random.choice(string.ascii_letters)
    return code


@receiver(user_signed_up)
def send_one_time_code(user, **kwargs):
    code = create_one_time_code()
    cache.set(f'{code}', user.username)

    user_email = user.email
    subject = "Ваш одноразовый код для подтверждения аккаунта"
    message = f'Никому не сообщайте ваш одноразовый код!\nКод: {code}'
    send_mail(subject=subject, message=message, from_email=None, recipient_list=[user_email,])
