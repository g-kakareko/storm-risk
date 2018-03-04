from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


# Define the login form (WTForms)

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    firstname = StringField('first name', validators=[InputRequired(), Length(min=2, max=32)])
    lastname = StringField('last name', validators=[InputRequired(), Length(min=2, max=32)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterFormShop(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    shopname = StringField('shopname', validators=[InputRequired(), Length(min=2, max=64)])
    address = StringField('address', validators=[InputRequired(), Length(min=8, max=128)])
    phonenumber = StringField('phonenumber', validators=[InputRequired(), Length(min=10, max=12)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterFormEmployee(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    firstname = StringField('firstname', validators=[InputRequired(), Length(min=2, max=32)])
    lastname = StringField('lastname', validators=[InputRequired(), Length(min=2, max=32)])
    phonenumber = StringField('phonenumber', validators=[InputRequired(), Length(min=10, max=12)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    manager = BooleanField('manager')
