# Local.
from settings import USERNAME, PASSWORD, MAIL_SERVER
from src.mail_account_connection import MailAccountConnection
from tools.logger import *


def download_latest_mail_attachments():
    mail_account_connection = MailAccountConnection(MAIL_SERVER, USERNAME, PASSWORD)
    logger.debug('Checking for mail...')
    emails = mail_account_connection.get_unread_mail('Inbox')
    logger.debug('Checking for attachments and downloading...')
    for mail in emails:
        mail_account_connection.download_attachment(mail)
    logger.debug('Complete.')


if __name__ == '__main__':
    download_latest_mail_attachments()
