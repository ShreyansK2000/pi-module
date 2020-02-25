from .flaskserver import create_app
from .flaskserver.db_setup import connect_db

db = None
db = connect_db()
app = create_app()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test')
def testing_testing():
    return 'testing, testing'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)