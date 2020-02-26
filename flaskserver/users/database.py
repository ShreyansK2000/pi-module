import pymongo
from time import time
import json
import re

import pdb

'''
Create user helper function

@param - db -> a MongoClient connected to an instance of MongoDB 
@param - name -> string of the user's name
@param - password -> string of the user's password
 
Adds the given user to the database with name=name,
    password=password if no such user already exists

Returns - a string of the new user's userid on success and an
          appropriate error message otherwise
'''    
def create_user(db, name, password):
    if db['users'].find({"name": name}).count() > 0:
        return '\"USER_EXISTS\"'
    else:
        user = {"name": name, "password": password, "history_ids": []}
        user_id = db['users'].insert_one(user).inserted_id
        return '\"'+ str(user_id)+'\"'

'''
Find user helper function

@param - db -> a MongoClient connected to an instance of MongoDB 
@param - name -> string of the user's name
@param - password -> string of the user's password
 
Finds the given user from the database with name=name,
    password=password if the user exists

Returns - a string of the user's userid if the user exists
'''   
def find_user(db, name, password):
    user = None
    if db['users'].find({"name": name}).count() > 0:
        user = db['users'].find_one({"name": name, "password": password})
        if user is not None:
            return '\"'+str(user["_id"])+'\"'
        else:
            return '\"INCORRECT_PASSWORD\"'
    else:
        return '\"USER_DNE\"'

'''
Find user helper function

@param - db -> a MongoClient connected to an instance of MongoDB 
@param - name -> string of the user's name
@param - password -> string of the user's password
 
Finds the given user from the database with name=name,
    password=password if the user exists

Returns - a string detailing the result
'''   
def remove_user(db, name, password):
    user = None
    if db['users'].find({"name": name}).count() > 0:
        user = db['users'].find_one({"name": name, "password": password})
        if user is not None:
            result = db['users'].delete_one(user)
            if result.deleted_count is 1:
                return '\"'+'Deleted user with userid:'+str(user["_id"])+'\"'
            else:
                return '\"'+'Unable to delete user with userid:'+str(user["_id"])+'\"'
        else:
            return '\"INCORRECT_PASSWORD\"'
    else:
        return '\"USER_DNE\"'
