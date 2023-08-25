from wtforms import StringField, IntegerField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from .models import Register


class CustomerRegisterForm(FlaskForm):
    name = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = EmailField('Email: ', [validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm', message='Both password must match')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
    country = StringField('Country: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    contact = IntegerField('Contact: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])
    zipcode = IntegerField('Zipcode: ', [validators.DataRequired()])

    profile = FileField('Profile: ', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Image only please')])

    submit = SubmitField('Submit')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError('This username is already exist')
        
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError('This email is already exist')
        

class CustomerLoginForm(FlaskForm):
    email = EmailField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])