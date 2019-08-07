# coding: utf-8
#
# created: 2018.10.23
# author : k.inokuchi
#

import datetime as dt
import json
from os.path import exists
from time    import time

LEVEL = ['DEBUG', 'INFO', 'WARN', 'ERROR']

# ------------------------------------------------------------------------------
# decorator -- record elapsed time
# ------------------------------------------------------------------------------
def time_record(func):
    def wrapper(*args, **kwargs):
        try:
            ret = None
            t0 = time()
            ret = func(*args, **kwargs)
            t1 = time()
        except Exception as e:
            error(traceback.format_exc())
            t1 = time()
        finally:
            info('function [{0}] elapsed: {1:.6f}'.format(func.__name__, t1 - t0))
            return ret

    return wrapper

def get_config(name):
    if not exists('/opt/winecave/conf/{0}.conf'.format(name)):
        return False
    with open('/opt/winecave/conf/{0}.conf'.format(name), 'r') as f:
        return json.load(f)

def get_loglevel():
    obj = get_config('log')

    if obj:
        return obj['level']
    else:
        return 1

def log(level, msg):
    if level < get_loglevel():
        return
    with open('/opt/winecave/log/app.log', 'a') as f:
        f.write('{0} [{1}] {2}\n'.format(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), LEVEL[level], msg))

def debug(msg):
    log(0, msg)

def info(msg):
    log(1, msg)

def warn(msg):
    log(2, msg)

def error(msg):
    log(3, msg)

if __name__ == '__main__':
    debug('this is debug message')
    info('this is info message')
    warn('this is warn message')
    error('this is error message')
