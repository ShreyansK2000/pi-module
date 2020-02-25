from flask import Blueprint, request, jsonify
from ...runserver import db
from .database import *

history = Blueprint('history', __name__)

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

@history.route('/get_user_history', methods=['GET'])
def get_user_history():
    global db
    name = (request.args.get('name'))
    
    if db is not None:
        return jsonify(get_history(db, name))
    else:
        return '\"NO_DB\"' 