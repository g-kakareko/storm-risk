from flask import Flask, render_template, redirect, url_for, Blueprint
from flask_sqlalchemy  import SQLAlchemy
from flask_wtf import FlaskForm 
from flask_login import login_user, login_required, logout_user, current_user
import logging

#import database object and login manager from app module
from app import app, db, login_manager


#Import module models containing User
from app.mod_auth.models import User, Shop
from app.mod_provider.models import Schedule

customer_mod = Blueprint("mod_customer", __name__)

@customer_mod.route('/dashboardcustomer')
@login_required
def dashboardcustomer():
	shops = Shop.query.all()
	return render_template('customer/dashboard_customer.html', name=current_user.first_name, shops = shops)