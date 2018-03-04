from sqlalchemy import db.Column, db.Integer, String, ForeignKey, db.DateTime, func, Date, Time
from sqlalchemy.ext.declarative import declarative_db.Model
from sqlalchemy.orm import relationship, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin
import db.DateTime
from ../app import app

app.config['SQLALCHEMY_DATAdb.Model_URI'] = "postgresql://localhost/cutcheck"  #+psycopg2
db = SQLAlchemy(app)
lm = LoginManager(app)

 
"""
    Shop (Service Provider) class representing the SQL table for service providers. 
    Stores basic info about the shop(Name, Location, Image. 
    Related its Employees with backref.  
                                                            """
class Shop(db.Model):
    __tablename__ = "Shops"

    ShopId = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(80), nullable=False)
    Location = db.Column(db.String(80), nullable=False)
    Img_path = db.Column(db.String(120), nullable=False)
    Shop_login = db.Column(db.String(80), nullable = False)
    Shop_password = db.Column(db.String(80), nullable = False)

    Employees = relationship("Employee", backref="Shops")
    #Enable backpropagation between Shops and their working hours
    Schedules = relationship("Schedule", backref="Shops")


    def __init__(self, name, location, img, login, password):
        self.Name = name
        self.Location = location
        self.Img_path = img
        self.Shop_login = login
        self.Shop_password = password

    def __repr__(self):
        return '<Name %r>' %self.Name

""" 
    ShopManager class represents table storing shop managers - users authorized to perfrom 
    actions like shop registration, employee registration, employee deletion and edition.
    ShopManager can edit Employees schedules. 
"""


"""
    Employee class representing the SQL table for users authorized by shops. 
    Stores basic info about the employee: First and Last Name, Phone Number, email. 
    Emplyees are related to their appoinments and the shop their work for.  
                                                            """

class Employee(db.Model):

    __tablename__  = "Employees"

    EmployeeId = db.Column(db.Integer, primary_key = True)
    FirstName = db.Column(db.String(60), nullable = False)
    LastName = db.Column(db.String(60), nullable = False)
    PhoneNumber = db.Column(db.String(15), nullable = False)
    Email = db.Column(db.String(50), nullable = False)
    Manager = db.Column(db.Integer, unique = False, default = 0) #default to false
    Password = db.Column(db.String(80), nullable = False)
    ShopId = db.Column(db.Integer, ForeignKey("Shops.ShopId"))

    #Enable backpropagation between Employees and their Appointments
    Appointments = relationship("Appointment", backref = "Employees")
    #Enable backpropagation between Employees and their Schedules
    Schedules = relationship("Schedule", backref="Employees")

    def __init__(self, firstname, lastname, phonenumber, email, managerBool, password):
        self.FirstName = firstname
        self.LastName = lastname
        self.PhoneNumber = phonenumber
        self.Email = email
        self.Manager = managerBool
        self.Password = password

    def __repr__(self):
        name = self.FirstName + self.LastName
        return '<Name %r, Email %r, Phone Number %r>' %(name, self.Email, self.PhoneNumber)

"""
    User (Customer) class representing the SQL table for customers. 
    Stores basic info about the users. Users are related to their appoinments. 
    Requires implementation of encryption for password. 
                                                            """
class User(UserMixin, db.Model ):

    __tablename__ = "Users"

    UserId = db.Column(db.Integer, primary_key = True)
    social_id = db.Column(db.String(64), nullable=False, unique = True)
    Name = db.Column(String(60), nullable = False)
    Email = db.Column(String(60), nullable = False, unique = True)
    PhoneNumber = db.Column(String(60), unique = True)
    Password = db.Column(String(300), nullable = True)

    #relationships
    Appointments = relationship("Appointment", backref = "Users")

    def __init__(self, name, email, phonenumber, password):
        self.Name = name
        self.Email = email
        self.PhoneNumber = phonenumber
        self.password = password

    def __repr__(self):
        return '<Name %r, Email %r, Phone Number %r>' % (self.name, self.Email, self.PhoneNumber)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


"""
    Appointment (main event) class representing the SQL table for the services provided by shops. 
    Scheduled appointments for each employee.
    Stores basic info about the users and employees. 
    Related to the users, employees and shops with backref.                       
    The time frames needs to be within employees working hours for the given day.
    Working hours are defined and stored in the Schedule table.
                                                                """
class Appointment(db.Model):

    __tablename__ = "Appointments"

    AppointmentId = db.Column(db.Integer, primary_key = True)
    DateCreated = db.Column(db.DateTime, default = func.now(), nullable = False)
    DateScheduled = db.Column(db.Date, nullable = False)
    UserName = db.Column(db.String(60), nullable = False)
    UserPhoneNumber = db.Column(db.String(15))
    UserEmail = db.Column(db.String(60))

    EmployeeId = db.Column(db.Integer, ForeignKey("Employees.EmployeeId"))
    ShopId = db.Column(db.Integer, ForeignKey("Shops.ShopId"))
    UserId = db.Column(db.Integer, ForeignKey("Users.UserId"))

    def __init__(self, datescheduled, username, userphone, useremail, employeeid, shopid):
        self.DateScheduled = datescheduled
        self.UserName = username
        self.UserPhoneNumber = userphone
        self.UserEmail = useremail
        self.EmployeeId = employeeid
        self.ShopId = shopid

    def __repr__(self):
        return '<User Name %r, User Email %r, Date and Time %r, EmployeeID %r>' \
               % (self.UserName, self.UserEmail, self.DateScheduled, self.EmployeeId)

"""Schedule class representing a daily availability for each of the employees. 
   It stores the WeekDay (0-6), ServiceLength (intervals), 
   StartTime (Employess start), EndTime(Emplouees End Time)                                                             
                                                                """
class Schedule(db.Model):

    __tablename__ = "Schedules"

    ScheduleId = db.Column(db.Integer, primary_key = True)
    WeekStartDate = db.Column(db.DateTime, nullable = False)
    WeekDay = db.Column(db.Integer) #0-6 0 = Moday 6 = Sunday
    ServiceLength = db.Column(db.Integer, nullable = False) #for example 20 minutes
    StartTime = db.Column(db.DateTime, nullable = False)
    EndTime = db.Column(db.DateTime, nullable = False)

    EmployeeId = db.Column(db.Integer, ForeignKey("Employees.EmployeeId"))
    ShopId = db.Column(db.Integer, ForeignKey("Shops.ShopId"))

    def __init__(self, weekday, servicelen, starttime, endtime):
        self.WeekDay = weekday
        self.ServiceLength = servicelen
        self.StartTime = starttime
        self.EndTime = endtime


    def __repr__(self):
        return '<Employee ID %r, Week Day %r, StartTime %r, EndTime %r, Service Length>' \
               % (self.EmployeeId, self.WeekDay, self.StartTime, self.EndTime, self.ServiceLength, )