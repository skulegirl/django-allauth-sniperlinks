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

## Settings

* ALLAUTH_SNIPERLINKS_VERIFICATION_SENDER
    Set the email used to send verification senders. This is used when creating sniper links, see features section below for an example.
    
    Defaults to DEFAULT_FROM_EMAIL.


## Features

Out of the box, a button with a sniper link for the email address submitted will be included in the message that appears after a verification email has been sent, e.g.: ![Sniper Link Sample Image](readme_images/SniperLinkSampleImg.png)

The button will open up the users webmail browser in another tab and attempt to pull up any emails sent from the address configured by ALLAUTH_SNIPERLINKS_VERIFICATION_SENDER.

The icon will change to match the webmail provider. See models.MailProviders for a list of currently supported webmail providers. 

Unsupported mail providers will not show a sniper link button.