from flask import Flask
from .database import init_db
from flask_login import LoginManager
from .models import User
from markdown_it import MarkdownIt
import bleach

def create_app():
    #Flask_app_config-----
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #LoginManager_config-----
    login_manager = LoginManager()
    login_manager.login_view = 'blog.index'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        session_db = app.session
        return session_db.query(User).get(int(user_id))

    #Database_initialization-----
    init_db(app)

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
