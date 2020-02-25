import pymongo

def connect_db():
    client = pymongo.MongoClient("localhost", 27017)
    return client.endpoint_test