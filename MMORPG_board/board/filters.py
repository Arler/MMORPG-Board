from django_filters import FilterSet, CharFilter

from .models import UserResponse


class UserResponseFilter(FilterSet):
	responder__username = CharFilter(field_name='responder__username', lookup_expr='contains',
									 label='Пользователь:')
	announcement__title = CharFilter(field_name='announcement__title', lookup_expr='contains',
									 label='Объявление:')

	class Meta:
		model = UserResponse
		fields = ['responder__username', 'announcement__title']
