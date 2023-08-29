from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os
from flask_msearch import Search
from flask_login import LoginManager
from flask_babel import Babel, lazy_gettext as _l
from config import Config


db = SQLAlchemy()
migrate = Migrate()
search = Search()
babel = Babel()


login_manager = LoginManager()
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = _l("Please login First")
photos = UploadSet('photos', IMAGES)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    login_manager.init_app(app)
    db.init_app(app)
    search.init_app(app)
    babel.init_app(app)
    migrate.init_app(app, db)
    configure_uploads(app, photos)
    patch_request_class(app)

    from shop.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from shop.products import bp as products_bp
    app.register_blueprint(products_bp)

    from shop.carts import bp as carts_bp
    app.register_blueprint(carts_bp)

    from shop.customers import bp as customers_bp
    app.register_blueprint(customers_bp)

    from shop.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    @app.context_processor
    def inject_conf_var():
        return dict(
            AVAILABLE_LANGUAGE=app.config['LANGUAGES'],
            CURRENT_LANGUAGE=session.get('language','en')
        )
    return app


@babel.localeselector
def get_locale():
    try:
        language = session['language']
    except KeyError:
        language = None
    if language:
        return language
    return 'ru'