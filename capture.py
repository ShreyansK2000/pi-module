from flask import Flask, jsonify, request, send_file
import numpy as np
import cv2
import os
import azure_api_calls as api
import de1_sockets as de1sock
import draw
import unidecode
import _thread
import pygame
from PIL import Image

import pdb

pygame.mixer.init()

z = 0
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

language_codes ={
    'english': 'en-us',
    'french': 'fr-fr',
    'german': 'de-de',
    'spanish': 'es-es',
    'italian': 'it-it'
    }

voice_codes = {
    'english': 'en-US-BenjaminRUS',
    'french': 'fr-FR-Paul-Apollo',
    'german': 'de-DE-Hedda',
    'spanish': 'es-ES-Laura-Apollo',
    'italian': 'it-IT-LuciaRUS'
    }

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"newTest": "TEST"})

@app.route('/translate', methods=['GET'])
def translate():
    target_language = (request.args.get('target_language')).lower()
    native_language  = (request.args.get('native_language')).lower()
    
    # get codes for text to speech playback
    target_language_code, target_voice_code = get_t2s_codes(target_language);
    native_language_code = language_codes[native_language]

    frame = get_frame()
    filename = "test_output_translate.bmp"
    cv2.imwrite(filename, frame)
    image_data = open(filename, "rb").read()

    # detect the objects in the image
    analysisJson = api.detect_objects(image_data)

    # draw bounding boxes on all the images
    objects = analysisJson['objects']
        
    returnJson = {
            "objects":[],
            "targetLanguage": target_language,
            "nativeLanguage": native_language
        }

    # find translation of detected objects for target language
    objectCount = 0
    translations = []
    for detectedObject in objects:
        translation_object_target = api.translate(detectedObject['object'],
                                    target_language_code)['translations'][0]['text']
        translations.append(unidecode.unidecode(translation_object_target))
        
        translation_object_native = detectedObject['object'] if native_language is "english" else api.translate(detectedObject['object'],
                                    native_language_code)['translations'][0]['text']
        
        returnJson["objects"].append({
            "native" : unidecode.unidecode(translation_object_native),
            "translated" : unidecode.unidecode(translation_object_target)
            })
        
        objectCount += 1
        
    boxed_filename = draw.boundingBoxes(frame, objects, translations)
    
    bmp_filename, palette_filename = palettize(boxed_filename)
    _thread.start_new_thread(de1sock.send_image_data, (bmp_filename, palette_filename))

    return jsonify(returnJson)

@app.route('/play_audio', methods=['GET'])
def play_audio():
    global z
    word = (request.args.get('word')).lower()
    language  = (request.args.get('language')).lower()
    
    api.text_to_speech(word, language_codes[language], voice_codes[language])
    
    
    pygame.mixer.music.load('response' + str(0) + '.wav')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    
    return "OK"
    
def palettize(filename):
    limitedColours = Image.open(filename).quantize(colors=64)
    bmp_filename = 'Images/limited.bmp'
    limitedColours.save(bmp_filename)
    
    palette_filename = getPalette(bmp_filename)
        
    return bmp_filename, palette_filename

def getPalette(filename):
    palette_filename = 'Images/limited.txt'
    
    with open(filename, "rb") as f:
        f.read(54) # go to offset 54
        palette_bytes = f.read(256)
        paletteFile = open(palette_filename, 'w')
                
        byte_iter = iter(palette_bytes)
        for byte in byte_iter:
            b = byte
            g = next(byte_iter)
            r = next(byte_iter)
                
            paletteFile.write(rgb2hex(r,g,b) + '\n')
                
            # force iterator to next 0 byte
            try:
                next(byte_iter)
            except:
                break
                
    return palette_filename

def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r,g,b)

def get_frame():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
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
