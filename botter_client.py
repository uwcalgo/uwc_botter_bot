#!/usr/bin/env python

import sys
from ConfigParser import SafeConfigParser
import requests

config = SafeConfigParser()
config.read(['botter_sample.ini',
             'botter.ini'])

global_config = 'global'
global_key_option = 'key'

if config.has_option(global_config, global_key_option):
    key = config.get(global_config, global_key_option)
else:
    sys.exit("Need an API key")

BASE_URL = 'https://api.telegram.org/bot{}/'.format(key)


def get_me():
    response = requests.get(BASE_URL + 'getMe')
    if response.status_code == 200:
        print(response.text)
    else:
        sys.exit(response)

if __name__ == '__main__':
    get_me()
