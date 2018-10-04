[![Build Status](https://travis-ci.com/orlandodiaz/googlemail.svg?branch=master)](https://travis-ci.com/orlandodiaz/googlemail)

### Description
High-level interface for sending email through googlemail.

### Usage

Create conf.py and fill in your email and password credentials. Ex:

    email = 'your.email@gmail.com'
    password = 'your.pass'   

Create googlemail object:
    
    gmail = Gmail(email, password)
    
 Start the server and login
 
    gmail.start_server()
    gmail.login()
    
 Create a simple template dictionary with the email header and body
 
    mail_template = {
        'from': 'fromsender@gmail.com',
        'to': 'tosender@gmail.com',
        'subject':  'Cool subject email',
        'body': """
        HTML template or the like
        """
    }
    
 Send the message
 
    gmail.send_msg(mail_template)

## Testing
To run the tests you need to configure the sender username, password, and recipient email. You can test locally or use a continous integration service like Jenkins
which allow you to host using a fixed static IPs. Travis-CI does their tests on multiple server causing Google to flag the account, making the tests worthless

    $ export GOOGLEMAIL_EMAIL=<YOUR SENDER EMAIL>
    $ export GOOGLEMAIL_PASSWORD=<YOUR SENDER PASSWORD>

    $ export GOOGLEMAIL_TESTEMAIL=<YOUR TEST RECIPIENT EMAIL>

