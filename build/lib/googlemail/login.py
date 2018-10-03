from .gmail import Gmail

def login(username, password):
    gmail = Gmail(username, password)
    gmail.login()
    return gmail