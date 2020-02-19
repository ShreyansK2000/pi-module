from flask import Flask, jsonify, request, send_file
import numpy as np
import cv2
import os
import azure_api_calls as api
import draw
import unidecode
from PIL import Image

import pdb

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

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

@app.route('/uniTest', methods=['GET'])
def toUTF8():
    string = "soursis d\u2019ordinateur"
    print(string)
    string = unidecode.unidecode(string)
    return jsonify({"out" : string})
    

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"newTest": "TEST"})

@app.route('/translate', methods=['GET'])
def translate():
    target_language = (request.args.get('target_language')).lower()
    
    # get codes for text to speech playback
    language_code, voice_code = get_t2s_codes(target_language);

    frame = get_frame()
    filename = "test_output_translate.bmp"
    cv2.imwrite(filename, frame)
    image_data = open(filename, "rb").read()

    # detect the objects in the image
    analysisJson = api.detect_objects(image_data)

    # draw bounding boxes on all the images
    objects = analysisJson['objects']
    boxed_filename = draw.boundingBoxes(frame, objects)
    
    palettize(boxed_filename)
    
    returnJson = {
            "objects":[],
            "targetLanguage": target_language,
            "nativeLanguage": "english"
        }

    # find translation of detected objects for target language
    objectCount = 0
    for detectedObject in objects:
        translation = api.translate(detectedObject['object'],
                                    language_code)['translations'][0]['text']
        #api.text_to_speech(translation, objectCount, language_code, voice_code)
        
        returnJson["objects"].append({
            "native" : detectedObject['object'],
            "translated" : unidecode.unidecode(translation)
            })
        
        objectCount += 1

    return jsonify(returnJson)

@app.route('/get_file', methods=['GET'])
def get_img():
    frame = get_frame()
    filename = "test_output_get_file.bmp"
    cv2.imwrite(filename, frame)
    
    return send_file(filename, mimetype='image/bmp')

def palettize(filename):
    limitedColours = Image.open(filename).quantize(colors=64)
    limitedColours.save('limited.bmp')
    limitedColoursRGB = limitedColours.convert('RGB')
    
    colours = limitedColoursRGB.getcolors()
    colours.sort(key=lambda x:x[1][0], reverse=True)
    paletteFile = open('limited.txt', 'w')
    
    for colour in colours:
        r = colour[1][0]
        g = colour[1][1]
        b = colour[1][2]
        paletteFile.write(rgb2hex(r,g,b) + '\n')
            
def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r,g,b)

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
