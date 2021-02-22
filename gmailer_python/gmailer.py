import smtplib
from email import encoders, utils
from email.utils import formatdate
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Final, List, NoReturn, Optional, Tuple, Union

class Gmailer:
    MAIL_PARAMS: Final[List[str]] = ['Subject', 'From', 'To', 'Cc', 'Bcc', 'Date']

    def __init__(self, from_addr: str, pwd: str, debug: bool=False) -> NoReturn:
        self.from_addr = from_addr
        self.pwd = pwd
        self.debug_mode = debug

    def create_msg(self, to_addr: Optional[str]=None, body: Optional[str]=None,
                    cc: Optional[str]=None, bcc: Optional[str]=None, subject: Optional[str]=None) -> MIMEText:
        to_addr, body, cc, bcc, subject = self._set_all(to_addr=to_addr, body=body, bcc=bcc, subject=subject)
        msg = MIMEMultipart()
        body = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.from_addr
        msg['To'] = to_addr
        msg['Cc'] = cc
        msg['Bcc'] = bcc
        msg['Date'] = formatdate()
        msg.attach(body)
        return msg

    def attach_file(self, msg: MIMEText, path: str, ext: Optional[str]=None,
                    filename: Optional[str]=None) -> MIMEText:
        if filename is None:
            filename = path.split('/')[-1]
        if ext is None:
            ext = filename.split('.')[-1]
        
        attachment = MIMEBase('text', ext)
        with open(file=path, mode='rb') as f:
            attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)
        return msg

    def send(self, to_addr: Optional[str]=None, body: Optional[str]=None, cc: Optional[str]=None,
            bcc: Optional[str]=None, subject: Optional[str]=None, msg: Optional[MIMEText]=None) -> NoReturn:

        if msg is None and to_addr is None:
            raise ValueError('You need to_addr or msg')

        if msg is None:
            msg = self.create_msg(to_addr=to_addr, body=body, cc=cc, bcc=bcc, subject=subject)
        if to_addr is None:
            to_addr = msg['To']
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

    def _set_all(self, to_addr: Optional[str]=None, body: Optional[str]=None,
                cc: Optional[str]=None, bcc: Optional[str]=None, subject: Optional[str]=None) -> Tuple[str]:
        to_addr = self._set_to_addr(to_addr=to_addr)
        body = self._set_body(body=body)
        cc = self._set_cc(cc=cc)
        bcc = self._set_bcc(bcc=bcc)
        subject = self._set_subject(subject=subject)
        return (
            to_addr, body, cc, bcc, subject
        )
