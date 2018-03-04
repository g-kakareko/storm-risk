#flask dependencies
from flask import Flask, render_template, redirect, url_for, Blueprint, request, session
import flask
from flask_wtf import FlaskForm 
from app.mod_auth.forms import RegisterForm, LoginForm, AppraisalForm, MitigationForm
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
import numpy as np
import csv
import math
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objs as go

from riskpy.vulnerability import vulnerability as vul
#import database object from app module 
from app import db, login_manager
from datetime import datetime
from app import app
#Import module models containing User
from app.mod_auth.models import User

#Define the blueprint: 'auth', sets its url prefix: app.url/auth
mod = Blueprint('mod_auth', __name__, url_prefix = "/auth")

def rating (damage):
    if damage[4] < 15000 and damage[5] < 40000:
        return 1
    elif damage[3] < 15000 and damage[4] < 40000:
        return 2
    elif damage[2] < 20000 and damage[3] < 30000:
        return 3
    else:
        return 4


def search(zipcode):
    with open('app/mod_auth/Zip_MedianValuePerSqft.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["RegionName"] == str(zipcode):
                return row["2018-01"]


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#set route and accepted methods
@mod.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('mod_auth.dashboardcustomer'))
        return '<h1>Invalid username or password</h1>'
    return render_template('auth/login.html', form=form)

@mod.route('/loginguest', methods=['POST'])
def loginguest():
    if request.method == 'POST' and request.form["guest"] == "guest":
        user = User.query.filter_by(email="guest@email.com").first()
        if user:
            if check_password_hash(user.password, "guestPass123"):
                login_user(user)
                return redirect(url_for('mod_auth.dashboardcustomer'))
        return '<h1>Invalid username or password</h1>'
    return render_template('auth/login.html', form=form) 


@mod.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        try:
            new_user = User(email=form.email.data, password=hashed_password)
            #check if email is taken
            #user = User.query.filter_by(email=form.email.data).first()
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return '<h1>This email address is already taken.</h1>'
        return redirect(url_for('mod_auth.login'))
    return render_template('auth/signup.html', form=form)
