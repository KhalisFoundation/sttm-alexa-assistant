#!/usr/bin/env python3.7.7
import logging
import banidb
import better_translit as bt
from flask import Flask, request

app = Flask(__name__)

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    type = req.get('request').get('type')
    json = {
            "version": "1.0",
            "response": {
                "outputSpeech": {},
                "reprompt": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "Can I help you with anything?"
                    }
                },
                "shouldEndSession": False
            }
        }
    if (type=='LaunchRequest'):
        output = {
            "type": "SSML",
            "text": "Waheguru ji ka Khalsa, Waheguru ji ki Fateh?",
            "ssml": "<speak><phoneme alphabet=\"ipa\" ph=\"ʋɑhɪGʊru d͡ʒi kɑ kʰɑlsa, ʋɑhɪGʊru d͡ʒi ki fət̪eh\">Waheguru ji ka Khalsa, Waheguru ji ki Fateh</phoneme></speak>"
        }
        json['response']['outputSpeech'] = output
    elif (type=='IntentRequest'):
        intent = req.get('intent').get('name')
        if (intent=='Random_Shabad'):
            random_shabad = bt.better(banidb.random()['verses'][0]['verse'])
            msg = f"Waheguru ji, Here is Random Shabad {random_shabad}"
            output = {
                "type": "SSML",
                "text": random_shabad,
                "ssml": msg
            }
            json['response']['outputSpeech'] = output
    return json


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)