# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.0 (default, Nov  6 2019, 15:49:01) 
# [Clang 4.0.1 (tags/RELEASE_401/final)]
# Embedded file name: /Users/slothyubo/Desktop/git-repo/gmailer-python/gmailer_python/gmailer.py
# Compiled at: 2021-02-15 00:38:06
# Size of source mod 2**32: 3169 bytes
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from typing import Dict, Final, List, NoReturn, Optional, Union

class Gmailer:
    MAIL_PARAMS = [
     'Subject', 'From', 'To', 'Bcc', 'Date']
    MAIL_PARAMS: Final[List[str]]

    def __init__(self, from_addr: str, pwd: str, debug: bool=False) -> NoReturn:
        self.from_addr = from_addr
        self.pwd = pwd
        self.debug_mode = debug

    def create_msg(self, to_addr: Optional[str]=None, body: Optional[str]=None, cc: Optional[str]=None, bcc: Optional[str]=None, subject: Optional[str]=None) -> MIMEText:
        to_addr, body, cc, bcc, subject = self._set_all(to_addr=to_addr, body=body, bcc=bcc, subject=subject)
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.from_addr
        msg['To'] = to_addr
        msg['Cc'] = cc
        msg['Bcc'] = bcc
        msg['Date'] = formatdate()
        return msg

    def send(self, to_addr, body: Optional[str]=None, cc: Optional[str]=None, bcc: Optional[str]=None, subject: Optional[str]=None):
        msg = self.create_msg(to_addr=to_addr, body=body, cc=cc, bcc=bcc, subject=subject)
        smtpobj = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
        if self.debug_mode:
            smtpobj.set_debuglevel(2)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        smtpobj.login(self.from_addr, self.pwd)
        smtpobj.sendmail(self.from_addr, to_addr, msg.as_string())
        smtpobj.close()

    def _set_body(self, body: Union[(None, str)]) -> str:
        if body is None:
            body = ''
        if not isinstance(body, str):
            raise ValueError(f"expect str, but {type(body)}")
        return body

    def _set_to_addr(self, to_addr: Union[(None, str)]) -> str:
        if to_addr is None:
            to_addr = ''
        if not isinstance(to_addr, str):
            raise ValueError(f"expect str, but {type(to_addr)}")
        return to_addr

    def _set_cc(self, cc: Union[(None, str)]) -> str:
        if cc is None:
            cc = ''
        if not isinstance(cc, str):
            raise ValueError(f"expect str, but {type(cc)}")
        return cc

    def _set_bcc(self, bcc: Union[(None, str)]) -> str:
        if bcc is None:
            bcc = ''
        if not isinstance(bcc, str):
            raise ValueError(f"expect str, but {type(bcc)}")
        return bcc

    def _set_subject(self, subject: Union[(None, str)]) -> str:
        if subject is None:
            subject = ''
        if not isinstance(subject, str):
            raise ValueError(f"expect str, but {type(subject)}")
        return subject

    def _set_all(self, to_addr: Optional[str]=None, body: Optional[str]=None, cc: Optional[str]=None, bcc: Optional[str]=None, subject: Optional[str]=None) -> NoReturn:
        to_addr = self._set_to_addr(to_addr=to_addr)
        body = self._set_body(body=body)
        cc = self._set_cc(cc=cc)
        bcc = self._set_bcc(bcc=bcc)
        subject = self._set_subject(subject=subject)
        return (
         to_addr, body, cc, bcc, subject)
# okay decompiling __pycache__/gmailer.cpython-38.pyc
