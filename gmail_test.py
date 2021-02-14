from gmailer_python import Gmailer

your_addr = input('Your Gmail Addrress is: ')
your_pwd = input('Your Gmail Password is: ')
gmailer = Gmailer(your_addr, your_pwd, debug=True)
gmailer.send(your_addr, 'For Test')