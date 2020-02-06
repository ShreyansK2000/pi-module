import os, requests, uuid, json, sys

obj_detect_subscription_key = "4de40c2867a54d2381f77ac810c2035f"
obj_detect_analyze_url = "https://7bvision.cognitiveservices.azure.com/vision/v2.1/detect"

translation_subscription_key = '3dab74dced954bd3a6d6bdd34dd77d96'
translation_endpoint = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'

def translate(input, language):
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

    f = open("image_response.txt","w+")
    f.write(str(response.json()))

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    #print(analysis)

    return analysis