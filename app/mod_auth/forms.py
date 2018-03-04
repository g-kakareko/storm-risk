from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField
from wtforms.validators import InputRequired, Email, Length, DataRequired


# Define the login form (WTForms)

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class AppraisalForm(FlaskForm):
	year = IntegerField('Year of Construction', validators=[InputRequired()])
	zip_code = IntegerField('Zip Code for Value Estimation', validators=[InputRequired()])
	area = IntegerField('Area in Square Feet', validators=[InputRequired()])
	window_protection = SelectField('Window Protection', choices=[("True","Yes"), ("False","No")], validators=[InputRequired()])
	surroundings = SelectField('Surroundings', choices=[("D","On shore"),("B","Suburban"), ("B", "City"), ("C","Field"), ("C", "Forrest")], validators=[InputRequired()])
	last_roof_renew = IntegerField("If you remember, provide a year of the last roof renovation.", default=0)
	roof_wall_connection = SelectField("Type of roof to wall connection", choices=[("d","default"),("1846","Toe Nail"), ("3069","Clip"), ("5840","Wrap")])
	type_of_construction = SelectField('Type of Construction', choices=[ ("1","Wood"), ("6300","Masonry") ], validators=[InputRequired()])
	#advanced
	type_of_roof_cover = SelectField("Type of your roof cover", choices=[("d","default"),("2442","tiles"), ("3352","shingles")])
	type_of_roof_sheathing = SelectField("Type of your roof sheathing", choices=[("d","default"),("2614","6d 6/12"), ("4932","8d 6/12"), ("6300","8d 6/6")])
	type_of_windows = SelectField("Type of windows", choices=[("d","default"),("2500","tall"), ("3330","medium"), ("5000","small"), ("6300","hurricane proof")])

class MitigationForm(FlaskForm):
	window_protection = SelectField('Window Protection', choices=[("True","Yes"), ("False","No")], validators=[InputRequired()])
	roof_wall_connection = SelectField("Type of roof to wall connection", choices=[("d","default"),("1846","Toe Nail"), ("3069","Clip"), ("5840","Wrap")])
	#advanced
	type_of_roof_cover = SelectField("Type of your roof cover", choices=[("d","default"),("2442","tiles"), ("3352","shingles")])
	type_of_roof_sheathing = SelectField("Type of your roof sheathing", choices=[("d","default"),("2614","6d 6/12"), ("4932","8d 6/12"), ("6300","8d 6/6")])
	type_of_windows = SelectField("Type of windows", choices=[("d","default"),("2500","tall"), ("3330","medium"), ("5000","small"), ("6300","hurricane proof")])
	