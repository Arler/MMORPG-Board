from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.cache import cache
from django import forms

from .models import User


class CustomSignupForm(SignupForm):
	send_news = forms.BooleanField(label='Присылать новости')

	def save(self, request):
		user = super(CustomSignupForm, self).save(request)
		user.send_news = self.cleaned_data['send_news']
		return user


class OneTimeCodeForm(forms.Form):
	username = forms.CharField(max_length=150)
	code = forms.CharField(max_length=16, label='Код')

	def clean(self):
		cleaned_data = super().clean()
		username = cleaned_data.get('username')
		code = cleaned_data.get('code')
		cache_code = cache.get(f'one_time_code_username-{username}', None)

		if User.objects.filter(username=username).exists() and cache_code == code:
			user = User.objects.get(username=username)
			common_users = Group.objects.get(name="Обычные пользователи")
			user.groups.add(common_users)
			return cleaned_data
		else:
			raise ValidationError('Имя пользователя или код введены неправильно')
