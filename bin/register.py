#coding: utf-8

import common   as com
import json
import requests
import traceback
from os      import walk
from os      import remove
from os.path import join
from time    import sleep


QUEUE = '/opt/winecave/queue/'

def find_all_files(directory):
    for root, dirs, files in walk(directory):
        for file in files:
            yield join(root, file)

@com.time_record
def regist_data(payload):
    try:
        api_url = 'http://edisoner.com/api/regist2.php'
        headers = {'content-type': 'application/json'}
        response = requests.post(api_url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            com.info('response: {0}'.format(response.text))
            data = json.loads(response.text)
            if data['code'] == 200:
                return True
            else:
                com.error('response: {0}'.format(response.text))
                return False
        else:
            com.error('http status error {0}'.format(response.status_code))
    except Exception as e:
        com.error(str(e))
        com.error(traceback.format_exc())
        return False

def process():
    sleep(5)
    files = find_all_files(QUEUE)
    for path in files:
        with open(path) as f:
            payload = json.load(f)
            if regist_data(payload):
                remove(path)
                com.info('{0} removed.'.format(path)) 
# ------------------------------------------------------------------------------
# program main
if __name__ == '__main__': 
    process()
    com.info('-' * 60)
