from django.apps import AppConfig


class DealerConfig(AppConfig):
    name = 'dealer'

    def ready(self):
        import dealer.signals