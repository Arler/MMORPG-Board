from django.urls import path
from .views import OneTimeCodeView


urlpatterns = [
    path('onetimecode/', OneTimeCodeView.as_view())
]