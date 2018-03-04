# Author: DANIEL BIS

from app import db
from app.mod_auth.models import User, Shop
from flask_login import UserMixin
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


"""class Appointment(db.Model):

    __tablename__ = "Appointments"

    appointmentId = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate = db.func.current_timestamp())
    date_scheduled = db.Column(db.Date, nullable = False)
    client_first = db.Column(db.String(60), nullable = False)
    client_last = db.Column(db.String(60), nullable = False)
    client_phone = db.Column(db.String(15))
    client_email = db.Column(db.String(60))

    employeeId = db.Column(db.Integer, ForeignKey("Employees.employeeId"))
    shopId = db.Column(db.Integer, ForeignKey("Shops.shopId"))
    userId = db.Column(db.Integer, ForeignKey("Users.id"))

    def __init__(self, datescheduled, username, userphone, useremail):
        self.Datescheduled = datescheduled
        self.client_first = client_first
        self.client_last = client_last
        self.client_phone = userphone
        self.client_email = client_email
        

    def __repr__(self):
        return '<Client Name %r, User Email %r, Date and Time %r, EmployeeID %r>' \
               % (self.client_first, self.client_email, self.datescheduled, self.employeeId)
"""
"""Schedule class representing a daily availability for each of the employees. 
   It stores the WeekDay (0-6), ServiceLength (intervals), 
   StartTime (Employess start), EndTime(Emplouees End Time)                                                             
                                                                """
class Schedule(db.Model):

    __tablename__ = "Schedules"

    scheduleId = db.Column(db.Integer, primary_key = True)
    #week_start_date = db.Column(db.DateTime, nullable = False)
    weekday = db.Column(db.Integer, default = -1) #0-6 0 = Moday 6 = Sunday
    service_length = db.Column(db.Integer, nullable = False, default=20) #for example 20 minutes
    start_time = db.Column(db.DateTime, nullable = False)
    end_time = db.Column(db.DateTime, nullable = False)

    emplId = db.Column(db.Integer, ForeignKey("Users.id"))

    def __init__(self, starttime, endtime, weekday = -1, servicelen = 20):
        self.weekDay = weekday
        self.serviceLength = servicelen
        self.start_time = starttime
        self.end_time = endtime


    def __repr__(self):
        return '<Employee ID %r, Week Day %r, StartTime %r, EndTime %r, Service Length>' \
               % (self.emplId, self.weekday, self.start_time, self.end_time, self.service_length, )


