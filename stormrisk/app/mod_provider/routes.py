# Author: DANIEL BIS


from flask import Flask, render_template, redirect, url_for, Blueprint
from flask_sqlalchemy  import SQLAlchemy
from flask_wtf import FlaskForm 
from flask_login import login_user, login_required, logout_user, current_user
import logging
from app.mod_provider.forms import DateForm

#import database object and login manager from app module
from app import db, login_manager
#import the app object itself
from app import app

#Import module models containing User
from app.mod_auth.models import User, Shop
from app.mod_auth.routes import load_user

from app.mod_provider.models import Schedule

provider_mod = Blueprint("mod_provider", __name__, url_prefix = "/provider")

@provider_mod.route('/addschedule', methods = ['GET', 'POST'])
def add_schedule():

	form = DateForm()

	if form.validate_on_submit():
		employee = User.query.filter_by(email = form.email.data).first()
		new_schedule = Schedule(starttime = form.start_time.data, endtime = form.end_time.data)

		employee.schedules.append(new_schedule)
		db.session.add(new_schedule)
		db.session.commit()
		return '<h1>New schedule added! </h1>'
	print("form not validated")
	return render_template('provider/add_schedule.html', form = form)

