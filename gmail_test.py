from gmailer_python import Gmailer
try:
    from config import GMAIL_ADDR, GMAIL_PWD
    your_addr = GMAIL_ADDR
    your_pwd = GMAIL_PWD
except ImportError:
    your_addr = input('Your Gmail Addrress is: ')
    your_pwd = input('Your Gmail Password is: ')

gmailer = Gmailer(your_addr, your_pwd, debug=True)
msg = gmailer.create_msg(your_addr, 'For attachment file test')
msg = gmailer.attach_file(msg=msg, path='test.csv', ext='csv')
gmailer.send(msg=msg)