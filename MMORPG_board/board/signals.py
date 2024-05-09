from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives

from .models import UserResponse


@receiver(post_save, sender=UserResponse)
def send_response_notification(instance, created, **kwargs):
	if created:
		subject = 'На ваше объявление откликнулись'
		text_message = f'Пользователь {instance.responder} откликнулся на ваше объявление: http://127.0.0.1:8000/{instance.announcement.id}'
		html_message = (
			f'Пользователь {instance.responder} откликнулся на ваше <a href="http://127.0.0.1:8000/{instance.announcement.id}">'
			f'объявление</a>'
		)
		user_email = instance.announcement.author.email
		msg = EmailMultiAlternatives(subject=subject, body=text_message, from_email=None, to=[user_email, ])
		msg.attach_alternative(html_message, 'text/html')
		msg.send()
	elif instance.accepted:
		subject = 'Ваш отклик приняли'
		text_message = f'Ваш отклик на объявлении http://127.0.0.1:8000/{instance.announcement.id} был принят'
		html_message = (
			f'Ваш отклик на <a href="http://127.0.0.1:8000/{instance.announcement.id}">объявлении</a> был принят'
		)
		user_email = instance.responder.email
		msg = EmailMultiAlternatives(subject=subject, body=text_message, from_email=None, to=[user_email, ])
		msg.attach_alternative(html_message, 'text/html')
		msg.send()
