from .flaskserver import create_app
from .flaskserver.db_setup import connect_db

app = create_app()

if __name__ == '__main__':
    db = connect_db()
    app.run(host='0.0.0.0', debug=True)