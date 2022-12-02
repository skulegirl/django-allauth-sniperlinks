from django.core.cache import cache
from allauth_sniperlinks.models import SniperLink
from allauth_sniperlinks.utils import get_sniper_link, get_sniper_link_img, USER_SNIPERLINK_CACHE_KEY
from allauth_sniperlinks.app_settings import VERIFICATION_SENDER


def unverified_email_sniperlinks(request):
    """
    Adds sniperlinks for any unverified emails for the currently logged in user
    to context.
    """
    sniperlinks_context = cache.get(USER_SNIPERLINK_CACHE_KEY.format(request.user.id))
    if sniperlinks_context is None:
        sniperlinks_context = {}
        unverified_email_sls = SniperLink.objects.filter(
            email_object__user=request.user, 
            email_object__verified=False
        )
        for sl in unverified_email_sls:
            sniperlinks_context[sl.email_object.email] = {
                'link': get_sniper_link(sl.mail_provider, sl.email_object.email, VERIFICATION_SENDER),
                'img': get_sniper_link_img(sl.mail_provider)
            }
        # Cache entry is invalidated via signal handler when any of the user's email entries change
        cache.set(
            USER_SNIPERLINK_CACHE_KEY.format(request.user.id),
            sniperlinks_context,
        )
    return {
        'sniperlinks': sniperlinks_context
    }
