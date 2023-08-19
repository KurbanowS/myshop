from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myshop.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'asfjashfjsbj121'
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.app_context().push()


from shop.admin import routes
from shop.products import routes