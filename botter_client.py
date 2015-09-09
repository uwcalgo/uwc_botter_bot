#!/usr/bin/env python

import sys
import json
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


def get_and_reply():
    response = requests.get(BASE_URL + 'getUpdates')
    if response.status_code == 200:
        dict_repr = json.loads(response.text)
        results = dict_repr['result']
        for result in results:
            update_id = result['update_id']
            message = result['message']
            if 'text' in message:
                # we're dealing with a text messages
                user = message['from']
                print("from:", user, "text", message['text'])
                response = dict(chat_id=user['id'],
                                text='Hello {}'.format(user['first_name']))
                print(json.dumps(response))
                outcome = requests.post(BASE_URL + 'sendMessage', data=response)
                if outcome.status_code == 200:
                    print("Yay, message sent")
                else:
                    print(outcome, outcome.text)
    else:
        sys.exit(response)
if __name__ == '__main__':
    get_and_reply()
