from django.views.decorators.cache import cache_page
from django.urls import path

from .views import AnnouncementsList, CreateAnnouncement, ResponsesList


urlpatterns = [
    path('', cache_page(0)(AnnouncementsList.as_view()), name='board'),
    path('createannouncement/', CreateAnnouncement.as_view(), name='create_announcement'),
    path('responses/', cache_page(0)(ResponsesList.as_view()), name='responses_list'),
]
