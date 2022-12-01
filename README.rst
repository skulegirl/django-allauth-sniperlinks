=====
Django Allauth Sniperlinks
=====

django-allauth-sniperlinks is a Django app to provide sniper links,
allowing users to quickly find account verification/confirmation emails
in their inbox

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "allauth_sniperlinks" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'allauth_sniperlinks',
    ]

2. Run ``python manage.py migrate`` to create the allauth_sniperlinks models.
