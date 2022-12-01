from django.conf import settings
from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured


def get_email_model_string(self) -> str:
        """Get the configured email model as a module path string."""
        return getattr(settings, "ALLAUTH_SNIPERLINKDS_EMAIL_MODEL", 'allauth.account.EmailAddress')  # type: ignore


def get_email_model(self):
    """
    Attempt to pull settings.ALLAUTH_SNIPERLINKDS_EMAIL_MODEL.
    Users have the option of specifying a custom subscriber model via the
    ALLAUTH_SNIPERLINKDS_EMAIL_MODEL setting.
    This methods falls back to allauth.account.EmailAddress if ALLAUTH_SNIPERLINKDS_EMAIL_MODEL is not set.
    Returns the email model that is active in this project.
    """
    model_name = get_email_model_string()

    # Attempt a Django 1.7 app lookup
    try:
        email_model = django_apps.get_model(model_name)
    except ValueError:
        raise ImproperlyConfigured(
            "ALLAUTH_SNIPERLINKDS_EMAIL_MODEL must be of the form 'app_label.model_name'."
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"ALLAUTH_SNIPERLINKDS_EMAIL_MODEL refers to model '{model_name}' "
            "that has not been installed."
        )

    if (
        "email"
        not in [field_.name for field_ in email_model._meta.get_fields()]
    ) and not hasattr(email_model, "email"):
        raise ImproperlyConfigured(
            "ALLAUTH_SNIPERLINKDS_EMAIL_MODEL must have an email attribute."
        )

    return email_model
