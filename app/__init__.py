from flask import Flask
from .database import init_db
from flask_login import LoginManager
from .models import User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #LoginManager_config
    login_manager = LoginManager()
    login_manager.login_view = 'blog.index'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        session_db = app.session
        return session_db.query(User).get(int(user_id))

    init_db(app)

    from .views import bp
    app.register_blueprint(bp)

    return app
