from django.apps import AppConfig


class AllauthSniperlinksConfig(AppConfig):
    name = 'allauth_sniperlinks'

    def ready(self):
        from . import signals