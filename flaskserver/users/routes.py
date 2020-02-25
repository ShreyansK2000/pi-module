from flask import Blueprint, request
from ...runserver import db
from .database import *

users = Blueprint('users', __name__)

'''
'''
@users.route('/register_user', methods=['GET'])
def register_user():
    global db
    name = (request.args.get('name'))
    password  = (request.args.get('password'))
    
    if db is not None:
        return create_user(db, name, password)
    else:
        return 'NO_DB'

'''
'''
@users.route('/authenticate_user', methods=['GET'])
def authenticate_user():
    global db
    name = (request.args.get('name'))
    password  = (request.args.get('password'))
    
    if db is not None:
        return find_user(db, name, password)
    else:
        return 'NO_DB'

'''
'''
@users.route('/delete_user', methods=['GET'])
def delete_user():
    global db
    name = (request.args.get('name'))
    password  = (request.args.get('password'))
    
    if db is not None:
        return remove_user(db, name, password)
    else:
        return 'NO_DB'