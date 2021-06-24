
from application import db

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username= db.Column(db.String(50), nullable = False, unique = True)
    email= db.Column(db.String(50), nullable = False, unique = True)
    admin =db.Column(db.Boolean, default = False)
    money = db.Column(db.Integer, default = 0)
    ship = db.relationship("Ships", backref = "user")

class Cities(db.Model):
    city_id = db.Column(db.Integer, primary_key = True)
    city_name = db.Column(db.String(50), nullable = False, unique = True)
    destination = db.relationship("Routes", backref = "destination", foreign_keys = "Routes.destination_id")
    departing = db.relationship("Routes", backref = "departing", foreign_keys = "Routes.departing_id")

class Routes(db.Model):
    route_id = db.Column(db.Integer, primary_key = True)
    departing_id = db.Column(db.Integer, db.ForeignKey(Cities.city_id))
    destination_id = db.Column(db.Integer, db.ForeignKey(Cities.city_id))
    length = db.Column(db.Integer, default = 0)
    ship = db.relationship("Ships", backref = "route")

class Ships(db.Model):
    ship_id = db.Column(db.Integer, primary_key = True)
    ship_name = db.Column(db.String(50), nullable = False, unique = True)
    speed = db.Column(db.Integer, nullable = False)
    owner_id = db.Column(db.Integer, db.ForeignKey(Users.user_id))
    route_id = db.Column(db.Integer, db.ForeignKey(Routes.route_id))
    dist = db.Column(db.Integer, default = 0)



