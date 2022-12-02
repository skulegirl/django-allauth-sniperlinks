from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from django.utils.safestring import mark_safe
from allauth.account.adapter import DefaultAccountAdapter
from allauth_sniperlinks import app_settings


class SniperLinkAccountAdapter(DefaultAccountAdapter):
    def add_message(
        self,
        request,
        level,
        message_template,
        message_context=None,
        extra_tags="",
    ):
        """
        Wrapper of `django.contrib.messages.add_message`, that reads
        the message text from a template.
        """
        if "django.contrib.messages" in settings.INSTALLED_APPS:
            try:
                if message_context is None:
                    message_context = {}
                message = render_to_string(
                    message_template,
                    message_context,
                    self.request,
                ).strip()
                if message:
                    if message_template in app_settings.SAFE_TEMPLATES:
                        message = mark_safe(message)
                    messages.add_message(request, level, message, extra_tags=extra_tags)
            except TemplateDoesNotExist:
                pass