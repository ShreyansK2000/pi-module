import pymongo
from time import time
import json
import re

import pdb
    
def create_user(db, name, password):
    if db['users'].find({"name": name}).count() > 0:
        return '\"USER_EXISTS\"'
    else:
        user = {"name": name, "password": password, "history_ids": []}
        user_id = db['users'].insert_one(user).inserted_id
        return '\"'+ str(user_id)+'\"'

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
