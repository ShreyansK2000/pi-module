from flask import Flask

'''
Creates and returns the flask app with
its blueprints registered
'''
def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False

    # Import and register the app's blueprints
    from .users.routes import users
    from .history.routes import history
    from .translate.routes import translate
    app.register_blueprint(users)
    app.register_blueprint(history)
    app.register_blueprint(translate)

    return app