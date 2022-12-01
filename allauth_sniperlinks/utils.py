import time
import re
import tld
import dns.resolver
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from .models import MailProviders, INVALID_EMAIL_FLAG

INVALID_EMAIL_FLAG = 'INVALIDEMAIL'


def get_sniper_link_img(mail_provider):
    try:
        filename = 'images/allauth_sniperlinks/provider_icons/{}.svg'.format(
            dict(MailProviders.choices)[mail_provider]
        )
        if finders.find(filename):
            filepath = static(filename)
        else: 
            filepath = static('images/allauth_sniperlinks/provider_icons/generic.svg')
    except KeyError:
        filepath = static('images/allauth_sniperlinks/provider_icons/generic.svg')
        
    return filepath


def get_mx_domian_and_provider(email_address):
    if email_address:
        match = re.match(r'(.*)@(.*)', email_address)
        if match is None or len(match.groups()) != 2:
            return INVALID_EMAIL_FLAG, None
        domain = match.group(2).lower()
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            mx_record = mx_records[0]
            for r in mx_records:
                if r.preference < mx_record.preference:
                    mx_record = r
        except Exception as e:
            return INVALID_EMAIL_FLAG, None
        try:
            mx_res_obj = tld.get_tld(
                mx_record.exchange.to_text(),
                fix_protocol=True,
                as_object=True,
            )
            email_res_obj = tld.get_tld(
                domain,
                fix_protocol=True,
                as_object=True
            )
            mx_domain = mx_res_obj.fld.lower()
            mail_provider = get_mail_provider(email_res_obj, mx_res_obj)
            return mx_domain, mail_provider
        except tld.exceptions.TldDomainNotFound as e:
            return INVALID_EMAIL_FLAG, None
        except Exception as e:
            return INVALID_EMAIL_FLAG, None


# TODO - changte these to regexes in case MX records span multiple domains or change
# TODO - add nightly tests to check for changes in MX domains
def get_mail_provider(email_res_obj, mx_res_obj):
    mx_domain = mx_res_obj.domain.lower()
    email_domain = email_res_obj.domain.lower()
    
    if mx_domain == 'google' or mx_domain == 'googlemail':
        if email_domain == 'gmail':
            return MailProviders.GMAIL
        else:
            return MailProviders.GSUITE
    
    if mx_domain == 'yahoodns':
        if email_domain == 'aol' or mx_domain == 'cs':
            return MailProviders.AOL
        if email_domain == 'yahoo':
            return MailProviders.YAHOO
        if email_domain == 'rogers':
            return MailProviders.ROGERS
        if email_domain == 'frontier':
            return MailProviders.FRONTIER
        else:
            return MailProviders.YAHOO

    if mx_domain == 'outlook':
        return MailProviders.OUTLOOK

    if mx_domain == 'icloud':
        return MailProviders.ICLOUD
    
    if mx_domain == 'charter':
        return MailProviders.CHARTER
    
    if mx_domain == 'centurylink':
        return MailProviders.CENTURYLINK
    
    if mx_domain == '1and1':
        return MailProviders.ONEANDONE
    
    if mx_domain == 'cloudfilter':
        if email_domain == 'shaw':
            return MailProviders.SHAW
        if email_domain == 'cox':
            return MailProviders.COX
    
    if mx_domain == 'comcast':
        return MailProviders.COMCAST

    if mx_domain == 'messagingengine':
        return MailProviders.FASTMAIL
    
    if mx_domain == 'frontiernet':
        return MailProviders.FRONTIER
    
    if mx_domain == 'mail':
        return MailProviders.MAILDOTCOM

    if mx_domain == 'oxsus-vadesecure':
        return MailProviders.EARTHLINK
    
    if mx_domain == 'prodigy':
        return MailProviders.PRODIGY
    
    if mx_domain == 'protonmail':
        return MailProviders.PROTONMAIL

    if mx_domain == 'untd':
        return MailProviders.JUNO
    
    if mx_domain == 'netaddress':
        return MailProviders.NETADDRESS
    
    if mx_domain == 'videotron':
        return MailProviders.VIDEOTRON
    
    if mx_domain == 'windstream':
        return MailProviders.WINDSTREAM
    
    if mx_domain == 'zoho':
        return MailProviders.ZOHO

    return MailProviders.UNKNOWN


