from django.apps import AppConfig


class AdviceConfig(AppConfig):
    name = 'apps.advice'
    verbose_name = "Платные консультации"

    def ready(self):
        import apps.advice.signals
