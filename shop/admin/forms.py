from wtforms import StringField, PasswordField, validators
from wtforms.validators import ValidationError
from flask_wtf import FlaskForm
from .models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=1, max=25)])
    username = StringField('Username', [validators.Length(min=1, max=30)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [validators.DataRequired(), validators.EqualTo('password', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [validators.DataRequired()])