# TODO - update these where possible to have better mobile links to email apps
def get_sniper_link(mail_provider, email_address, outgoing_email_address):
    if mail_provider == MailProviders.UNKNOWN or outgoing_email_address is None:
        return ""

    match = re.match(r'(.*)@(.*)', outgoing_email_address)
    if match is None or len(match.groups()) != 2:
            return ""
    sending_domain = match.group(2).lower()

    match = re.match(r'(.*)@(.*)', email_address)
    if match is None or len(match.groups()) != 2:
        receiving_domain = ""
    else:
        receiving_domain = match.group(2).lower()

    if mail_provider == MailProviders.GMAIL:
        return "https://mail.google.com/mail/u/?#search/from%3A%40{}+in%3Aanywhere".format(
            sending_domain
        )
    
    if mail_provider == MailProviders.GSUITE:
        if receiving_domain:
            return "https://mail.google.com/a/{}/#search/from%3A%40{}+in%3Aanywhere".format(
                receiving_domain,
                sending_domain
            )
        else:
            return "https://mail.google.com/mail/u/?#search/from%3A%40{}+in%3Aanywhere".format(
                sending_domain
            )

    if mail_provider == MailProviders.YAHOO:
        return "https://mail.yahoo.com/d/search/keyword=from%3A{}".format(
            outgoing_email_address
        )
    
    if mail_provider == MailProviders.ROGERS:
        # has search but routes through Rogers-specific login if needed.
        # Seems search param will not be maintained if login required, but should work if already logged in.
        return "https://mail.yahoo.com/d/search/keyword=from%3A{}?.intl=ca&.partner=rogers-acs&.lang=en-CA".format(
            outgoing_email_address
        )

    if mail_provider == MailProviders.FRONTIER:
        # has search but routes through Frontier-specific login if needed.
        # (Unclear if search param will be maintained if login required, but should work if already logged in.)
        return "https://mail.yahoo.com/d/search/keyword=from%3A{}?.intl=us&.partner=ftr&.lang=en-US".format(
            outgoing_email_address
        )
    
    if mail_provider == MailProviders.PRODIGY:
        # has search but routes through ATT-specific login if needed.
        # (Unclear if search param will be maintained if login required, but should work if already logged in.)
        return "https://mail.yahoo.com/d/search/keyword=from%3A{}?.intl=us&.partner=sbc&.lang=en-US".format(
            outgoing_email_address
        )

    if mail_provider == MailProviders.AOL:
        return "https://https://mail.aol.com/"

    if mail_provider == MailProviders.OUTLOOK:
        return "https://outlook.live.com/"

    # really need to do this one based on device, open app on mobile
    if mail_provider == MailProviders.ICLOUD:
        return "https://www.icloud.com/mail"
    
    if mail_provider == MailProviders.CHARTER:
        return "http://webmail.spectrum.net/"
    
    if mail_provider == MailProviders.CENTURYLINK:
        # redirect to login only works for recent timestamps, otherwise goes to
        # main page
        ts = int(time.time())
        return "http://centurylink.net/zmail/index.php?autologin=true&ts={}".format(ts)

    if mail_provider == MailProviders.ONEANDONE:
        return "https://mail.ionos.ca/"

    if mail_provider == MailProviders.SHAW:
        return "https://webmail.shaw.ca/"

    if mail_provider == MailProviders.COX:
            return "https://myemail.cox.net/"
    
    if mail_provider == MailProviders.COMCAST:
        return "https://xfinityconnect.email.comcast.net/" 

    if mail_provider == MailProviders.FASTMAIL:
        # Supports searching all folders with in:*
        return "https://www.fastmail.com/mail/search:in%3A*+from%3A{}/".format(
            sending_domain
        )

    if mail_provider == MailProviders.MAILDOTCOM:
        # MAIL.COM annoyingly doesn't let you use a generic link, so it will redirect to mail.com 
        # and make people log in every time. Stupid.
        return "https://navigator-lxa.mail.com/"

    if mail_provider == MailProviders.PROTONMAIL:
        # Supports searching all with all-mail
        return "https://mail.protonmail.com/u/0/all-mail#from={}".format(
            sending_domain
        )

    if mail_provider == MailProviders.JUNO:
        return "https://webmaila.juno.com/webmail/new/"

    # if mail_provider == MailProviders.EARTHLINK:
    # if mail_provider == MailProviders.NETADDRESS:
    # if mail_provider == MailProviders.VIDEOTRON:
    # if mail_provider == MailProviders.WINDSTREAM:
    # if mail_provider == MailProviders.ZOHO:

    return ""