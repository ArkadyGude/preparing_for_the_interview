import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser


class EmailClient:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def send_message(self, server, port, recipients, subject, message):
        try:
            email_message = MIMEMultipart()
            email_message['From'] = self.login
            email_message['To'] = ', '.join(recipients)
            email_message['Subject'] = subject
            email_message.attach(MIMEText(message))
            send_mail = smtplib.SMTP(server, port)
            send_mail.ehlo()
            send_mail.starttls()
            send_mail.ehlo()
            send_mail.login(self.login, self.password)
            result = send_mail.sendmail(email_message['From'], email_message['To'], email_message.as_string())
            send_mail.quit()

        except Exception as e:
            return f'Failed to send email: {e}'

        return result

    def receive_mail(self, server, mailbox, header=None):
        receive_mail = imaplib.IMAP4_SSL(server)

        try:
            receive_mail.login(self.login, self.password)
            receive_mail.list()
            receive_mail.select(mailbox)
            criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
            result, data = receive_mail.uid('search', None, criterion)
            assert data[0], 'There are no letters with current header'
            latest_email_uid = data[0].split()[-1]
            print(latest_email_uid.decode('utf-8'))
            result, data = receive_mail.uid('fetch', latest_email_uid.decode('utf-8'), '(RFC822)')
            raw_email = data[0][1]
            email_result_receive = email.message_from_string(raw_email.decode('utf-8'))
            receive_mail.logout()
        except Exception as e:
            return f'Failed to receive email:{e}'

        return email_result_receive


def main():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    login = config['Settings']['login']
    password = config['Settings']['password']
    mailbox = config['Settings']['mailbox']
    port = config['Settings']['port']
    server = config['Settings']['server']

    gmail = EmailClient(login, password)
    print(gmail.send_message(
        server,
        port,
        ['...@.ru', '...@.com', '...@.ru'],
        'Тема сообщения',
        'Текст сообщения'
    ))
    print(gmail.receive_mail(server, mailbox))


if __name__ == '__main__':
    main()
