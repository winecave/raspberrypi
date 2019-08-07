# -*- coding: UTF-8 -*-
#
# Alert Mail Sender Program
#
# created  : 2018.10.23
# modified : ----.--.--
#
# author   : inokuchi koichi
#
# c 2000 - 2018 FreeBit Co., Ltd. All Rights Reserved.

import datetime           as dt
import common             as com
import smtplib
from email.header         import Header
from email.mime.text      import MIMEText
from email.mime.multipart import MIMEMultipart

# --------------------------------------------------------------------------------
# 添付なしメール送信
# --------------------------------------------------------------------------------
def sendmail(to_addr, subject, body_text, from_addr='monitor@oberyo.nir.jp'):
    msg = MIMEMultipart()
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = from_addr
    msg['To'] = to_addr

    msg.attach(MIMEText(body_text, 'plain', 'utf-8'))

    conf = com.get_config('mail')
    s = smtplib.SMTP_SSL(conf['host'], conf['port'])
    s.login(conf['user'], conf['passwd'])
    s.sendmail(from_addr, to_addr.split(','), msg.as_string())
    s.quit()
# --------------------------------------------------------------------------------

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 1:
        sendmail('koichi.inokuchi@gmail.com', 'temperature alert', 'This is mail body')
    else:
        for arg in argv:
            print(arg)
        sendmail(argv[1], argv[2], argv[3], 'k.inokuchi@freebit.net')
