# -*- coding: utf-8 -*-
import os, requests, uuid, json, sys

def translate (phrase, language):

    subscription_key = '3dab74dced954bd3a6d6bdd34dd77d96'

    endpoint = 'https://api.cognitive.microsofttranslator.com/'

    path = '/translate?api-version=3.0'
    params = '&to=' + language
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': phrase
    }]


    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    
    return response[0]['translations'][0]['text']
