from flask import Blueprint, request
import pymongo

users_api = Blueprint('users_api', __name__)

"""
It is assumed for the endpoints in this file that an
instance of MongoDB is running on the default host and port
"""

# Return a MongoClient to interact with our MongoDB instance
def connect_db():
    client = pymongo.MongoClient("localhost", 27017)
    return client

# CREATE

# Add a user with name username from the database
@users_api.route("/<username>", methods=['POST'])
def insert_user(username):
    # Add user to database
    return username, 'SUCCESS'

# READ

# Get a list of users from the database
@users_api.route("/")
def get_all_users():
    # Read users from database
    return {"users": ['Alice', 'Bob', 'Charlie']}

# Get a user with user id userid from the database
@users_api.route("/<userid>", methods=['GET'])
def get_user(userid):
    # retrieve user with user id is userid
    return {"username": 'Alice', 
            "userid": 1
    }

# Get a user's target language with user id userid from the database
@users_api.route("/<userid>/target_language", methods=['GET'])
def get_target_language(userid):
    # retrieve user with user id is userid from mongo
    # access the target_language property
    return {"username": 'Alice',
            "user id": userid,
            "target language": 'German'}

# UPDATE

# Update a user's username, with user id is userid
@users_api.route("/<userid>", methods=['PUT'])
def change_username(userid):
    new_username = request.args.get('username')
    # update username in the mongo db
    return 'Username was successfully changed', new_username

# Update a user's target language
@users_api.route("/<userid>", methods=['PUT'])
def change_target_language(userid):
    new_target_language = request.args.get('target_language')
    # update the user's target language in the mongo db
    return 'The target language was successfully changed', new_target_language

# DELETE

# Delete a user with user id userid from the database
@users_api.route("/<userid>", methods=['DELETE'])
def delete_user(userid):
    return userid, 'SUCCESS'

if __name__ == 'users':
    client = connect_db()
    db = client.database
    users = db.users