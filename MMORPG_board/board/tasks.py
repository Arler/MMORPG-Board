from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery import shared_task
from datetime import datetime, timedelta

from subaccount_system.models import User
from board.models import Announcement


@shared_task
def daily_announcements_email():
	user_emails = User.objects.filter(send_news=True).values_list('email', flat=True)

	current_date = datetime.now()
	one_day_ago = current_date - timedelta(days=1)
	announcements = Announcement.objects.filter(date_created__gte=one_day_ago)

	html_content = render_to_string(
		'board_app/daily_announcements.html',
		{
			'link': 'http://127.0.0.1:8000',
			'announcements': announcements
		}
	)

	for email in user_emails:
		msg = EmailMultiAlternatives(
			subject='Объявления за день',
			body='',
			from_email=None,
			to=[email]
		)
		msg.attach_alternative(html_content, 'text/html')
		msg.send()