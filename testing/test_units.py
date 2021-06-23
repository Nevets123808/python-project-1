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

        #Add test records here
        user = Users(username = "NewUser", email = "test@testing.com")
        db.session.add(user)
        db.session.commit()

        user = Users.query.first()
        ship = Ships(ship_name = "NewShip", speed = 1, owner_id = user.user_id)
        db.session.add(ship)
        db.session.commit()

        

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
    
    # def test_select_user(self):
    #     response = self.client.get(url_for('selectuser', user_id = 1))
    #     self.assertEqual(response.status_code, 200)

    def test_new_user(self):
        response = self.client.get(url_for('newuser'))
        self.assertIn(b'Please enter user details', response.data)

    def test_delete_user(self):
        user = Users.query.first()
        response = self.client.get(url_for('deleteuser', user_id = user.user_id), follow_redirects = True)
        self.assertNotIn(b"NewUser", response.data)
    
    def test_user_details(self):
        user = Users.query.first()
        response = self.client.post(url_for('userdetails', user_id = user.user_id), data = dict(name="Newer User",email=None), follow_redirects = True)
        self.assertIn(b"Newer User", response.data)
    
    def test_shiplist(self):
        user = Users.query.first()
        response = self.client.get(url_for('shiplist', user_id = user.user_id))
        self.assertIn(b"NewShip", response.data)
    
    def test_ship(self):
        user = Users.query.first()
        ship = Ships.query.filter_by(owner_id=user.user_id).first()
        response = self.client.get(url_for('ship', user_id = user.user_id, ship_id= ship.ship_id))
        self.assertIn(b'NewShip', response.data)
    
    def test_new_ship(self):
        user= Users.query.first()
        response = self.client.post(url_for('newship', user_id = user.user_id), data = dict(name="NewerShip", type='Fast'), follow_redirects = True)
        ships = Ships.query.filter_by(owner_id=user.user_id).all()
        self.assertEqual(len(ships), 2)

    def test_sail(self):
        user = Users.query.first()
        ship = Ships.query.filter_by(owner_id = user.user_id).first()
        response = self.client.get(url_for('sail', user_id = user.user_id, ship_id = ship.ship_id, route_id = 1))
        self.assertEqual(response.status_code, 200)

    def test_ship_details(self):
        user = Users.query.first()
        ship = Ships.query.filter_by(owner_id= user.user_id).first()
        response = self.client.post(url_for('shipdetails', user_id = user.user_id, ship_id = ship.ship_id), data =dict(name="NewerShip"), follow_redirects=True)
        self.assertIn(b'NewerShip', response.data)
    
    def test_delete_ship(self):
        user = Users.query.first()
        ship = Ships.query.filter_by(owner_id = user.user_id).first()
        response = self.client.get(url_for('deleteship', user_id = user.user_id, ship_id = ship.ship_id))
        self.assertNotIn(b'NewShip', response.data)

    def test_admin(self):
        response = self.client.get(url_for('admin'))
        self.assertIn(b'Admin Options', response.data)
    
    def test_make_admin(self):
        response = self.client.post(url_for('makeadmin'), data = dict(user = 'NewUser'))
        user= Users.query.first()
        self.assertEqual(user.admin, True)
    
    def test_new_city(self):
        response = self.client.post(url_for('newcity'), data = dict(name="Newerton"))
        city = Cities.query.filter_by(city_name = "Newerton").first()
        self.assertEqual(city.city_name, "Newerton")
        route = Routes.query.filter_by(departing_id = city.city_id).first()
        self.assertIsNotNone(route)
    
    def test_new_route(self):
        response = self.client.get(url_for('newroute'))
        self.assertEqual(response.status_code, 200)