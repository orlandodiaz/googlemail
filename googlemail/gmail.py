import smtplib
import socket
import os
from email.mime.multipart  import MIMEMultipart
from email.mime.text import MIMEText
from textwrap import dedent
from smtplib import SMTPAuthenticationError, SMTPSenderRefused
if __name__ == '__main__':
    from config import log
else:
    from .config import log


class Gmail(object):
    """Higher level SMTP object for sending emails through gmail"""

    def __init__(self, user, password):
        self.GMAIL_USERNAME = user
        self.GMAIL_PASSWORD = password

        self.host = socket.gethostbyname('smtp.googlemail.com')
        self.port = 587  # 465 SSL, 587 NORMAL
        self.server = None
        self.is_loggedin = False

        self.start_server()

    def __str__(self):
        return 'Username: {} \n Password: {} \n Host: {} \n Port: {} \n'.format(self.GMAIL_USERNAME,
                                                                                self.GMAIL_PASSWORD,
                                                                                self.host, self.port)
    def __repr__(self):
        return 'Gmail({0}, {1})'.format(self.GMAIL_USERNAME, self.port)

    def start_server(self):
        """ Starts the server object. this may take a while"""

        log.info('Creating server object')

        try:
            self.server = smtplib.SMTP(self.host, self.port)
            # self.server = smtplib.SMTP_SSL(self.host, self.port)
            # self.server.set_debuglevel(1)
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
        except Exception as ex:
            log.error(ex)
        else:
            log.debug("Server started with host {} and port {}".format(self.host, self.port))

    def login(self):
        """ Try and log in into googlemail """

        log.info('Logging in to googlemail server as {}'.format(self.GMAIL_USERNAME))
        try:
            self.server.login(self.GMAIL_USERNAME, self.GMAIL_PASSWORD)
        except SMTPAuthenticationError as ex:
            # print(ex)
            log.error("Username or password is incorrect")
            log.error("GOOGLEMAIL_EMAIL: {}".format(os.environ['GOOGLEMAIL_EMAIL']))
            log.error("GOOGLEMAIL_PASSWORD: {}".format(os.environ['GOOGLEMAIL_PASSWORD']))
            log.error("GOOGLEMAIL_TESTMAIL: {}".format(os.environ['GOOGLEMAIL_TESTEMAIL']))


            raise
        except SMTPSenderRefused as ex:
            log.error("Google blocking login. Go to your gmail and allow access from this location")
            raise

        else:
            self.is_loggedin = True

    def send_msg_with_template(self, template):
        """ Send message with given template"""

        # Store information to the msg MIME object
        msg = MIMEMultipart()
        msg['To'] = template['to']
        msg['Subject'] = template['subject']
        template['body'] = dedent(template['body'])  # fix wacky indentation
        body = template['body']


        msg.attach(MIMEText(body, 'plain'))

        text = msg.as_string()

        log.debug('Sending email')
        try:
            self.server.sendmail(self.GMAIL_USERNAME, template['to'], text)
        except Exception as ex:
            log.error(ex)
        else:
            log.info('Email was sent succesfully')

    def send_msg(self, recipient, subject='', body=''):
        body = MIMEText(body)
        body['Subject'] = subject
        try:
            self.server.sendmail(from_addr=self.GMAIL_USERNAME, to_addrs=recipient, msg=body.as_string())
        except Exception as ex:
            log.error(ex)
        else:
            log.info('Email was sent succesfully')

    def close_server(self):
        self.server.quit()