"""
@mod.route('/dashboard')
@login_required
def dashboard():
    return render_template('auth/dashboard.html', name=current_user.first_name)
"""
@mod.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@mod.route('/dashboardcustomer', methods=['GET', 'POST'])
@login_required
def dashboardcustomer():
    form = AppraisalForm()
    
    if form.is_submitted():
        print ("submitted")
        print(form.errors)

    if form.validate_on_submit():
        print("validated")
        params_object = {
            "year": form.year.data,
            "zip_code": form.zip_code.data,
            "area": form.area.data,
            "window_protection": form.window_protection.data,
            "surroundings": form.surroundings.data,
            "last_roof_renew": form.last_roof_renew.data,
            "roof_wall_connection": form.roof_wall_connection.data,
            "type_of_roof_cover": form.type_of_roof_cover.data,
            "type_of_construction": form.type_of_construction.data,
            "type_of_roof_sheathing": form.type_of_roof_sheathing.data,
            "type_of_windows": form.type_of_windows.data
        }

        value_est = int(search(params_object["zip_code"]))
        area = int(params_object["area"]) * 0.09290
        base_side = math.sqrt(area/2)
        cap_window = None

        if params_object["type_of_windows"] == "d":
            cap_window = 3330
        else:
            cap_window = int(params_object["type_of_windows"])
 
        if params_object["window_protection"] == "True":
            cap_window = 6300


        lenght = 2 * base_side
        width = base_side
        exp_cat = params_object["surroundings"]
        gust_speed = np.arange(0, 120)  # m/s
        
        #walls capacity
        cap_walls = 2614
        if int(params_object["type_of_construction"]) == 6300:
            cap_walls = int(params_object["type_of_construction"])
        else:
            if int(params_object["year"]) < 1991:
                cap_walls = 2614
            elif int(params_object["year"]) < 2001:
                cap_walls = 4932
            else:
                cap_walls = 6300

       
        cap_r2w = 1900
        if params_object["roof_wall_connection"] == "d":
            if int(params_object["year"]) < 1991:
                cap_r2w = 1846
            elif int(params_object["year"]) < 2001:
                cap_r2w = 3069
            else:
                cap_r2w = 5840
        else:
            cap_r2w = int(params_object["roof_wall_connection"])

        cap_rs = 2614
        if params_object["type_of_roof_sheathing"] == "d":
            if int(params_object["year"]) < 1991:
                cap_rs = 2614
            elif int(params_object["year"]) < 2001:
                cap_rs = 4932
            else:
                cap_rs = 6300
        else:
            cap_rs = int(params_object["type_of_roof_sheathing"])

        cap_door = 2394
        if int(params_object["year"]) < 2005:
            cap_door = 2394
        else:
            cap_door = 4788

        cap_gd = 1500
        if int(params_object["year"]) < 2005:
            cap_gd = 1430
        else:
            cap_gd = 2490


        cap_rc = 2442
        if params_object["type_of_roof_cover"] == "d":
            if int(params_object["year"]) < 1991:
                cap_rw2 = 2442
            else:
                cap_rc = 3352
        else:
            cap_rc = int(params_object["type_of_roof_cover"])

        wall_height = 3
        roof_height = 4
        n_windows = 10
        cov = 0.5
        year = datetime.utcnow().year
        if (int(params_object["last_roof_renew"])  - year) > 7:
            cap_rc = cap_rc * 0.8
            cap_rs = cap_rs * 0.8
            cap_r2w = cap_r2w * 0.8

        # ------------------ Main Function Vulnerability Estimation ------------------
        damage_ration = vul.vulnerability(exp_cat=exp_cat, gust_speed=gust_speed, cap_walls=cap_walls,
                            cap_rc=cap_rc, cap_rs=cap_rs, cap_window=cap_window, cap_door=cap_door,
                            cap_gd=cap_gd, lenght=lenght, width=width, cov=cov, wall_height=3,
                            roof_height=4, n_windows=10) 
        dollar_damage = damage_ration * int(value_est) * int(params_object["area"])

        print(dollar_damage)

        calculated_params = {
            "exp_cat": exp_cat, 
            "gust_speed": 0, 
            "cap_walls": cap_walls,
            "cap_rc": cap_rc, 
            "cap_rs": cap_rs, 
            "cap_window": cap_window, 
            "cap_door": cap_door,
            "cap_gd": cap_gd, 
            "lenght": lenght, 
            "width": width, 
            "cov": cov, 
            "cap_r2w": cap_r2w,
            "wall_height": 3,
            "roof_height": 4, 
            "n_windows": 10
        }
        new_arr =tuple(damage_ration)
        session['dollar_damage'] = tuple(dollar_damage)
        session['params_object'] = params_object
        session['calculated_params'] = calculated_params
        session['damage_ration'] = new_arr
        session['value_est'] = value_est
        return redirect(url_for('mod_auth.estimation'))

    return render_template('customer/dashboard_customer.html', name=current_user.email, form=form)

@mod.route('/estimation', methods=['GET', 'POST'])
@login_required
def estimation():
    damage_ration = session.pop('damage_ration', None)
    dollar_damage = session.pop('dollar_damage', None)
    value_est = session.pop('value_est', None)
    params_object = session.pop('params_object', None)
    session["dollar_damage"] = dollar_damage
    session["damage_ration"] = damage_ration
    session["value_est"] = value_est
    session["params_object"] = params_object
    gust_speed = np.arange(0, 120)  # m/s
    dollar_damage= np.array(dollar_damage)
    dollar_damage = dollar_damage - dollar_damage[0]
    my_plot_div = plot([Scatter(x=gust_speed * 2.237, y= dollar_damage)], output_type='div')
    damage_cats = [dollar_damage[30], dollar_damage[40], dollar_damage[48], dollar_damage[57], dollar_damage[65], dollar_damage[78]]
    damage_cats = [round(a/1000)*1000 for a in damage_cats]
    rate = rating(damage_cats)
    return render_template('customer/estimation.html', value = value_est * int(params_object["area"]) , div_placeholder= flask.Markup(my_plot_div), dollar_damage = damage_cats, rate = rate)

