from flask import Blueprint, request, jsonify
import cv2
import os
import unidecode
import _thread
import pygame

# Helper functions for image operations
from .image_operations import *

# Helper script for socket communication
from .de1_sockets import send_image_data

# Microsoft API calls
from .azure_api_calls import *

# Create the translate blueprint
translate = Blueprint('translate', __name__)

# Initialize latest_bmp and latest_palette
latest_bmp = None
latest_palette = None

pygame.mixer.init()

# Mapping of languages to language codes for azure calls
language_codes = {
    'english': 'en-us',
    'french': 'fr-fr',
    'german': 'de-de',
    'spanish': 'es-es',
    'italian': 'it-it'
    }

# Mapping of languages to voice codes for azure calls
voice_codes = {
    'english': 'en-US-BenjaminRUS',
    'french': 'fr-FR-Paul-Apollo',
    'german': 'de-DE-Hedda',
    'spanish': 'es-ES-Laura-Apollo',
    'italian': 'it-IT-LuciaRUS'
    }

'''
Main end point for the application.
 
@param - target_language -> string identifying the language to translate to
@param - native_language -> string identifying the selected native language
 
Receives user native language and target language
Fetches image from Pi camera
Sends and receives data from REST api calls for Azure API
Sends response to De1Soc, image over socket thread and response message over HTTP
'''
@translate.route('/translate', methods=['GET'])
def big_translate():
    target_language = (request.args.get('target_language')).lower()
    native_language  = (request.args.get('native_language')).lower()
    
    # get codes for text to speech playback and for HTTP response
    target_language_code  = language_codes[target_language]
    target_voice_code = voice_codes[target_language]
    native_language_code = language_codes[native_language]

    frame = get_frame()
    filename = "Images/test_output_translate.bmp"
    cv2.imwrite(filename, frame)
    image_data = open(filename, "rb").read()

    # detect the objects in the image
    analysisJson = detect_objects(image_data)

    # draw bounding boxes on all the images
    objects = analysisJson['objects']
        
    returnJson = {
            "objects":[],
            "targetLanguage": target_language,
            "nativeLanguage": native_language
        }

    # find translation of detected objects for target language
    translations = []
    for detectedObject in objects:
        translation_object_target = api_translate(detectedObject['object'],
                                    target_language_code)['translations'][0]['text']
        translations.append(unidecode.unidecode(translation_object_target))
        
        translation_object_native = detectedObject['object'] if native_language is "english" else api_translate(detectedObject['object'],
                                    native_language_code)['translations'][0]['text']
        
        returnJson["objects"].append({
            "native" : unidecode.unidecode(translation_object_native),
            "translated" : unidecode.unidecode(translation_object_target)
            })
        
    boxed_filename = boundingBoxes(frame, objects, translations)

    global latest_bmp
    global latest_palette
    
    latest_bmp, latest_palette = palettize(boxed_filename)

    return jsonify(returnJson)

'''
Audio endpoint for the application.
 
@param word -> string identifying the language to translate to
@param language -> string identifying the selected native language
 
Receives and plays audio of the translation of the given word
'''
@translate.route('/play_audio', methods=['GET'])
def play_audio():
    word = (request.args.get('word')).lower()
    language  = (request.args.get('language')).lower()
    
    text_to_speech(word, language_codes[language], voice_codes[language])
    
    pygame.mixer.music.load('Sound/response' + str(0) + '.wav')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    
    return '\"OK\"'

'''
Open bmp socket endpoint for the application.
 
@param word -> string identifying the language to translate to
@param language -> string identifying the selected native language
 
Opens a socket to send the bmp image to the DE1
'''
@translate.route('/open_bmp_sock', methods=['GET'])
def open_bmp_sock():
    global latest_bmp
    global latest_palette
    
    _thread.start_new_thread(send_image_data, (latest_bmp, latest_palette))

    return '\"OK\"'
