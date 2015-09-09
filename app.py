#!/usr/bin/env python

import json
from ConfigParser import SafeConfigParser
from flask import Flask, Response, render_template, abort, request, redirect
from werkzeug.debug import DebuggedApplication
from telegram_models import User

config = SafeConfigParser()
config.read(['botter_sample.ini', 'botter.ini'])
global_config = 'global'
global_debug_option = 'debug'

app = Flask(__name__)

BOT_ID = '126927261'
BOT_NAME = 'uwc_botter_bot'

if config.has_option(global_config, global_debug_option):
    debug = config.getboolean(global_config, global_debug_option)
    if debug:
        app.debug = True
        app.wsgi_app = DebuggedApplication(app.wsgi_app, True)


@app.route('/')
def hello():
    hello = {'hello': 'world'}
    return Response(json.dumps(hello), mimetype='application/json')

# methods to implement:
#getMe
#sendMessage
#forwardMessage
#sendPhoto
#sendAudio
#sendDocument
#sendSticker
#sendVideo
#sendVoice
#sendLocation
#sendChatAction
#getUserProfilePhotos
#getUpdates
#setWebhook

@app.route('/getMe', methods=['GET', 'POST'])
def get_me():
    response = json.dumps(dict(ok='true', result=User(id=BOT_ID, first_name=BOT_NAME, username=BOT_NAME).to_dict()))
    return Response(response, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
