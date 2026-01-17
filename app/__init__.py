from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from markdown_it import MarkdownIt
import os
import bleach

db = SQLAlchemy()

def create_app():
    #Flask_app_config-----
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    #Database_setup-----
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        database_url = database_url.replace("postgres://", "postgresql://")
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)

    from .models import User
    with app.app_context():
        db.create_all()

    #LoginManager_config-----
    login_manager = LoginManager()
    login_manager.login_view = 'blog.index'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(int(user_id))

    #Blueprint_registration-----
    from .views import bp
    app.register_blueprint(bp)

    #markdown_support-----
    md = MarkdownIt("commonmark")
    md.renderer.rules["softbreak"] = lambda *args: "<br>\n"

    @app.template_filter('markdown')
    def markdown_filter(text):
        # markdown > html
        html = md.render(text)

        allowed_tags = [ 'p', 'ul', 'ol', 'li', 'strong', 'em', 'a', 'code', 'br',
                         'pre', 'blockquote', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
        ]

        allowed_attrs = {
            'a': ['href', 'title'],
            'code': ['class'],
        }

        clean_html = bleach.clean(
            html,
            tags=allowed_tags,
            attributes=allowed_attrs,
            strip=False
        )
        return clean_html

    return app
