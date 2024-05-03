from django.views.generic.edit import FormView
from django.shortcuts import redirect

from .forms import OneTimeCodeForm


class OneTimeCodeView(FormView):
    template_name = 'subaccount_system/one_time_code.html'
    form_class = OneTimeCodeForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.authorized:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('/')