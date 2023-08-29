import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/flaskecommerce"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'asfjashfjsbj121'
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'shop/static/images')
    LANGUAGES = ['en', 'ru']