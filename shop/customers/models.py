from flask_login import UserMixin
from shop import db, login_manager
from datetime import datetime
import json


@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)


class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(180), unique=False, nullable=False)
    country = db.Column(db.String(20), unique=False)
    city = db.Column(db.String(20), unique=False)
    contact = db.Column(db.Integer, unique=False) 
    address = db.Column(db.String(40), unique=False)
    zipcode = db.Column(db.Integer, unique=False)
    profile = db.Column(db.String(200), unique=False, default='profile.jpg')
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Register %r>' % self.username
    

class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEcodedDict)
    
    def __repr__(self):
        return '<CustomerOrder %r>' % self.invoice


db.create_all()