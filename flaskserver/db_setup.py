import pymongo

'''
Pre-Condition: An instance of MongoDB is already running
               on the local machine, i.e. the RPi for the
               purposes of our project

Create a MongoClient and connect to the running MongoDB
instance.

Returns the MongoClient
'''
def connect_db():
    client = pymongo.MongoClient("localhost", 27017)
    return client.endpoint_test