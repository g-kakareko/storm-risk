from flask_sqlalchemy  import SQLAlchemy
from app import app, db
#Import models
from app.mod_auth.models import User, Shop, Employee
from app.mod_auth.routes import load_user

from app.mod_provider.models import Schedule