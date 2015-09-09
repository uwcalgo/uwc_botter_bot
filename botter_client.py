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
global_state_option = 'statefile'

if config.has_option(global_config, global_key_option):
    key = config.get(global_config, global_key_option)
else:
    sys.exit("Need an API key")

config.base_url = 'https://api.telegram.org/bot{}/'.format(key)


def get_me(config):
    response = requests.get(config.base_url + 'getMe')
    if response.status_code == 200:
        print(response.text)
    else:
        sys.exit(response)


def get_and_reply(config):
    if config.has_option(global_config, global_state_option):
        statefile_filename = config.get(global_config, global_state_option)
    else:
        statefile_filename = 'state.json'

    try:
        input_file = open(statefile_filename, 'rb')
    except IOError:
        state = dict()
    else:
        state = json.load(input_file)

    next_message_id = state.get('last_message_id', 0) + 1
    request_params = dict(offset=str(next_message_id))
    response = requests.get(config.base_url + 'getUpdates', params=request_params)
    if response.status_code == 200:
        dict_repr = json.loads(response.text)
        results = dict_repr['result']
        for result in results:
            update_id = result['update_id']
            last_message_id = update_id
            message = result['message']
            if 'text' in message:
                # we're dealing with a text messages
                user = message['from']
                print("from:", user, "text", message['text'])
                response = dict(chat_id=user['id'],
                                text='Hello {}'.format(user['first_name']))
                print(json.dumps(response))
                outcome = requests.post(config.base_url + 'sendMessage', data=response)
                if outcome.status_code == 200:
                    print("Yay, message sent")
                else:
                    print(outcome, outcome.text)
            state['last_message_id'] = last_message_id
        with open(statefile_filename, 'wb') as output_file:
            json.dump(state, output_file)
    else:
        sys.exit(response)

if __name__ == '__main__':
    get_and_reply(config)
