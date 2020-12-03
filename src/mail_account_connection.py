# Python standard.
import email
import imaplib
import os
from datetime import date, timedelta
from itertools import chain
from typing import List, Union
from email.message import Message

# Local.
from settings import TRUSTED_SENDERS, ACCEPTED_FILETYPES
from tools.logger import *


class MailAccountConnection:
    TRUSTED_FROM_ADDRESSES = TRUSTED_SENDERS

    def __init__(self, mail_server: str, username: str, password: str):
        self.connection = imaplib.IMAP4_SSL(mail_server)
        self.connection.login(username, password)

    def _close_connection(self):
        self.connection.close()

    @classmethod
    def _get_sent_since_filter(cls) -> str:
        return f'(SENTSINCE {(date.today() - timedelta(1)).strftime("%d-%b-%Y")})'

    @classmethod
    def _get_header_from_filter(cls, email_address: str) -> Union[str, None]:
        """ https://tools.ietf.org/html/rfc3501.html#page-49 6.4.4"""
        return f'(HEADER FROM "{email_address}")'

    def _get_email_message_from_id(self, email_id: str) -> Message:
        _type, raw_data = self.connection.fetch(email_id, '(RFC822)')

        return email.message_from_bytes(raw_data[0][1])

    def _mark_as_read(self, email_id: str):
        self.connection.store(email_id, '+FLAGS', '\Seen')

    def _get_email_ids(self) -> list:
        ids = []
        for email_address in self.TRUSTED_FROM_ADDRESSES:
            (result, email_ids) = self.connection.search(
                None,
                '(UNSEEN)',
                self._get_sent_since_filter(),
                self._get_header_from_filter(email_address),
            )
            if result == "OK":
                ids.append(reversed(email_ids[0].split()))

        return list(chain.from_iterable(ids))

    def get_unread_mail(self, mailbox_name: str) -> List[Message]:
        emails = []
        self.connection.select(mailbox_name, readonly=False)
        for email_id in self._get_email_ids():
            try:
                emails.append(self._get_email_message_from_id(email_id))
                self._mark_as_read(email_id)
            except Exception as exc:
                logger.error(f'{exc} for email id: {email_id}. Skipping email.', exc_info=True)
        self._close_connection()

        return emails

    @classmethod
    def download_attachment(cls, message: Message, download_folder: str = "/tmp"):
        for part in message.walk():
            filename = part.get_filename()
            if filename and filename.split('.')[-1] in ACCEPTED_FILETYPES:
                download_location = os.path.join(download_folder, filename)
                if not os.path.isfile(download_location):
                    with open(download_location, 'wb') as output_loc:
                        output_loc.write(part.get_payload(decode=True))
                    logger.info(f'Downloaded "{filename}" to {download_location}')

