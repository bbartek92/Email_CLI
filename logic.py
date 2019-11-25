import json
import connector
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

class Config:
    def __init__(self):
        config = self.read_json()
        self.sender_email = config['sender_email']
        self.smtp_server = config['smtp_server']
        self.smtp_port = config['smtp_port']
        self.imap_server = config['imap_server']
        self.imap_port = config['imap_port']

    def read_json(self):
        with open('config.json') as f:
            config = json.load(f)
        return config

    def get_sender(self):
        return self.sender_email

    def get_smtp_info(self):
        return self.smtp_server, self.smtp_port

    def get_imap_info(self):
        return self.imap_server, self.imap_port

class MailBox:
    def __init__(self):
        config = Config()
        sender_email =config.get_sender()
        smtp_server, smtp_port = config.get_smtp_info()
        imap_server, imap_port = config.get_imap_info()
        password = getpass.getpass()
        self.conn = connector.Connector(sender_email, password,
                                        smtp_server, smtp_port,
                                        imap_server, imap_port)

    def write(self):
        message = MIMEMultipart("alternative")
        print('Email:')
        message['Subject'] = input('Subject: ')
        receiver = input('Receiver: ')
        message['To'] = receiver
        text = input('Message:  ')
        part = MIMEText(text, 'plain')
        message.attach(part)
        self.conn.write(receiver, message)
        print("\nemail sent")

    def read(self):
        emails = self.conn.read()
        padding1 = 70
        padding2 = 45
        print('+', '-' * padding1, '+', '-' * padding2, '+', sep='')
        print('|', '{var: <{pad}}'.format(var='Subject', pad=padding1), '|',
              '{var: <{pad}}'.format(var='From', pad=padding2),
              '|', sep='')
        print('+', '-' * padding1, '+', '-' * padding2, '+', sep='')
        for num, email in emails.items():
            print('|', '{var: <{pad}}'.format(var=email[0], pad=padding1), '|',
                  '{var: <{pad}}'.format(var=email[1], pad=padding2),
                  '|', sep='')
            print('+', '-' * padding1, '+', '-' * padding2, '+', sep='')

    def auto(self):
        text = input("Set automatic reply: ")
        emails = self.conn.read()
        email_list = [*emails]
        while True:
            time.sleep(10)
            new_emails = self.conn.read()
            new_email_list = [*new_emails]
            for email in new_email_list:
                if email not in email_list:
                    print(email, 'is new email')
                    print('Subject', new_emails[email][0])
                    print('To', new_emails[email][1])
                    print(text)
                    message = MIMEMultipart("alternative")
                    message['Subject'] = 'Re: ' + new_emails[email][0]
                    receiver = new_emails[email][1]
                    message['To'] = receiver
                    part = MIMEText(text, 'plain')
                    message.attach(part)
                    self.conn.write(receiver, message)
                    print("\nemail sent")
            check = input('Continue sending or stop? (Y|N) ')
            if check != 'Y':
                break