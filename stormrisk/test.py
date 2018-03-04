#Authors: Daniel Bis and Abraham D’mitri Joseph

########################################################################################
########  "premature optimization is root cause of all evil" - Donald Knuth ###########
########################################################################################

from app import app, db
from app.mod_auth.models import User, Shop
from app.mod_provider.models import Schedule
from flask import abort, url_for
from urllib.parse import urlparse
import os
import unittest
import tempfile


class TestBase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SIDOCHECK_TEST_DB"]
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        
        return app

    # executed after each test
    def tearDown(self):
        db.session.close()
        db.drop_all()


    ###############
    #### tests ####
    ###############
 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
 

    ########################
    #### helper methods ####
    ########################
 
    def register(self, firstname, lastname, email, password):
        return self.app.post(
            'auth/signup',
            data=dict(firstname = firstname, lastname = lastname, email=email, password=password),
            follow_redirects=True
        )

    def login(self, email, password):
        user1 = User("testuser", "testuserlast", "testuser@gmail.com", "testuserpass")
        db.session.add(user1)
        db.session.commit()
        return self.app.post(
            'auth/login',
            data=dict(email=email, password=password),
            follow_redirects=True
    )

    def logout(self):
        return self.app.get(
            'auth/logout',
            follow_redirects=True
        )  

    def test_valid_user_registration(self):
        response = self.register('test', 'User1','testUser1@gmail.com','FlaskRocks')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>New user has been created!</h1>', response.data)

    """def test_login(self):
        expectedPath = "localhost:8080/dashboardcustomer"
        response = self.login("testuser@gmail.com", "testuserpass")
        self.assertEqual(response.status_code, 200)
        self.assertIn (b'<title>Dashboard Customer</title>', response.data)"""


 #(USER) def __init__(self, firstname, lastname, email, password, role, manager = 0, phonenumber = "")
    def test_user_model(self):
        user1 = User("testuser", "testuserlast", "testuser@gmail.com", "testuserpass", "customer")
        user2 = User("testuser2", "testuser2", "shop1@gmail.com", "shop1pass", "customer", 1, "8506667676")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        self.assertEqual(User.query.count(), 2)

    def test_shop_model(self):
        user1 = User("testuser", "testuserlast", "testuser@gmail.com", "testuserpass", "shop")
        user2 = User("shop1", "shop1", "shop1@gmail.com", "shop1pass", "shop", 1, "8506667676")
        new_shop = Shop("shop1", 'location')
        new_shop.users.append(user2)
        #print("appended")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        u1 = User.query.filter_by(first_name="shop1").first()
        shop1 = Shop.query.filter_by(shopname="shop1").first()
        self.assertEqual(u1.shopId, shop1.shopId)

    def test_employee_model(self):
        user1 = User("testuser", "testuserlast", "testuser@gmail.com", "testuserpass", "customer")
        user2 = User("testuser2", "testuser2last",  "shop1@gmail.com","shop1pass", "employee", 1, "8506667676")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        empl_count = User.query.filter_by(role="employee").count()
        self.assertEqual(empl_count, 1)

    def test_add_schedule(self):
        #manager rights
        user1 = User("shop1", "shop1", "shop1@gmail.com", "shop1pass", "shop", 1, "8506667676")
        new_shop = Shop("shop1", 'location')
        db.session.add(new_shop)
        new_shop.users.append(user1)
        user2 = User("testuser2", "testuser2last",  "testuser1@gmail.com","shop1pass", "employee", 1, "8506667676")
        new_shop.users.append(user2)
        db.session.commit()
        empl = User.query.filter_by(email="testuser1@gmail.com").first()
        #shop = Shop.query.filter_by(shopId= empl.shopId)

        schedule = Schedule(starttime = "2018-02-22 11:00:00", endtime = "2018-02-22 6:00:00")
        empl.schedules.append(schedule)
        db.session.commit()

        schedule_count = Schedule.query.filter_by(emplId=empl.id).count()
        self.assertEqual(schedule_count, 1)







if __name__ == "__main__":
    unittest.main()
