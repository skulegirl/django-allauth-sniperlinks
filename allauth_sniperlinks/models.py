from django.db import models
from django.utils.translation import gettext_lazy as _
from allauth.account.models import EmailAddress

# Create your models here.
class MailProviders(models.TextChoices):
    UNKNOWN = 'UNKNOWN', _('Unknown')
    GMAIL = 'GMAIL', _('Gmail')
    GSUITE = 'GSUITE', _('Gsuite')
    YAHOO = 'YAHOO', _('Yahoo')
    AOL = 'AOL', _('AOL')
    ROGERS = 'ROGERS', _('ROGERS')
    OUTLOOK = 'OUTLOOK', _('Outlook')
    ICLOUD = 'ICLOUD', _('iCloud')
    CHARTER = 'CHARTER', _('Charter')
    CENTURYLINK = 'CENTURYLINK', _('CenturyLink')
    ONEANDONE = 'ONEANDONE', _('1and1')
    COMCAST = 'COMCAST', _('Comcast')
    COX = 'COX', _('Cox')
    SHAW = 'SHAW', _('Shaw')
    FASTMAIL = 'FASTMAIL', _('Fastmail')
    FRONTIER = 'FRONTIER', _('Frontier')
    MAILDOTCOM = 'MAILDOTCOM', _('Mail_com')
    EARTHLINK = 'EARTHLINK', _('Earthlink')
    PRODIGY = 'PRODIGY', _('Prodigy')
    PROTONMAIL = 'PROTONMAIL', _('ProtonMail')
    JUNO = 'JUNO', _('Juno')
    NETADDRESS = 'NETADDRESS', _('NetAddress')  # USA.NET
    VIDEOTRON = 'VIDEOTRON', _('Videotron')
    WINDSTREAM = 'WINDSTREAM', _('Windstream')  # (Seems same as Century Link)
    ZOHO = 'ZOHO', _('Zoho')


class SniperLink(models.Model):
    email_object = models.OneToOneField(
        EmailAddress,
        on_delete=models.CASCADE,
    )
    mx_domain = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    mail_provider = models.CharField(
        max_length=30,
        choices=MailProviders.choices,
        default=MailProviders.UNKNOWN,
    )
