
from application import db

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username= db.Column(db.String(50), nullable = False)
    email= db.Column(db.String(50), nullable = False)
    admin =db.Column(db.Boolean, default = False)

class Cities(db.Model):
    city_id = db.Column(db.Integer, primary_key = True)
    city_name = db.Column(db.String(50), nullable = False)

class Routes(db.Model):
    route_id = db.Column(db.Integer, primary_key = True)
    departing_id = db.Column(db.Integer, db.ForeignKey(Cities.city_id))
    destination_id = db.Column(db.Integer, db.ForeignKey(Cities.city_id))
    length = db.Column(db.Integer)

class Ships(db.Model):
    ship_id = db.Column(db.Integer, primary_key = True)
    ship_name = db.Column(db.String(50), nullable = False)
    speed = db.Column(db.Integer, nullable = False)
    owner_id = db.Column(db.Integer, db.ForeignKey(Users.user_id))
    route_id = db.Column(db.Integer, db.ForeignKey(Routes.route_id))



