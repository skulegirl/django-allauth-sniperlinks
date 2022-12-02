from django import template

register = template.Library()


@register.simple_tag
def get_sniperlink_for_email(sniperlinks, email):
    if sniperlinks and email in sniperlinks:
        return sniperlinks[email]
