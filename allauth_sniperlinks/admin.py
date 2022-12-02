from django.contrib import admin
from allauth_sniperlinks.models import SniperLink

@admin.register(SniperLink)
class SniperLinkAdmin(admin.ModelAdmin):
    list_display = ['email_object', 'mx_domain', 'mail_provider']
