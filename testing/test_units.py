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
        db.drop_all()
        return app
    
    def setUp(self):
        """
        Remember, this is before every test
        """
        #Create table
        db.create_all()

        #Add test records here
        #one test user
        user = Users(username = "NewUser", email = "test@testing.com")
        db.session.add(user)
        db.session.commit()

        #three test cities
        city1 = Cities(city_name = "TestCity1")
        city2 = Cities(city_name = "TestCity2")
        city3 = Cities(city_name = "TestCity3")

        db.session.add_all([city1,city2,city3])
        db.session.commit()

        city1 = Cities.query.filter_by(city_name="TestCity1").first()
        city2 = Cities.query.filter_by(city_name="TestCity2").first()
        city3 = Cities.query.filter_by(city_name="TestCity3").first()

        #Test route for each city and between city1 and city2 (there and back again)
        route1 = Routes(departing_id = city1.city_id, destination_id = city1.city_id, length = 0)
        route2 = Routes(departing_id = city2.city_id, destination_id = city2.city_id, length = 0)
        route3 = Routes(departing_id = city3.city_id, destination_id = city3.city_id, length = 0)
        route12 = Routes(departing_id = city1.city_id, destination_id = city2.city_id, length = 10)
        route21 = Routes(departing_id = city2.city_id, destination_id = city1.city_id, length = 10)

        db.session.add_all([route1, route2, route3, route12, route21])
        db.session.commit()
        
        #two test ships after all the routes so it has a route to sit on, one in city, one sailing
        user = Users.query.first()
        route = Routes.query.filter_by(departing_id=city1.city_id, destination_id=city1.city_id).first()
        sail_route = Routes.query.filter_by(departing_id=city1.city_id, destination_id=city2.city_id).first()
        ship = Ships(ship_name = "NewShip", speed = 1, owner_id = user.user_id, route_id = route.route_id)
        sailing = Ships(ship_name = "Sailing", speed = 3, owner_id = user.user_id, route_id = sail_route.route_id)
        db.session.add_all([ship, sailing])
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
        response = self.client.post(url_for('newuser'), data = dict(name = "Newer User",email="new@newer.new"), follow_redirects=True)
        self.assertIn(b"Newer User", response.data)

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
        num_ships = len(Ships.query.filter_by(owner_id=user.user_id).all())
        response = self.client.post(url_for('newship', user_id = user.user_id), data = dict(name="NewerShip", type='Fast', city = 'TestCity1'), follow_redirects = True)
        ships = Ships.query.filter_by(owner_id=user.user_id).all()
        self.assertEqual(len(ships), num_ships+1)

    def test_sail_in_sailing(self):
        user = Users.query.first()
        ship = Ships.query.filter_by(ship_name="Sailing").first()
        response = self.client.get(url_for('sail', user_id = user.user_id, ship_id = ship.ship_id))
        self.assertIn(b"is currently on the way to", response.data)

    def test_sail_in_city(self):
        user = Users.query.first()
        ship = Ships.query.filter_by(ship_name="NewShip").first()
        response = self.client.get(url_for('sail', user_id = user.user_id, ship_id = ship.ship_id))
        self.assertIn(b"is currently docked in", response.data)
    
    def test_set_sail(self):
        user = Users.query.first()
        ship = Ships.query.filter_by(ship_name="NewShip").first()
        response = self.client.post(url_for('sail', user_id = user.user_id, ship_id = ship.ship_id), data = dict(destination = 'TestCity2'), follow_redirects=True)
        self.assertIn(b"is currently on the way to", response.data)

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
    
    def tet_admin_city_list(self):
        response = self.client.get(url_for('admincitylist'))
        self.assertIn(b"TestCity3", response.data)
    
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
        city1 = Cities.query.filter_by(city_name="TestCity1").first()
        city3 = Cities.query.filter_by(city_name="TestCity3").first()
        response = self.client.post(url_for('newroute', city_id = city1.city_id), data=dict(destination = city3.city_name, length =10))
        route = Routes.query.filter_by(departing_id = city3.city_id, destination_id = city1.city_id,).first()
        self.assertEqual(route.length, 10)
    
    def test_end_turn(self):
        ship = Ships.query.filter_by(ship_name = "Sailing").first()
        ship.dist = 9
        db.session.commit()
        response = self.client.get(url_for('endturn'))
        self.assertEqual(ship.dist, 0)