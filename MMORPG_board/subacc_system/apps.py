from django.apps import AppConfig


class SubaccSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subacc_system'

    def ready(self):
        from . import signals