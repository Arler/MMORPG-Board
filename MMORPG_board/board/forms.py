from django.core.exceptions import ValidationError
from django import forms
from tinymce.widgets import TinyMCE

from .models import Announcement


class CreateAnnouncementForm(forms.ModelForm):
	text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

	class Meta:
		model = Announcement
		fields = [
			'title',
			'text',
			'category',
		]

	def clean(self):
		cleaned_data = super().clean()
		text = cleaned_data.get('text')
		title = cleaned_data.get('title')

		if title == text:
			raise ValidationError('Описание не должно быть идентично заголовку')

		return cleaned_data


class ResponseForm(forms.Form):
	text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))