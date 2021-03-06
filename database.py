import pymongo
from time import time
import json
import re

'''
Starts and connects to the database
 
 - Returns the database endpoint
'''   
def connect_db():
    client = pymongo.MongoClient("localhost", 27017)
    #client.drop_database('users')
    return client.endpoint_test
    
'''
Adds a new word to an existing user's history

- Returns ADD_OK if the addition was successful and NO_SUCH_USER if the user doesn't exist
'''
def add_history(db, username, native_language, target_language, native_word, target_word):
    translation = db['translations'].find_one({"native_language" : native_language, "target_language" : target_language, "native_word" : native_word, "target_word" : target_word})
    if translation is not None:
        translation_id = translation["_id"]
    else:
        translation = {"native_language" : native_language, "target_language" : target_language, "native_word" : native_word, "target_word" : target_word}
        translation_id = db['translations'].insert_one(translation).inserted_id
    user = db['users'].find_one({"name" : username})
    
    if user is None:
        return '\"NO_SUCH_USER\"'
    
    for history_id in user['history_ids']:
        if history_id['id'] == translation_id:
            db['users'].update_one(
                {"name" : username, "history_ids.id" : translation_id},
                {"$set" : {"history_ids.$.timestamp" : time()}}
                )
            return '\"ADD_OK\"'
    
    db['users'].update({"name" : username}, {'$push': {"history_ids" :{"timestamp" : time(), "id" : translation_id}}})
    return '\"ADD_OK\"'

'''
Adds a new word to an existing user's history

- Returns REMOVE_OK if the addition was successful and NO_SUCH_TRANSLATION if the word doesn't exist
'''
def remove_history(db, username, native_language, target_language, native_word, target_word):
    # Remove the translation from the user collection if it exists,
    translation = db['translations'].find_one({"native_language" : native_language, "target_language" : target_language, "native_word" : native_word, "target_word" : target_word})
    
    if translation is None:
        return '\"NO_SUCH_TRANSLATION\"'
    
    translation_id = translation["_id"]
    db['users'].update(
        {"name" : username},
        {"$pull" : {"history_ids" : {"id" : translation_id}}}
        )
    
    return '\"REMOVE_OK\"'

'''
Fetches the entirety of an existing user's history of saved words

- Returns the history in json format if it exists or an error message otherwise
'''
def get_history(db, username):
    # Lookup user by username
    # Sort their history_id value by most recent timestamp first
    # return this collection
    user = db['users'].find_one({"name" : username})
    timestamp_sorted = sorted(user['history_ids'], key=lambda k: k['timestamp'], reverse=True)
    
    ret = []
    for entry in timestamp_sorted:
        translation = db['translations'].find_one({"_id" : entry['id']})
        ret.append({
            "native_language" : translation['native_language'],
            "target_language" : translation['target_language'],
            "native" : translation['native_word'],
            "translated" : translation['target_word']
            })
        
    return {"history": ret}

'''
Creates a new user in the database

- Returns the new user's user_id if the creation was successful or USER_EXISTS otherwise
'''
def create_user(db, name, password):
    if db['users'].find({"name": name}).count() > 0:
        return '\"USER_EXISTS\"'
    else:
        user = {"name": name, "password": password, "history_ids": []}
        user_id = db['users'].insert_one(user).inserted_id
        return '\"'+ str(user_id)+'\"'

'''
Finds a user in the database

- Returns the user's user_id if successful or an error message otherwise
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
Removes a user from the database

- Returns deleted user's id if successful or an error message otherwise
'''
def remove_user(db, name, password):
    user = None
    if db['users'].find({"name": name}).count() > 0:
        user = db['users'].find_one({"name": name, "password": password})
        if user is not None:
            result = db['users'].delete_one(user)
            if result.deleted_count is 1:
                return '\"SUCCESS\"'
            else:
                return '\"FAILED\"'
        else:
            return '\"INCORRECT_PASSWORD\"'
    else:
        return '\"USER_DNE\"'
