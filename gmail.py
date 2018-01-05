# Name: Gmail sender
# Description: Higher-level interface for sending gmail
# Creating a server object to smtp.gmail.com will take minutes. Use the socket method
# attached below

# Copyright 2018 Orlando Reategui

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import smtplib
from log import log
import socket
from email.mime.multipart  import MIMEMultipart
from email.mime.text import MIMEText
from textwrap import dedent
from cred import email, password


class Gmail(object):
    """higher level gmail object for sending emails"""
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.host = socket.gethostbyname('smtp.gmail.com')
        self.port = 587  # 465 SSL, 587 NORMAL
        self.server = None

    def __str__(self):
        return 'Username: {} \n Password: {} \n Host: {} \n Port: {} \n'.format(self.username, self.password,
                                                                                self.host, self.port)

    def __repr__(self):
        return 'Gmail({0}, {1})'.format(self.username, self.password)

    def start_server(self):
        """ start the server object. this may take a while"""
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
        """ try and log in into gmail"""

        log.info('Logging in to gmail server as {}'.format(self.username))
        try:
            self.server.login(self.username, self.password)
        except Exception as ex:
            log.error(ex)

    def send_msg(self, template):
        """ send message with given template"""

        # Store information to the msg MIME object
        msg = MIMEMultipart()
        msg['From'] = template['from']
        msg['To'] = template['to']
        msg['Subject'] = template['subject']
        template['body'] = dedent(template['body'])  # fix wacky indentation
        body = template['body']
        msg.attach(MIMEText(body, 'plain'))

        text = msg.as_string()

        log.debug('Sending email')
        try:
            self.server.sendmail(self.username, template['to'], text)
        except Exception as ex:
            log.error(ex)
        else:
            log.info('Email was sent succesfully')

    def quit(self):
        self.server.quit()


if __name__ == '__main__':

    # Create gmail object
    gmail = Gmail(email, password)
    gmail.start_server()
    gmail.login()

    mail_template = {
        'from': 'fromsender@gmail.com',
        'to': 'tosender@gmail.com',
        'subject':  'Cool subject email',
        'body': """
        HTML template or the like
        """
    }

    gmail.send_msg(mail_template)

