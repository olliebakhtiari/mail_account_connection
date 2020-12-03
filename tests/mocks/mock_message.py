# Python standard.
from __future__ import annotations
from random import choice, randint
from typing import List

# Local.
from settings import ACCEPTED_FILETYPES


class MockMessage:
    INVALID_FILETYPES = ['.jar', '.bat', '.adp', '.asf', '.bas', '.chm', '.cmd', '.com', '.exe', '.mov', '.msi']

    def __init__(self, filename: str = '', valid_attachment_count: int = 0):
        self.filename = filename
        self.valid_attachment_count = valid_attachment_count
        self.invalid_attachment_count = 3 - valid_attachment_count

    def walk(self) -> List[MockMessage]:
        parts = []
        for i in range(self.valid_attachment_count):
            parts.append(MockMessage(filename=f'valid-file-{randint(0, 500)}{choice(ACCEPTED_FILETYPES)}'))
        for j in range(self.invalid_attachment_count):
            parts.append(MockMessage(filename=f'invalid-file-{randint(500, 1000)}{choice(self.INVALID_FILETYPES)}'))

        return parts

    def get_filename(self) -> str:
        return self.filename

