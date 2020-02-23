import pymongo

def connect_db():
    client = pymongo.MongoClient("localhost", 27017)
    return client.db

def update_history(db, _id, word):
    db.update_one(
        { "_id": _id},
        { "$push": { "history": word }}
    )

def create_user(db, name, password):
    user = {"name": name, "password": password, "history": []}
    user_id = db.insert_one(user)
    return user_id

def authenticate_user(db, name, password):
    user = db.find_one({"name": name, "password": password})
    if(user)
      return user._id.toString()
    else
      return ""

