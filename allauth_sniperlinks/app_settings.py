from django.conf import settings
from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured

VERIFICATION_SENDER = getattr(settings, "ALLAUTH_SNIPERLINKS_VERIFICATION_SENDER", settings.DEFAULT_FROM_EMAIL)
SAFE_TEMPLATES = getattr(
    settings, "ALLAUTH_SNIPERLINKS_SAFE_TEMPLATES",
    [
        "account/messages/" "email_confirmation_sent.txt",
    ]
)