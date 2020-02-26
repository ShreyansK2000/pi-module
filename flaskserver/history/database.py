import pymongo
from time import time
import json
import re

import pdb

'''
Add to user history helper function
 
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
Remove from user history helper function
 
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
Get user history helper function
 
@param - name -> string of the user's name

Gets the user's history with name=name
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