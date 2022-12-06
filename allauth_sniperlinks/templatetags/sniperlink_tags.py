from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


register = template.Library()


@register.simple_tag
def get_sniperlink_for_email(sniperlinks, email):
    if sniperlinks and email in sniperlinks:
        return sniperlinks[email]


@register.simple_tag(takes_context=True)
def unverified_email_banner(context, banner_class="", link_class=""):
    sniperlinks = context['sniperlinks']
    context['banner_class'] = banner_class
    context['link_class'] = link_class
    html = ''
    # Check if the user has any unverified email addresses from allauth
    if sniperlinks:
        # Loop through the sniperlinks in the context.
        for email in sniperlinks:
            banner_context = context.flatten()
            link = sniperlinks[email]['link']
            if link:
                banner_context['email'] = email
                banner_context['link'] = link
                banner_context['img'] = sniperlinks[email]['img']
                html += render_to_string('allauth_sniperlinks/banner.html', banner_context)

    # Return the HTML as a safe string
    return mark_safe(html)
