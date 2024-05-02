from django.views.generic.edit import FormView

from .forms import OneTimeCodeForm


class OneTimeCodeView(FormView):
    template_name = 'subaccount_system/one_time_code.html'
    form_class = OneTimeCodeForm
    success_url = '/'
