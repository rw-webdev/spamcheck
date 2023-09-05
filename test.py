import json
import os

from django.test import TestCase
from unittest.mock import patch

from spamcheck.util import is_in_spam_list


class TestSpamCheck(TestCase):

    def setUp(self):
        # Mocked blacklist data
        self.mocked_blacklist = {
            'spam_domains': ['spamydomain.com'],
            'spam_emails': ['baduser@spamy.com'],
            'spam_ips': ['192.0.2.123']
        }

    # Test email domain is spam
    @patch('spamcheck.util.fetch_blacklist')
    def test_spam_domain(self, mock_fetch_blacklist):
        mock_fetch_blacklist.return_value = self.mocked_blacklist
        self.assertTrue(is_in_spam_list(email_address='user@spamydomain.com'))

    # Test full email address is spam
    @patch('spamcheck.util.fetch_blacklist')
    def test_spam_email(self, mock_fetch_blacklist):
        mock_fetch_blacklist.return_value = self.mocked_blacklist
        self.assertTrue(is_in_spam_list(email_address='baduser@spamy.com'))

    # Test IP address is spam
    @patch('spamcheck.util.fetch_blacklist')
    def test_spam_ip(self, mock_fetch_blacklist):
        mock_fetch_blacklist.return_value = self.mocked_blacklist
        self.assertTrue(is_in_spam_list(ip_address='192.0.2.123'))

    # Test non-spam inputs
    @patch('spamcheck.util.fetch_blacklist')
    def test_non_spam(self, mock_fetch_blacklist):
        mock_fetch_blacklist.return_value = self.mocked_blacklist
        self.assertFalse(is_in_spam_list(
            email_address='gooduser@goodmail.com', ip_address='192.0.2.124'))

    # Test no inputs
    @patch('spamcheck.util.fetch_blacklist')
    def test_no_input(self, mock_fetch_blacklist):
        mock_fetch_blacklist.return_value = self.mocked_blacklist
        self.assertFalse(is_in_spam_list())

    def test_can_parse_json(self):
        """Make sure no issues parsing the blacklist json file"""

        json_data = open(f'{os.path.dirname(os.path.abspath(__file__))}/blacklist.json')
        blacklist_data = json.load(json_data)
        json_data.close()

        self.assertTrue('spam_domains' in blacklist_data)
        self.assertTrue('spam_emails' in blacklist_data)
        self.assertTrue('spam_ips' in blacklist_data)
