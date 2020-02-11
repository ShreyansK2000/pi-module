from flask import Flask, jsonify, request, send_file
import numpy as np
import cv2
import os
import azure_api_calls as api
import draw

app = Flask(__name__)

language_codes ={
    'english': 'en-us',
    'french': 'fr-fr',
    'german': 'de-de',
    'spanish': 'es-es'
    }

voice_codes = {
    'english': 'en-US-BenjaminRUS',
    'french': 'fr-FR-Paul-Apollo',
    'german': 'de-DE-Hedda',
    'spanish': 'es-ES-Laura-Apollo'
    }

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"newTest": "TEST"})

@app.route('/translate', methods=['GET'])
def translate():
    target_language = request.args.get('target_language')
    
    # get codes for text to speech playback
    language_code, voice_code = get_t2s_codes(target_language);

    frame = get_frame()
    filename = "test_output_translate.jpeg"
    cv2.imwrite(filename, frame)
    image_data = open(filename, "rb").read()

    # detect the objects in the image
    analysisJson = api.detect_objects(image_data)

    # draw bounding boxes on all the images
    objects = analysisJson['objects']
    draw.boundingBoxes(frame, objects)

    # find translation of detected objects for target language
    objectCount = 0
    for detectedObject in objects:
        translation = api.translate(detectedObject['object'],
                                    language_code)['translations'][0]['text']
        api.text_to_speech(translation, objectCount, language_code, voice_code)
        analysisJson['objects'][objectCount]['translation'] = translation
        objectCount += 1

    analysisJson['targetLanguage'] = target_language

    return jsonify({"azure_output": analysisJson})

@app.route('/get_file', methods=['GET'])
def get_img():
    frame = get_frame()
    filename = "test_output_get_file.jpg"
    cv2.imwrite(filename, frame)
    return send_file(filename, mimetype='image/jpg')

def get_frame():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    x, frame = camera.read()
    if x:
        camera.release()
        return frame
    else:
        print("error")
        return None
    
def get_t2s_codes(target_language):
    return language_codes[target_language], voice_codes[target_language]

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
