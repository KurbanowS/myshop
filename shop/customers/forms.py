from wtforms import StringField, TextAreaField, PasswordField, SubmitField, validators, Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import EmailField


class CustomerRegisterForm(Form):
    name = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = EmailField('Email: ', [validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm', message='Both password must match')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
    country = StringField('Country: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    contact = StringField('Contact: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])

    profile = FileField('Profile: ', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Image only please')])

    submit = SubmitField('Submit')