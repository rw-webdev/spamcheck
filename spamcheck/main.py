import json
import logging

try:
    from django.conf import settings
except ImportError:
    settings = None

import boto3

logger = logging.getLogger(__name__)


class SpamCheck:

    blacklist = None

    def __init__(self, request):
        self.blacklist = fetch_blacklist()
        self.ip_address = visitor_ip_address(request)

    def fails_spamchecks(self, email_address, email_body):
        return self.is_in_spam_list(email_address) or self.has_spam_keywords(email_body)

    def has_spam_keywords(self, email_body):

        # Check for spam keywords in the subject and body
        for keyword in self.blacklist.get('spam_keywords', []):
            if keyword.lower() in email_body.lower():
                logger.warning('Form Spammer (Keyword): %s' % keyword.lower())
                return True
        return False

    def is_in_spam_list(self, email_address=None):
        """Check email or IP against spam lists if provided

        :param str email_address: Email address
        :return: bool
        """

        '''Check email against spam domains/addresses'''
        if email_address and '@' in email_address:
            email_address = email_address.lower()
            if email_address[email_address.index('@') + 1:] in self.blacklist.get('spam_domains', []):
                logger.warning('Form Spammer (Domain): %s' % email_address)
                return True
            if email_address in self.blacklist.get('spam_emails', []):
                logger.warning('Form Spammer (Email): %s' % email_address)
                return True

        '''Check IP against spam IPs'''
        if self.ip_address and self.ip_address in self.blacklist.get('spam_ips', []):
            logger.warning('Form Spammer (IP): %s' % self.ip_address)
            return True

        return False

    def get_visitor_ip_address(self):
        return self.ip_address


def visitor_ip_address(request):
    """Get visitor IP address"""

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def fetch_blacklist():
    session = boto3.session.Session()
    try:
        client = session.client(
            's3', region_name='sfo2',
            endpoint_url=settings.SPAMLIST_ENDPOINT_URL,
            aws_access_key_id=settings.SPAMLIST_KEY_ID,
            aws_secret_access_key=settings.SPAMLIST_SECRET_KEY)
    except Exception as e:
        logger.error(e)
        return {}

    try:
        '''Fetch the file content'''
        response = client.get_object(
            Bucket=settings.SPAMLIST_BUCKET_NAME, Key='email-blacklist/blacklist.json')
        file_content = response['Body'].read().decode('utf-8')
        return json.loads(file_content)
    except Exception as e:
        logger.error(e)
    return {}
