#coding: utf-8

import common   as com
import datetime as dt
import json
import hashlib
import mail
import os
import requests
import sensor   as s
import threading
import time
import uptime

last_alerted = 0
last_reported = 0

QUEUE = '/opt/winecave/queue/'

def enqueue(obj):
    try:
        with open('{0}{1}'.format(QUEUE, hashlib.md5(str(obj).encode()).hexdigest()), 'w') as f:
            f.write(json.dumps(obj))
    except Exception as e:
        com.error(traceback.format_exc())
        com.error(str(e))

def regist_data(type, value):
    api_url = 'http://edisoner.com/api/regist2.php'
    headers = {'content-type': 'application/json'}
    payload = {'type': type, 'value': round(value, 2), 'timestamp': dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    enqueue(payload)
#    response = requests.post(api_url, data=json.dumps(payload), headers=headers)
#    com.info('response: {0}'.format(response.text))

def alert():
    global last_alerted
    # エラー発報は1時間に1回とする
    if time.time() - last_alerted > 3600:
        subject = 'sensor error [{0}]'.format(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        body_text = 'I2C Error occured.'
        mail.sendmail('koichi.inokuchi@gmail.com', subject, body_text)
        last_alerted = time.time()
        com.warn('alert mail fired !')

def report(t, h):
    global last_reported
    # 通知1時間に1回とする
    if time.time() - last_reported > 3595:
        stat = os.statvfs('/')
        free = int(stat.f_bavail * stat.f_frsize // 1024 // 1024)
        total = int(stat.f_blocks * stat.f_frsize // 1024 // 1024)
        used = int((stat.f_blocks - stat.f_bfree) * stat.f_frsize // 1024 //1024)
        subject = '[{0}] sensor status report'.format(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        body_text = []
        body_text.append('sensor status at {0}'.format(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        body_text.append('    system uptime: {0:d} days {1:d} hour {2:d} min'.format(
            int(uptime.uptime()//86400),
            int(uptime.uptime()%86400//3600),
            int(uptime.uptime()%3600//60)))
        body_text.append('    file system total: {0:,d} MB'.format(total))
        body_text.append('    file system used : {0:,d} MB ({1:.1f}%)'.format(used, used * 100 / total))
        body_text.append('    file system avail: {0:,d} MB ({1:.1f}%)'.format(free, free * 100 / total))
        body_text.append('    temperature  : {0:.2f} C'.format(t))
        body_text.append('    humidity     : {0:.2f} %'.format(h))
        mail.sendmail('koichi.inokuchi@gmail.com', subject, '\n'.join(body_text))
        last_reported = time.time()
        com.info('report mail fired !')
    else:
        com.info('report mail skiped !')

def process():
    t = s.get_temperature()
    error = False

    if t != s.ERROR:
        regist_data('T', t)
        com.info('{0:.2f} C'.format(t))
    else:
        com.error('I2C error')
        error = True

    p = s.get_pressure()
    if p != s.ERROR:
        regist_data('P', p)
        com.info('{0:.2f} hPa'.format(p))
    else:
        com.error('I2C error')
        error = True

    h = s.get_humidity()
    if h != s.ERROR:
        regist_data('H', h)
        com.info('{0:.2f} %'.format(h))
    else:
        com.error('I2C error')
        error = True

    if error:
       alert()
    else:
        report(t, h)
    com.info('-' * 60)

# ------------------------------------------------------------------------------
# program main
com.info('----- Wine cave monitor started.')

if __name__ == '__main__': 
    com.info('Wine cave monitor started.')
    AJUST = 0.060
    while True:
        t0 = time.time()
        th = threading.Thread(target=process)
        th.start()
        t1 = time.time()
        com.info('sleep for {0:.6f} seconds'.format(60 - (t1 - t0) - AJUST))
        time.sleep(60 - (t1 - t0) - AJUST)

