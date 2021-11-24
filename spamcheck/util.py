import logging

from .spamlist import spam_domains, spam_emails, spam_ips

logger = logging.getLogger(__name__)


def is_in_spam_list(email_address=None, ip_address=None):
    """Check email or IP against spam lists if provided

    :param str email_address: Email address
    :param str ip_address: IP address
    :return: bool
    """

    '''Check email against spam domains/addresses'''
    if email_address and '@' in email_address:
        email_address = email_address.lower()
        if email_address[email_address.index('@') + 1:] in spam_domains:
            logger.warning('ContactUsForm Spammer (Domain): %s' % email_address)
            return True
        if email_address in spam_emails:
            logger.warning('ContactUsForm Spammer (Email): %s' % email_address)
            return True

    '''Check IP against spam IPs'''
    if ip_address and ip_address in spam_ips:
        logger.warning('ContactUsForm Spammer (IP): %s' % ip_address)
        return True

    return False


def visitor_ip_address(request):
    """Get visitor IP address"""

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
