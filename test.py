import json
import os

from django.http import HttpRequest
from django.test import TestCase
from unittest.mock import patch, MagicMock

from spamcheck import SpamCheck


class TestSpamCheck(TestCase):

    @patch('spamcheck.main.fetch_blacklist')
    def setUp(self, mock_fetch_blacklist):

        # Create a mock request object
        mock_request = MagicMock(spec=HttpRequest)
        mock_request.META = {
            'HTTP_X_FORWARDED_FOR': '192.168.1.1',
            'REMOTE_ADDR': '127.0.0.1'
        }

        # Mocked blacklist data
        mock_fetch_blacklist.return_value = {
            'spam_domains': ['spamydomain.com'],
            'spam_emails': ['baduser@spamy.com'],
            'spam_keywords': ['janitorial'],
            'spam_ips': ['192.0.2.123']
        }

        self.spamcheck = SpamCheck(mock_request)

    # Test run all tests function w/ failing email
    def test_fails_spamchecks_spam_email(self):
        self.assertTrue(self.spamcheck.fails_spamchecks(
            email_address='user@spamydomain.com',
            email_body='A valid message'))

    # Test run all tests function w/ failing keyword
    def test_fails_spamchecks_spam_keyword(self):
        self.assertTrue(self.spamcheck.fails_spamchecks(
            email_address='good-user@valid-domain.com',
            email_body='A spammy message containing the bad word "janitorial"'))

    # Test run all tests function w/ passing data
    def test_fails_spamchecks_passing(self):
        self.assertFalse(self.spamcheck.fails_spamchecks(
            email_address='good-user@valid-domain.com',
            email_body='A valid message'))

    # Test full email address is spam
    def test_spam_email(self):
        self.assertTrue(self.spamcheck.is_in_spam_list(
            email_address='baduser@spamy.com'))

    # Test IP address is spam
    @patch('spamcheck.main.visitor_ip_address')
    def test_spam_ip(self, mock_visitor_ip_address):
        self.spamcheck.ip_address = '192.0.2.123'
        self.assertTrue(self.spamcheck.is_in_spam_list())

    # Test non-spam inputs
    @patch('spamcheck.main.visitor_ip_address')
    def test_non_spam(self, mock_visitor_ip_address):
        self.spamcheck.ip_address = '192.0.2.124'
        self.assertFalse(self.spamcheck.is_in_spam_list(
            email_address='gooduser@goodmail.com'))

    # Test no inputs
    def test_no_input(self):
        self.assertFalse(self.spamcheck.is_in_spam_list())

    def test_can_parse_json(self):
        """Make sure no issues parsing the blacklist json file"""

        json_data = open(f'{os.path.dirname(os.path.abspath(__file__))}/blacklist.json')
        blacklist_data = json.load(json_data)
        json_data.close()

        self.assertTrue('spam_domains' in blacklist_data)
        self.assertTrue('spam_emails' in blacklist_data)
        self.assertTrue('spam_ips' in blacklist_data)

    def test_has_spam_keywords_when_true(self):
        """Test has_spam_keywords function when message contains spam"""

        message = """
         Hi there, I hope all is well. We specialize in providing janitorial 
         services. Would you be interested in receiving a free estimate for 
         your facility's janitorial needs? 
        """

        self.assertTrue(self.spamcheck.has_spam_keywords(message))

    def test_has_spam_keywords_when_false(self):
        """Test has_spam_keywords function when message is valid"""

        message = """
         Hi there, I hope all is well. We are interested in a 1031 exchange!
        """

        self.assertFalse(self.spamcheck.has_spam_keywords(message))