@mod.route('/mitigation', methods=['GET', 'POST'])
@login_required
def mitigation():
    form = MitigationForm()

    if form.validate_on_submit():
        mitigation_params = {
            "window_protection": form.window_protection.data,
            "roof_wall_connection": form.roof_wall_connection.data,
            "type_of_roof_cover": form.type_of_roof_cover.data,
            "type_of_roof_sheathing": form.type_of_roof_sheathing.data,
            "type_of_windows": form.type_of_windows.data
        }
        session["mitigation_params"] = mitigation_params
        return redirect(url_for('mod_auth.estimation_mit'))
    return render_template('customer/mitigate.html', form=form)

@mod.route('/estimation_mit', methods=['GET', 'POST'])
@login_required
def estimation_mit():
    damage_ration = session.pop('damage_ration', None)
    dollar_damage = session.pop('dollar_damage', None)
    value_est = session.pop('value_est', None)
    mitigation_params = session.pop('mitigation_params', None)
    params_object = session.pop('params_object', None)
    calculated_params = session.pop('calculated_params', None)
    
    session["mitigation_params"] = mitigation_params
    session['params_object'] = params_object
    session['calculated_params'] = calculated_params
    session['damage_ration'] = damage_ration
    session['value_est'] = value_est
    session["dollar_damage"] = dollar_damage
    value_est2 = (value_est * int(params_object["area"])) 
    print("area", int(params_object["area"]))
    print("value", value_est)

    cap_r2w = None
    if mitigation_params["roof_wall_connection"] == "d":
        cap_r2w = calculated_params["cap_r2w"]
    else:
        cap_r2w = int(mitigation_params["roof_wall_connection"])

    cap_rs = None
    if mitigation_params["type_of_roof_sheathing"] == "d":
        cap_rs = calculated_params["cap_rs"]
    else:
        cap_rs = int(mitigation_params["type_of_roof_sheathing"])

    cap_rc = None
    if mitigation_params["type_of_roof_cover"] == "d":
        cap_rc = calculated_params["cap_rc"]
    else:
        cap_rc = int(mitigation_params["type_of_roof_cover"])

    cap_window = None
    if mitigation_params["type_of_windows"] == "d":
        cap_window = calculated_params["cap_window"]
    else:
        cap_window = int(mitigation_params["type_of_windows"])
 
    if mitigation_params["window_protection"] == "True":
        cap_window = 6300

    gust_speed = np.arange(0, 120)  # m/s
    print(cap_r2w, cap_rs, cap_rc, cap_window)
    
    damage_ration = vul.vulnerability(exp_cat=calculated_params["exp_cat"], gust_speed=gust_speed, cap_walls=calculated_params["cap_walls"],
                            cap_rc=cap_rc, cap_rs=cap_rs, cap_window=cap_window, cap_door=calculated_params["cap_door"],
                            cap_gd=calculated_params["cap_gd"], lenght=calculated_params["lenght"], width=calculated_params["width"], cov=calculated_params["cov"], wall_height=3,
                            roof_height=4, n_windows=10) 
    print(damage_ration)
    dollar_damage= np.array(dollar_damage)
    dollar_damage = dollar_damage - dollar_damage[0]
    dollar_damage_mit = damage_ration * int(value_est) * int(params_object["area"])
    dollar_damage_mit = dollar_damage_mit - dollar_damage_mit[0]
    damage_cats = [dollar_damage[30], dollar_damage[40], dollar_damage[48], dollar_damage[57], dollar_damage[65], dollar_damage[78]]
    damage_cats = [round(a/1000)*1000 for a in damage_cats]
    damage_cats_mit = [dollar_damage_mit[30], dollar_damage_mit[40], dollar_damage_mit[48], dollar_damage_mit[57], dollar_damage_mit[65], dollar_damage_mit[78]]
    damage_cats_mit = [round(a/1000)*1000 for a in damage_cats_mit]
    rate = rating(damage_cats_mit)

    my_plot_div = plot([Scatter(x=gust_speed * 2.237, y= dollar_damage)], output_type='div')
    my_plot_div_mit = plot([Scatter(x=gust_speed * 2.237, y= dollar_damage_mit)], output_type='div')

    return render_template('customer/estimation_mit.html', value = value_est2, div_placeholder= flask.Markup(my_plot_div), div_placeholder_mit = flask.Markup(my_plot_div_mit), dollar_damage = damage_cats, dollar_damage_mit = damage_cats_mit, rate = rate)


