from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False

    from .users.routes import users
    from .history.routes import history
    from .translate.routes import translate
    app.register_blueprint(users)
    app.register_blueprint(history)
    app.register_blueprint(translate)

    return app