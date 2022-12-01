from django.contrib import admin
from allauth_sniperlinks.models import SniperLink

@admin.register(SniperLink)
class SniperLinkAdmin(admin.ModelAdmin):
    list_dislay = ['email_object__email', 'mx_domain', 'mail_provider']
