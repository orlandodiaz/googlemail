from conf import EMAIL, PASSWORD, TEST_EMAIL
from googlemail import Gmail
import pytest

@pytest.fixture(scope="class")
def gmail():
    gmail = Gmail(EMAIL, PASSWORD)
    gmail.login()
    yield gmail
    gmail.close_server()


def test_send_msg_with_template(gmail):
    mail_template = {
        'to': TEST_EMAIL,
        'subject': 'test_send_msg_with_template::PASSED',
        'body':
        """
        googlemail::test_send_msg_with_template::PASSED
        
        """
    }

    gmail.send_msg_with_template(mail_template)

def test_send_msg(gmail):
    gmail.send_msg(TEST_EMAIL, subject="googlemail::test_send_msg::PASSED", body="googlemail::test_send_msg::PASSED")



