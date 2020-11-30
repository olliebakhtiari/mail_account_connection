# Python standard.
import email
import imaplib
import logging
import os
from datetime import date, timedelta
from typing import List
from email.message import Message

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class MailAccountConnection:
    def __init__(self, mail_server: str, username: str, password: str):
        self.connection = imaplib.IMAP4_SSL(mail_server)
        self.connection.login(username, password)
        self.connection.select('Inbox', readonly=False)

    def close_connection(self):
        self.connection.close()

    @classmethod
    def _get_sent_since_filter(cls) -> str:
        return f'(SENTSINCE {(date.today() - timedelta(1)).strftime("%d-%b-%Y")})'

    def _get_email_message_from_id(self, email_id: str) -> Message:
        _type, raw_data = self.connection.fetch(email_id, '(RFC822)')

        return email.message_from_bytes(raw_data[0][1])

    def _mark_as_read(self, email_id: str):
        self.connection.store(email_id, '+FLAGS', '\Seen')

    def get_unread_mail(self) -> List[Message]:
        emails = []
        (result, email_ids) = self.connection.search(None, '(UNSEEN)', self._get_sent_since_filter())
        if result == "OK":
            email_ids = reversed(email_ids[0].split())
            for email_id in email_ids:
                try:
                    emails.append(self._get_email_message_from_id(email_id))
                    self._mark_as_read(email_id)
                except Exception as exc:
                    logger.error(f'{exc} for email id: {email_id}. Skipping email.', exc_info=True)
        self.close_connection()

        return emails

    @classmethod
    def download_attachment(cls, message: Message, download_folder: str = "/tmp"):
        for part in message.walk():
            filename = part.get_filename()
            if filename:
                download_location = os.path.join(download_folder, filename)
                if not os.path.isfile(download_location):
                    with open(download_location, 'wb') as output_loc:
                        output_loc.write(part.get_payload(decode=True))
                    logger.info(f'Downloaded "{filename}" to {download_location}')

