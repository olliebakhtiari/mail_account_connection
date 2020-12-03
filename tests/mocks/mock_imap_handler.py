# Python standard.
import re
from typing import Tuple, List, Union

# Local.
from tests.mocks.mock_message import MockMessage


class MockImapHandler:
    def __init__(self):
        self.mailbox_map = {
            'Inbox': {
                'example_2@hostname.com': [1, 2, 3],
                'example_3@hostname.de': [4, 5, 6],
            },
            'Important': {
                'example_2@hostname.com': [7, 8, 9],
                'example_3@hostname.de': [10, 11, 12],
            },
        }
        self.available_mailboxes = list(self.mailbox_map.keys())
        self.mailbox_selected = self.available_mailboxes[0]

    @classmethod
    def parse_header_from(cls, query: str) -> str:
        return re.match(r"^.*\"(.*)\".*$", query).group(1)

    def parse_filter(self, query: str) -> str:
        if 'HEADER FROM' in query:
            return self.parse_header_from(query)
        else:
            raise NotImplementedError('Filter parser for query not implemented.')

    @classmethod
    def fetch(cls, *args):
        return MockMessage()

    def search(self, charset, *criteria) -> Union[Tuple[str, List[int]], None]:
        for arg in criteria:
            valid_sender = self.parse_filter(arg)
            if valid_sender:
                return "OK", self.mailbox_map[self.mailbox_selected][valid_sender]

    def store(self, *args):
        pass

    def select(self, mailbox_name: str, **kwargs):
        if mailbox_name not in self.available_mailboxes:
            raise ValueError('Mailbox specified not valid.')
        self.mailbox_selected = mailbox_name
