from flask import url_for
from flask_testing import TestCase
from application import app, db
from application.models import *

class TestBase(TestCase):
    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
            SECRET_KEY='TEST_SECRET',
            DEBUG=True,
            WTF_CSRF_ENABLED=False
            )
        return app
    
    def setUp(self):
        """
        Remember, this is before every test
        """
        #Create table
        db.create_all()
        user = Users(username = "NewUser", email = "test@testing.com")
        db.session.add(user)
        db.session.commit()

        #Add test records here

    def tearDown(self):
        """
        After every test
        """

        db.session.remove()
        db.drop_all()

class TestRoutes(TestBase):
    def test_home_get(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create a new user", response.data)
    
    def test_select_user(self):
        response = self.client.get(url_for('selectuser', user_id = 1))
        self.assertEqual(response.status_code, 200)

    def test_new_user(self):
        response = self.client.get(url_for('newuser'))
        self.assertIn(b'Please enter user details', response.data)

    def test_delete_user(self):
        user = Users.query.first()
        response = self.client.get(url_for('deleteuser', user_id = user.user_id), follow_redirects = True)
        self.assertNotIn(b"NewUser", response.data)
    
    def test_user_details(self):
        response = self.client.get(url_for('userdetails', user_id = 1))
        self.assertEqual(response.status_code, 200)
    
    def test_shiplist(self):
        response = self.client.get(url_for('shiplist', user_id = 1))
        self.assertEqual(response.status_code, 200)
    
    def test_ship(self):
        response = self.client.get(url_for('ship', ship_id = 1))
        self.assertEqual(response.status_code, 200)
    
    def test_new_ship(self):
        response = self.client.get(url_for('newship'))
        self.assertEqual(response.status_code, 200)

    def test_sail(self):
        response = self.client.get(url_for('sail', ship_id = 1, route_id = 1))
        self.assertEqual(response.status_code, 200)

    def test_ship_details(self):
        response = self.client.get(url_for('shipdetails', ship_id = 1))
        self.assertEqual(response.status_code, 200)
    
    def test_admin(self):
        response = self.client.get(url_for('admin'))
        self.assertEqual(response.status_code, 200)
    
    def test_make_admin(self):
        response = self.client.get(url_for('makeadmin', user_id = 1))
        self.assertEqual(response.status_code, 200)
    
    def test_new_city(self):
        response = self.client.get(url_for('newcity'))
        self.assertEqual(response.status_code, 200)
    
    def test_new_route(self):
        response = self.client.get(url_for('newroute'))
        self.assertEqual(response.status_code, 200)