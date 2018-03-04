#Author: DANIEL BIS

# Import flask and template operators
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
#import login manager 
from flask_login import LoginManager, current_user, login_required

# Define the WSGI application object
app = Flask(__name__)
Bootstrap(app)
# Configurations
app.config.from_object('config')


# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


# Define the database object which is imported
# by modules and controllers

 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.routes import mod
from app.mod_provider.routes import provider_mod
from app.mod_customer.routes import customer_mod

# Register blueprint(s)
app.register_blueprint(mod_auth.routes.mod)
app.register_blueprint(mod_provider.routes.provider_mod)
app.register_blueprint(mod_customer.routes.customer_mod)
# app.register_blueprint(xyz_module)
# ..


#Home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboardprovider')
@login_required
def dashboardprovider():
    return render_template('dashboardprovider.html', name=current_user.first_name)



# Sample HTTP error handling
"""@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404"""

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()