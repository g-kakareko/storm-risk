from app import db
from flask_login import UserMixin
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

#define user model
class User(UserMixin, db.Model):

    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key = True);
        #identification data email&password
    email = db.Column(db.String(64), nullable = False, unique = True)
    password = db.Column(db.String(128), nullable = False)
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate = db.func.current_timestamp())

    #relationships (will be defined later)
    #Appointments = relationship("Appointment", backref = "Users")

    def __init__(self, email, password):
        self.email = email
        self.password = password
      
     

    def __repr__(self):
        return '<Name %r, Email %r>' % (self.first_name, self.email)




