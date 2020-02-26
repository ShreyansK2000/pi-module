from flask import Blueprint, request
from ...runserver import db
from .database import *

# Create the users Blueprint
users = Blueprint('users', __name__)

'''
User registration endpoint
 
@param - name -> string of the user's name
@param - password -> string of the user's password
 
Registers a new user in the database
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
User authentication (login) endpoint
 
@param - name -> string of the user's name
@param - password -> string of the user's password
 
Logs in the given user if the credentials match
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
User deletion endpoint
 
@param - name -> string of the user's name
@param - password -> string of the user's password
 
Deletes the given user if the user with the credentials exists
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