import pymongo

def connect_db():
        client = pymongo.MongoClient("localhost", 27017)
        return client
   
client = connect_db()
db = client.database
users = db.users

#Delete entire table to avoid duplicate _id in testing
users.drop()

testUser = { "name": "Alice", "password": "abc", "_id": "1", "history": [] }

x = users.insert_one(testUser)

print(x)

y = users.find_one({ "_id": "1" })
print(y)

#Test update a query
users.update_one(
    { "_id": "1"},
    { "$push": { "history": "apple" }}
)


#Print users
for z in users.find():
    print(z)
