from flask import Blueprint, request, jsonify
from ...runserver import db
from .database import *

# Create the history Blueprint
history = Blueprint('history', __name__)

'''
Add to user history endpoint
 
@param - name -> string of the user's name
@param - native_language -> string of the user's native 
                            language
@param - target_language -> string of the user's target 
                            language
@param - native_word -> string of the native word of the 
                        captured item
@param - target_word -> string of the target (translated) 
                        word of the captured item
 
Adds the translation to the user's history 
'''
@history.route('/add_to_history', methods=['GET'])
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
Remove from user history endpoint
 
@param - name -> string of the user's name
@param - native_language -> string of the user's native 
                            language
@param - target_language -> string of the user's target 
                            language
@param - native_word -> string of the native word of the 
                        captured item
@param - target_word -> string of the target (translated) 
                        word of the captured item
 
Removes the translation from the user's history 
'''
@history.route('/remove_from_history', methods=['GET'])
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
Get user history endpoint
 
@param - name -> string of the user's name

Gets the user's history with name=name
'''
@history.route('/get_user_history', methods=['GET'])
def get_user_history():
    global db
    name = (request.args.get('name'))
    
    if db is not None:
        return jsonify(get_history(db, name))
    else:
        return '\"NO_DB\"' 