# Local.
from src.mail_account_connection import MailAccountConnection
from tests.mocks.mock_imap_handler import MockImapHandler


class MockMailAccountConnection(MailAccountConnection):
    TRUSTED_FROM_ADDRESSES = ['example_2@hostname.com', 'example_3@hostname.de']

    def __init__(self):
        self.connection = MockImapHandler()
        self.connection.login = ''

    def _close_connection(self):
        return 'Connection closed.'

