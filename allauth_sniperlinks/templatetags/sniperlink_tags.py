from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def get_sniperlink_for_email(sniperlinks, email):
    if sniperlinks and email in sniperlinks:
        return sniperlinks[email]


@register.simple_tag(takes_context=True)
def unverified_email_banner(context, banner_class="", link_class=""):
    print("Hi mom!")
    sniperlinks = context['sniperlinks']
    unverified_emails = []

    html = ''
    # Check if the user has any unverified email addresses from allauth
    if sniperlinks:
        # Loop through the sniperlinks in the context.
        for email in sniperlinks:
            link = sniperlinks[email]['link']
            if link:
                img = sniperlinks[email]['img']
                html += f'<div class="{banner_class}" style="display:flex; align-items:center; justify-content: space-between;">'
                html += '<div style="display:flex; align-items:center; overflow-wrap: anywhere;">'
                html += '''
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="height:2rem; width:2rem; color: #ffcc00; margin-left:0.5em; margin-right:0.5rem;">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
                </svg>

                '''
                html += f'Please confirm your email address: {email}.'
                html += '</div>'
                html += f'<a href="{link}" class="{link_class}" target="_blank" style="display: flex; align-items: center; margin-left:1rem; margin-right:1rem; flex-shrink: 0">'
                html += f'<img src="{img}" alt="mail provider icon" style="margin-right: 0.5em; width: 2rem;">'
                html += 'Open Confirmation Email'
                html += '</a>'
                html += '</div>'

    # Return the HTML as a safe string
    return mark_safe(html)
