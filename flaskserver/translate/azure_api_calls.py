import os, requests, uuid, json, sys, time
from xml.etree import ElementTree

obj_detect_subscription_key = "4de40c2867a54d2381f77ac810c2035f"
obj_detect_analyze_url = "https://7bvision.cognitiveservices.azure.com/vision/v2.1/detect"

translation_subscription_key = '3dab74dced954bd3a6d6bdd34dd77d96'
translation_endpoint = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'

t2s_subscription_key = "64ed66f8f5124a53be448e98d0da203a"
t2s_endpoint = 'https://westus2.tts.speech.microsoft.com/cognitiveservices/v1'

def api_translate(input, language):
    params = '&to=' + language
    constructed_url = translation_endpoint + params

    headers = {
        'Ocp-Apim-Subscription-Key': translation_subscription_key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'text': input
    }]

    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    #print(response[0])

    return response[0]


def detect_objects(image_data):
    global obj_detect_subscription_key
    global obj_detect_analyze_url

    headers = {'Ocp-Apim-Subscription-Key': obj_detect_subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}

    response = requests.post(obj_detect_analyze_url,
                             headers=headers,
                             params=params,
                             data=image_data)
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    return response.json()

# call this function for each word in the objects detected json
def text_to_speech(tts, language_code, voice_code):
    access_token = None
    fetch_token_url = "https://westus2.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers = {
        'Ocp-Apim-Subscription-Key': t2s_subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = str(response.text)

    save_audio_headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
        'User-Agent': '7b'
    }

    xml_body = ElementTree.Element('speak', version='1.0')
    xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
    voice = ElementTree.SubElement(xml_body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', language_code)
    voice.set('name', voice_code) # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
    voice.text = tts
    body = ElementTree.tostring(xml_body)

    response = requests.post(t2s_endpoint, headers=save_audio_headers, data=body)
    if response.status_code == 200:
        with open('Sound/response' + str(0) + '.wav', 'wb') as audio:
            audio.write(response.content)
            print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
    else:
        print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
        print("Reason: " + str(response.reason) + "\n")