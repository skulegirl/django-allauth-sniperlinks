# Django Allauth Sniperlinks

django-allauth-sniperlinks is a Django app to provide sniper links,
allowing users to quickly find account verification/confirmation emails
in their inbox.

Development supported by [Subscribe Sense](https://www.subscribesense.com), which provides hosted sniper link support and other friction reduction for marketing email list signup.

The package integrates with the amazing [Django Allauth](https://github.com/pennersr/django-allauth) package.

## Quick start

1. Add "allauth_sniperlinks" to your INSTALLED_APPS setting **before the allauth package**  like this:
    ```
    INSTALLED_APPS = [
        ...
        'allauth_sniperlinks',
        'allauth',
        ...
    ]
    ```

2. Add "allauth_sniperlinks.context_processors.unverified_email_sniperlinks" to the 'context_processors' option in your TEMPLATES setting:
    ```
    TEMPLATES = [
        {
            ...
            'OPTIONS': {
                'context_processors': [
                    ...
                    'allauth_sniperlinks.context_processors.unverified_email_sniperlinks',
                    ...
                ],
            },
            ...
        },
    ]
    ```

3. In settings, set `ACCOUNT_ADAPTER="allauth_sniperlinks.adapter.SniperLinkAccountAdapter"`.

    If you have already overridden the account adapter to support another allauth package, you may need to create a custom account adapter that inherits from both adapters.
    
    E.g. in myapp/adapters.py:
    ```
    from allauth_sniperlinks.adapter import SniperLinkAccountAdapter
    from apps.teams.adapter import AcceptInvitationAdapter

    class MyappAccountAdapter(AcceptInvitationAdapter, SniperLinkAccountAdapter):
        pass
    ```

    And in settings.py:
    ```
    ACCOUNT_ADAPTER = 'myapp.adapters.MyappAccountAdapter'
    ```

4. Run python manage.py migrate to create the allauth_sniperlinks models.
