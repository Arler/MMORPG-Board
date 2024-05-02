from django.apps import AppConfig


class SubaccountSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subaccount_system'

    def ready(self):
        from . import signals