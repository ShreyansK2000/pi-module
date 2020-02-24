import pymongo

def connect_db():
    client = pymongo.MongoClient("localhost", 27017)
    return client.endpoint_test

def update_history(db, _id, word):
    db.update_one(
        { "_id": _id},
        { "$push": { "history": word }}
    )

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
