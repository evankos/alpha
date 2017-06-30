from django.apps import AppConfig


class BackdoorConfig(AppConfig):
    name = 'backdoor'

    def ready(self):
        import backdoor.signals  # noqa

