from .flaskserver import create_app
from .flaskserver.db_setup import connect_db

# Connect a MongoClient to the MongoDB
db = connect_db()

# Create the Flask app
app = create_app()

'''
Two basic routes to test that the server is working
after having ran the flask run command in terminal
'''
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test')
def testing_testing():
    return 'testing, testing'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)