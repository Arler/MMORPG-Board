from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.core.cache import cache

from .models import Announcement, UserResponse
from .forms import CreateAnnouncementForm


class AnnouncementsList(ListView):
    model = Announcement
    ordering = '-date_created'
    template_name = 'board_app/board.html'
    context_object_name = 'announcements'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'announcement-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'announcement-{self.kwargs["pk"]}', obj)
            return obj

        return obj


class ResponsesList(PermissionRequiredMixin, ListView):
    permission_required = ('board.view_userresponse',)
    model = UserResponse
    ordering = '-date_created'
    template_name = 'board_app/responses.html'
    context_object_name = 'user_response'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'userresponse-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'userresponse-{self.kwargs["pk"]}', obj)
            return obj

        return obj

    def dispatch(self, request, *args, **kwargs):
        """
        Переопределение метода dispatch необходимо, чтобы пользователь мог быть перенаправлен на страницу ввода
        одноразового кода, если он захочет перейти на страницу этого представления, не вводя сам код.
        """
        if self.request.user.is_authenticated and not self.request.user.authorized:
            return redirect('/subaccountsystem/onetimecode/')
        else:
            return super().dispatch(request, *args, **kwargs)


class CreateAnnouncement(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_announcement',)
    form_class = CreateAnnouncementForm
    model = Announcement
    template_name = 'board_app/create_announcement.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Переопределение метода dispatch необходимо, чтобы пользователь мог быть перенаправлен на страницу ввода
        одноразового кода, если он захочет перейти на страницу этого представления, не вводя сам код.
        """
        if self.request.user.is_authenticated and not self.request.user.authorized:
            return redirect('/subaccountsystem/onetimecode/')
        else:
            return super().dispatch(request, *args, **kwargs)
