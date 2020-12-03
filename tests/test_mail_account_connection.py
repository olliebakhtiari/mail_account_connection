# Python standard.
import unittest
from datetime import date, timedelta

# Local.
from tests.mocks.mock_mail_account_connection import MockMailAccountConnection


class TestMailAccountConnection(unittest.TestCase):
    def setUp(self):
        self.mail_account_connection = MockMailAccountConnection

    def test_get_sent_since_filter(self):
        yesterday = (date.today() - timedelta(1)).strftime("%d-%b-%Y")
        expected_filter = f'(SENTSINCE {yesterday})'
        self.assertEqual(expected_filter, self.mail_account_connection._get_sent_since_filter())

    def test_get_header_from_filter(self):
        expected_filter = '(HEADER FROM "example_2@hostname.com")'
        self.assertEqual(expected_filter, self.mail_account_connection._get_header_from_filter('example_2@hostname.com'))

    def test_get_mail_from_different_mailboxes(self):
        pass

    def test_download_single_valid_attachment_successfully(self):
        pass

    def test_download_multiple_valid_attachment_successfully(self):
        pass

    def test_doesnt_download_invalid_filetype(self):
        pass

    def test_doesnt_download_single_invalid_filetype_from_multiple_attachments(self):
        pass


if __name__ == '__main__':
    unittest.main()
