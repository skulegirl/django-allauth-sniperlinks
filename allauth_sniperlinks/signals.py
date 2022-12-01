from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from allauth.account.models import EmailAddress
from allauth_sniperlinks import app_settings
from allauth_sniperlinks.utils import get_mx_domian_and_provider
from allauth_sniperlinks.models import SniperLink

@receiver(pre_save, sender=EmailAddress)
def cache_previous_email(sender, instance, *args, **kwargs):
    original_email = None
    if instance.id:
        original_email = EmailAddress.objects.get(pk=instance.id).email
    
    instance.__original_email = original_email


@receiver(post_save, sender=EmailAddress)
def update_mx_domain_and_provider(sender, instance, created, **kwargs):
    if created:
        mx_domain, mail_provider = get_mx_domian_and_provider(instance.email)
        SniperLink.objects.create(
            email_object=instance,
            mx_domain=mx_domain,
            mail_provider=mail_provider
        )
    elif instance.__original_email != instance.email:
        mx_domain, mail_provider = get_mx_domian_and_provider(instance.email)
        instance.sniperlink.mx_domain = mx_domain
        instance.sniperlink.mail_provider = mail_provider
        instance.sniperlink.save()
