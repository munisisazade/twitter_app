from django.apps import AppConfig


class BaseUserConfig(AppConfig):
    name = 'base_user'
    verbose_name = "Istifadəçilər"

    def ready(self):
        import base_user.signals
