from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.core.cache import cache

from .models import Announcement, UserResponse
from subaccount_system.models import User
from .forms import CreateAnnouncementForm, ResponseForm
from .filters import UserResponseFilter


class AnnouncementsList(ListView):
    model = Announcement
    ordering = '-date_created'
    template_name = 'board_app/board.html'
    context_object_name = 'announcements'
    paginate_by = 10

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'announcement-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'announcement-{self.kwargs["pk"]}', obj)
            return obj

        return obj

    def post(self, request, **kwargs):
        if 'action' in request.POST and request.POST['action'] == 'delete':
            Announcement.objects.get(pk=request.POST['announcement_id']).delete()
            return redirect('.')


class AnnouncementDetail(DetailView, FormView):
    model = Announcement
    template_name = 'board_app/announcement.html'
    context_object_name = 'announcement'
    form_class = ResponseForm
    success_url = '.'

    def post(self, request, *args, **kwargs):
        if 'action' in request.POST and request.POST['action'] == 'delete':
            UserResponse.objects.get(pk=request.POST['response_id']).delete()
            return redirect(f'/{kwargs.get("pk")}')
        else:
            form = self.get_form()
            if form.is_valid():
                announcement = Announcement.objects.get(pk=kwargs.get('pk'))
                UserResponse.objects.create(
                    responder=request.user, announcement=announcement, text=form.cleaned_data.get('text')
                )
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = UserResponse.objects.filter(announcement=context['announcement']).all().order_by('-date_created')
        return context


class ResponsesList(PermissionRequiredMixin, ListView):
    permission_required = ('board.view_userresponse',)
    model = UserResponse
    ordering = '-date_created'
    template_name = 'board_app/responses.html'
    context_object_name = 'responses'
    paginate_by = 10

    def get_queryset(self):
        queryset = UserResponse.objects.filter(announcement__author=self.request.user).order_by('-date_created')
        self.filterset = UserResponseFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'userresponse-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'userresponse-{self.kwargs["pk"]}', obj)
            return obj

        return obj

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['send_news'] = self.request.user.send_news
        return context

    def post(self, request):
        if request.POST['action'] == 'accept':
            response_id = request.POST['response_id']
            user_response = UserResponse.objects.get(pk=response_id)
            user_response.accepted = True
            user_response.save()
        elif request.POST['action'] == 'send_news':
            user = User.objects.get(pk=request.user.id)
            if request.POST.get('send_news', False):
                user.send_news = True
                user.save()
            else:
                user.send_news = False
                user.save()
        elif request.POST['action'] == 'reject':
            response_id = request.POST['response_id']
            user_response = UserResponse.objects.get(pk=response_id)
            user_response.rejected = True
            user_response.save()
        return redirect('.')

    def dispatch(self, request, *args, **kwargs):
        """
        Переопределение метода dispatch необходимо, чтобы пользователь был перенаправлен на страницу ввода
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
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        """
        Переопределение метода dispatch необходимо, чтобы пользователь был перенаправлен на страницу ввода
        одноразового кода, если он захочет перейти на страницу этого представления, не вводя сам код.
        """
        if self.request.user.is_authenticated and not self.request.user.authorized:
            return redirect('/subaccountsystem/onetimecode/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

