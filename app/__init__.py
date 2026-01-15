from flask import Flask
from .database import init_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    from .views import bp
    app.register_blueprint(bp)

    return app
