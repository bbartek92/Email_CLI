import smtplib
import ssl
import imaplib
import email
import re

class Connector:
    def __init__(self, email, password, smtp_server, smtp_port,
                 imap_server, imap_port):
        self.EMAIL = email
        self.PASSWORD = password
        self.SMTP_SERVER = smtp_server
        self.SMTP_PORT = smtp_port
        self.IMAP_SERVER = imap_server
        self.IMAP_PORT = imap_port
        self.context = ssl.create_default_context()

    def write(self, receiver, message):
        server = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
        try:
            server.starttls(context=self.context)
            server.login(self.EMAIL, self.PASSWORD)
            server.sendmail(self.EMAIL, receiver, message.as_string())
        except Exception as e:
            print(e)
        finally:
            server.quit()

    def read(self):
        server = imaplib.IMAP4_SSL(self.SMTP_SERVER)
        emails = {}
        try:
            server.login(self.EMAIL, self.PASSWORD)
            server.select('inbox')
            type, data = server.search(None, 'ALL')
            id_list = data[0].split()
            first_email_id = int(id_list[0])
            last_email_id = int(id_list[-1])
            pattern = re.compile('<.*@.*>')

            for num in range(last_email_id, first_email_id-1, -1):
                typ, data = server.fetch(str(num), '(RFC822)')
                dat = data[0][1].decode(encoding='UTF-8')
                msg = email.message_from_string(dat)
                from_info = msg['From']
                match = pattern.findall(from_info)
                if len(match):
                    emails[num] = [msg['Subject'], match[0]]
                else:
                    emails[num] = [msg['Subject'], msg['From']]
        except Exception as e:
            print(e)
        finally:
            server.logout()

        return emails