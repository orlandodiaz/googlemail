### Description
High-level interface for sending email through gmail.

### Usage

Create cred.py and fill in your email and password credentials. Ex:

    email = 'your.email@gmail.com'
    password = 'your.pass'   

Create gmail object:
    
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
    