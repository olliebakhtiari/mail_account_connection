# Local.
from settings import USERNAME, PASSWORD, MAIL_SERVER
from src.mail_account_connection import MailAccountConnection


def download_latest_mail_attachments():
    mail_account_connection = MailAccountConnection(MAIL_SERVER, USERNAME, PASSWORD)
    emails = mail_account_connection.get_unread_mail()
    for mail in emails:
        mail_account_connection.download_attachment(mail)


if __name__ == '__main__':
    download_latest_mail_attachments()
