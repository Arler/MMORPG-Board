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
		user.save()
		return user


class OneTimeCodeForm(forms.Form):
	code = forms.CharField(max_length=125, label='Код')

	def clean(self):
		cleaned_data = super().clean()
		code = cleaned_data.get('code')
		code = code.strip(' ')
		username = cache.get(code)

		if username:
			user = User.objects.get(username=username)
			common_users = Group.objects.get(name="Обычные пользователи")
			# Авторизация
			user.groups.add(common_users)
			user.authorized = True
			user.save()

			cache.delete(f'{code}')
			return cleaned_data
		else:
			raise ValidationError('Код введён неправильно')
