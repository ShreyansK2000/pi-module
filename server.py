# Required libraries
import cv2
import os
import unidecode
import _thread
import pygame
import reverse_geocode as rg
from flask import Flask, jsonify, request

import threading
import atexit

# Helper functions for database and image operations
from database import *
from image_operations import *

# Helper script for socket communication
import de1_sockets as de1sock

# Microsoft API calls
import azure_api_calls as api

streaming_thread = None

pygame.mixer.init()

db = None
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

latest_bmp = None
latest_palette = None

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
'''
 Simple test endpoint to make sure that our
 server is able to send responses
'''
@app.route('/test', methods=['GET'])
def test():
    return jsonify({"newTest": "TEST"})

'''
 Main end point for the application.
 
 @param target_language the string identifying the language to translate to
 @param native_language the string identifying the selected native language
 
 - Receives user native language and target language.
 - Fetches image from Pi camera
 - Sends and receives data from REST api calls for Azure API
 - Sends response to De1Soc, image over socket thread and
   response message over HTTP
'''
@app.route('/translate', methods=['GET'])
def translate():
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
    analysisJson = api.detect_objects(image_data)

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
        translation_object_target = api.translate(detectedObject['object'],
                                    target_language_code)['translations'][0]['text']
        translations.append(unidecode.unidecode(translation_object_target))
        
        translation_object_native = detectedObject['object'] if native_language is "english" else api.translate(detectedObject['object'],
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
Opens a socket to send the bmp image to the De1

- return OK if the image was sent successfully
'''
@app.route('/open_bmp_sock', methods=['GET'])
def open_bmp_sock():
    global latest_bmp
    global latest_palette
    
    _thread.start_new_thread(de1sock.send_image_data, (latest_bmp, latest_palette))
    
    return '\"OK\"'


@app.route('/get_location', methods=['GET'])
def get_location():
    latitude = float(request.args.get('latitude'))
    longitude  = float(request.args.get('longitude'))
    
    coordinates = [(latitude, longitude)]
    output = rg.search(coordinates)
    
    return '\"' + output[0]['country'].lower() + '\"'

'''
Plays audio from RPi audio output over a speaker or headset using the pygame library

@param word the word that the user wishes to hear the audio for
@param language the target language for the audio

- returns a .wav audio file with the given word spoken in the target language
'''
@app.route('/play_audio', methods=['GET'])
def play_audio():
    word = (request.args.get('word')).lower()
    language  = (request.args.get('language')).lower()
    
    api.text_to_speech(word, language_codes[language], voice_codes[language])
    
    pygame.mixer.music.load('Sound/response' + str(0) + '.wav')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    
    return '\"OK\"'

'''
 End point for registering a new user
 
 @param name the new user's username
 @param password the new user's password
 
 - Returns the user's unique user_id if successful 
 - create_user method takes care of instance where user already exists in the db
'''
@app.route('/register_user', methods=['GET'])
def register_user():
    global db
    name = (request.args.get('name'))
    password  = (request.args.get('password'))
    
    if db is not None:
        return create_user(db, name, password)
    else:
        return '\"NO_DB\"'

''''
 End point for authenticating a user
 
 @param name the existing user's username
 @param password the existing user's password
 
 - Returns the user's unique user_id if successful 
 - find_user method takes care of incorrect username/password scenarios
'''
@app.route('/authenticate_user', methods=['GET'])
def authenticate_user():
    global db
    name = (request.args.get('name'))
    password  = (request.args.get('password'))
    
    if db is not None:
        return find_user(db, name, password)
    else:
        return '\"NO_DB\"'

'''
End point for deleting an existing user

 @param name the existing user's username
 @param password the existing user's password
 
 - Returns the user's unique user_id if successful
 - delete_user method takes care of incorrect username/password scenarios 
'''
@app.route('/delete_user', methods=['GET'])
def delete_user():
    global db
    name = (request.args.get('name'))
    password  = (request.args.get('password'))
    
    if db is not None:
        return remove_user(db, name, password)
    else:
        return '\"NO_DB\"'

'''
End point for adding a word to a user's history

 @param name the user's username
 
 - Returns the user's ADD_OK if successful
 - add_history method takes care of incorrect username/password and invalid word scenarios 
'''    
@app.route('/add_to_history', methods=['GET'])
def add_to_history():
    global db
    name = (request.args.get('name'))
    native_language = (request.args.get('native_language'))
    target_language = (request.args.get('target_language'))
    native_word = (request.args.get('native_word'))
    target_word = (request.args.get('target_word'))
    
    if db is not None:
        return add_history(db, name, native_language, target_language, native_word, target_word)
    else:
        return '\"NO_DB\"'

'''
End point for removing a word from a user's history

 @param name the user's username
 
 - Returns the user's DELETE_OK if successful
 - add_history method takes care of incorrect username/password and invalid word scenarios 
'''      
@app.route('/remove_from_history', methods=['GET'])
def remove_from_history():
    global db
    name = (request.args.get('name'))
    native_language = (request.args.get('native_language'))
    target_language = (request.args.get('target_language'))
    native_word = (request.args.get('native_word'))
    target_word = (request.args.get('target_word'))
    
    if db is not None:
        return remove_history(db, name, native_language, target_language, native_word, target_word)
    else:
        return '\"NO_DB\"'

'''
End point for adding a word to a user's history

 @param name the user's username
 
 - Returns a user's entire history of words
 - add_history method takes care of incorrect username/password and invalid word scenarios 
'''    
@app.route('/get_user_history', methods=['GET'])
def get_user_history():
    global db
    name = (request.args.get('name'))
    
    if db is not None:
        return jsonify(get_history(db, name))
    else:
        return '\"NO_DB\"' 
    
def stop_streaming_thread():
    global streaming_thread
    
    stop_stream()
    
    if streaming_thread is not None:
        streaming_thread.join()
    
if __name__ == '__main__':
    db = connect_db()
    
    streaming_thread = threading.Thread(target = start_stream, args = ())
    streaming_thread.start()
    
    atexit.register(stop_streaming_thread)
    
    app.run(host='0.0.0.0', debug=False)
